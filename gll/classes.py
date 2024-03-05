"""
This module implements several classes used by GLL in the parse and generate function.

Many of the classes here correspond to structure of the XML files that GLL parses, such as Command.
Others correspond to generated files, e.g. SourceFile and IncludeFile.

Some code generation is handled here as well, e.g. Command can generate declarations and definitions,
and SourceFile and IncludeFile will enerate boilerplate comments, namespaces, include guards and the like.
"""
import os.path

from gll.constants import *

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
        return f"{self.major}.{self.minor}"
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
        if self.owner is None:
            self.owner = module
            getattr( self.owner, self.coreList ).append( self )
        else:
            print( f"{module.name} requires {self.name} as well" )

        #if extension then...

    def remove( self, module ):
        if self.owner is not None:
            getattr( self.owner, self.coreList    ).remove( self )
            getattr( self.owner, self.removedList ).append( self )
            #print( "%s removes %s" % ( module.name, self.name ) )
        else:
            print( f"{module.name} is removing {self.name} even though it doesn't belong to anything" )

class Enum( GLObj ):
    coreList    = "coreEnums"
    removedList = "removedEnums"

    def __init__( self, name, value ):
        super().__init__()
        self.name    = name
        self.value   = value

    def getDefinition( self, nameWidth ):
        return f"#define {self.name.ljust( nameWidth )} {self.value}"

class Command( GLObj ):
    coreList    = "coreCommands"
    removedList = "removedCommands"

    def __init__( self, rv, name, params ):
        super().__init__()
        self.rv      = rv
        self.name    = name
        self.params  = params

        #Prototype name for this command (of the form PFN...PROC, where ... is the function's name in uppercase)
        self.prototypeName = f"PFN{name.upper()}PROC"

    #Function prototype appearing in an .hpp file
    #Needed by declarations and definitions of this command
    def getPrototype( self, rvWidth, ptnameWidth ):
        if len( self.params ) > 0:
            paramsString = " {} ".format( ", ".join( self.params ) )
        else:
            paramsString = ""

        #Note: The C preprocessor resolves GLAPI to APIENTRY on Windows, and nothing on other platforms
        return f"typedef {self.rv.ljust( rvWidth )} (GLAPI *{self.prototypeName.ljust( ptnameWidth )})({paramsString});"

    #Declaration appearing in an .hpp file
    def getDeclaration( self, ptnameWidth ):
        return f"extern {self.prototypeName.ljust( ptnameWidth )} {self.name};"

    #Definition appearing in a .cpp file
    def getDefinition( self, ptnameWidth, nameWidth ):
        return f"{self.prototypeName.ljust( ptnameWidth )} {self.name.ljust( nameWidth )} = nullptr;"

    #Appears in a function that loads the command
    def getLoadStatement( self, nameWidth, ptnameWidth ):
        nameQuotedJustified = ( f"\"{self.name}\"" ).ljust( nameWidth + 2 )
        return f"if( !( {self.name.ljust( nameWidth )} = ( {self.prototypeName.ljust( ptnameWidth )} )getProcAddress( {nameQuotedJustified} ) ) ) ++fail;"

class Module:
    def __init__( self, name ):
        self.name         = name

        #Core
        self.coreEnums           = []
        self.coreCommands        = []
        self.coreLoadFunction    = f"load_mod_{name}"

        #Removed
        self.removedEnums        = []
        self.removedCommands     = []
        self.removedLoadFunction = f"load_mod_{name}_rem"

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
        self.coreEnumWidth            = max( ( len( enum.name             ) for enum    in self.coreEnums       ), default=0 )    #Enum names
        self.coreReturnValueWidth     = max( ( len( command.rv            ) for command in self.coreCommands    ), default=0 )    #Function return values
        self.corePrototypeWidth       = max( ( len( command.prototypeName ) for command in self.coreCommands    ), default=0 )    #Function prototypes
        self.coreFunctionNameWidth    = max( ( len( command.name          ) for command in self.coreCommands    ), default=0 )    #Function names

        self.removedEnumWidth         = max( ( len( enum.name             ) for enum    in self.removedEnums    ), default=0 )    #Enum names
        self.removedReturnValueWidth  = max( ( len( command.rv            ) for command in self.removedCommands ), default=0 )    #Function return values
        self.removedPrototypeWidth    = max( ( len( command.prototypeName ) for command in self.removedCommands ), default=0 )    #Function prototypes
        self.removedFunctionNameWidth = max( ( len( command.name          ) for command in self.removedCommands ), default=0 )    #Function names

class Feature( Module ):
    def __init__( self, api, number ):
        #Parse version from number string; ensures number matches "\d.\d" format
        version = Version( number )
        
        #Name follows the following format: "namespace_major_minor"
        name = "{}_{}".format( api, str( version ).replace( ".", "_" ) )

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
        self.path         = f"{self.basePath}/{path}"
        self.relativePath = path
        self.fout         = None

    def writeComment( self ):
        self.fout.write(
             "/*\n"
            f"{self.relativePath}\n"
             "-----------------------\n"
             "Copyright (c) 2024, theJ89\n"
             "\n"
             "Description:\n"
             "    Automatically generated.\n"
             "*/\n"
        )

    #Writes the beginning of each nested namespace block in the NAMESPACES constant
    def beginNamespaces( self ):
        if len( NAMESPACES ) > 0:
            for ns in NAMESPACES:
                self.fout.write( f"namespace {ns} {{\n" )
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
        self.guardName = "{}{}".format( GUARD_PREFIX, self.relativePath.replace( ".", "_" ).replace( "/", "_" ) ).upper()

    def beginIncludeGuard( self ):
        self.fout.write(
            f"#ifndef {self.guardName}\n"
            f"#define {self.guardName}\n"
             "\n\n\n\n"
        )

    def endIncludeGuard( self ):
        self.fout.write(
             "\n"
            f"#endif //{self.guardName}"
        )
