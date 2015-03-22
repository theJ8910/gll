import os.path

from gll.constants import *
from gll.util import maxOrZero

class Version:
    major = 1
    minor = 0

    def __init__( self, *args ):
        if len( args ) == 2 and all( type( x ) == int for x in args ):
            self.major, self.minor = args
        elif len( args ) == 1 and type( args[0] ) == str:
            self.major, self.minor = ( int(x) for x in args[0].split(".") )
        else:
            raise ValueError( "Wrong number / types of arguments provided to Version.__init__(): " + ", ".join( type(x).__name__ for x in args ) )

    def __str__( self ):
        return "%s.%s" % ( self.major, self.minor )
    def __lt__( self, other ):
        return self.major < other.major or self.major == other.major and self.minor < other.minor
    def __gt__( self, other ):
        return self.major > other.major or self.major == other.major and self.minor > other.minor
    def __le__( self, other ):
        return self.major < other.major or self.major == other.major and self.minor <= other.minor
    def __ge__( self, other ):
        return self.major > other.major or self.major == other.major and self.minor >= other.minor
    def __eq__( self, other ):
        return self.major == other.major and self.minor == other.minor
    def __ne__( self, other ):
        return self.major != other.major or self.minor != other.minor

#Stores information about types
class Type:
    def __init__( self, content, name = None, comment = None, api = None ):
        self.content = content
        self.name    = name
        self.comment = comment
        self.api     = api

#Base class for Enum and Command
class GLObj:
    def __init__( self ):
        self.owner = None

    def require( self, module ):
        if self.owner == None:
            self.owner = module
            getattr( self.owner, self.coreList ).append( self )
        else:
            print( "%s requires %s as well" % ( module.name, self.name ) )

        #if extension then...

    def remove( self, module ):
        if self.owner != None:
            getattr( self.owner, self.coreList    ).remove( self )
            getattr( self.owner, self.removedList ).append( self )
            #print( "%s removes %s" % ( module.name, self.name ) )
        else:
            print( "%s is removing %s even though it doesn't belong to anything" % ( module.name, self.name ) )

class Enum( GLObj ):
    coreList    = "coreEnums"
    removedList = "removedEnums"

    def __init__( self, name, value ):
        super().__init__()
        self.name    = name
        self.value   = value

    def getDefinition( self, nameWidth ):
        return "#define %s %s" % ( self.name.ljust( nameWidth ), self.value )

class Command( GLObj ):
    coreList    = "coreCommands"
    removedList = "removedCommands"

    def __init__( self, rv, name, params ):
        super().__init__()
        self.rv      = rv
        self.name    = name
        self.params  = params

        #Prototype name for this command (of the form PFN...PROC, where ... is the function's name in uppercase)
        self.prototypeName = "PFN%sPROC" % name.upper()

    #Function prototype appearing in an .hpp file
    #Needed by declarations and definitions of this command
    def getPrototype( self, rvWidth, ptnameWidth ):
        if len( self.params ) > 0:
            paramsString = " %s " % ", ".join( self.params )
        else:
            paramsString = ""

        #Note: The C preprocessor resolves GLAPI to APIENTRY on Windows, and nothing on other platforms
        return "typedef %s (GLAPI *%s)(%s);" % (
            self.rv.ljust( rvWidth ),
            self.prototypeName.ljust( ptnameWidth ),
            paramsString
        )

    #Declaration appearing in an .hpp file
    def getDeclaration( self, ptnameWidth ):
        return "extern %s %s;" % (
            self.prototypeName.ljust( ptnameWidth ),
            self.name
        )

    #Definition appearing in a .cpp file
    def getDefinition( self, ptnameWidth, nameWidth ):
        return "%s %s = nullptr;" % (
            self.prototypeName.ljust( ptnameWidth ),
            self.name.ljust( nameWidth )
        )

    #Appears in a function that loads the command
    def getLoadStatement( self, nameWidth, ptnameWidth ):
        return "if( !( %s = ( %s )getProcAddress( %s ) ) ) ++fail;" % (
            self.name.ljust( nameWidth ),
            self.prototypeName.ljust( ptnameWidth ),
            ( "\"%s\"" % self.name ).ljust( nameWidth + 2 )
        )

class Module:
    def __init__( self, name ):
        self.name         = name

        #Core
        self.coreEnums           = []
        self.coreCommands        = []
        self.coreLoadFunction    = "load_mod_%s"     % name

        #Removed
        self.removedEnums        = []
        self.removedCommands     = []
        self.removedLoadFunction = "load_mod_%s_rem" % name

    #Calling this tells the enum/command that this module requires it
    #If it is the first module to do so it becomes its "owner",
    #and is added to this module's core list
    def require( self, obj ):
        obj.require( self )

    #Calling this tells the enum/command that this module has removed it
    def remove( self, obj ):
        obj.remove( self )

    def computeWidths( self ):
        #The code generator sorts sections of data into columns.
        #To do this, it computes the max widths for:
        self.coreEnumWidth         = maxOrZero( len( enum.name             ) for enum    in self.coreEnums    )    #Enum names
        self.coreReturnValueWidth  = maxOrZero( len( command.rv            ) for command in self.coreCommands )    #Function return values
        self.corePrototypeWidth    = maxOrZero( len( command.prototypeName ) for command in self.coreCommands )    #Function prototypes
        self.coreFunctionNameWidth = maxOrZero( len( command.name          ) for command in self.coreCommands )    #Function names

        self.removedEnumWidth         = maxOrZero( len( enum.name             ) for enum    in self.removedEnums    )    #Enum names
        self.removedReturnValueWidth  = maxOrZero( len( command.rv            ) for command in self.removedCommands )    #Function return values
        self.removedPrototypeWidth    = maxOrZero( len( command.prototypeName ) for command in self.removedCommands )    #Function prototypes
        self.removedFunctionNameWidth = maxOrZero( len( command.name          ) for command in self.removedCommands )    #Function names

class Feature( Module ):
    def __init__( self, api, number ):
        #Parse version from number string; ensures number matches "\d.\d" format
        version = Version( number )
        
        #Name follows the following format: "namespace_major_minor"
        name = "%s_%s" % ( api, str(version).replace( ".", "_" ) )

        super().__init__( name )
        self.api     = api
        self.version = version

class Extension( Module ):
    def __init__( self, name, apis ):
        super().__init__( name )
        self.apis = apis

class SourceFile:
    basePath = SRC_PROJECT_DIR

    def __init__( self, path ):
        self.path         = "%s/%s" % ( self.basePath, path )
        self.relativePath = path
        self.fout         = None

    def writeComment( self ):
        self.fout.write( "/*\n%s\n-----------------------\nCopyright (c) 2015, theJ89\n\nDescription:\n    Automatically generated.\n*/\n" % self.relativePath )

    #Writes the beginning of each nested namespace block in the NAMESPACES constant
    def beginNamespaces( self ):
        if len( NAMESPACES ) > 0:
            for ns in NAMESPACES:
                self.fout.write( "namespace %s {\n" % ns )
            self.fout.write( "\n" )

    #Writes the end of each nested namespace block in the NAMESPACES constant
    def endNamespaces( self ):
        if len( NAMESPACES ) > 0:
            self.fout.write( "\n" )
            for ns in NAMESPACES:
                self.fout.write( "}\n" )

    def write( self, str ):
        self.fout.write( str )

    def __enter__( self ):
        self.fout = open( self.path, "w" )
        return self

    def __exit__( self, exc_type, exc_value, traceback ):
        self.fout.close()
        self.fout = None

class IncludeFile( SourceFile ):
    basePath = INC_PROJECT_DIR

    def __init__( self, path ):
        super().__init__( path )
        self.guardName = ( "%s%s" % ( GUARD_PREFIX, self.relativePath.replace( ".", "_" ).replace( "/", "_" ) ) ).upper()

    def beginIncludeGuard( self ):
        self.fout.write( "#ifndef %s\n" % self.guardName )
        self.fout.write( "#define %s\n" % self.guardName )
        self.fout.write( "\n\n\n\n" )

    def endIncludeGuard( self ):
        self.fout.write( "\n" )
        self.fout.write( "#endif //%s" % self.guardName )