"""
This is the main module for the GLL generator.
Implements functions to download and parse the OpenGL XML API Registry files, as well as cleaning up or generating C++ source code and header files from the registry.
It also processes options from the user to determine which function to invoke.
"""

#TODO: * commands and enums can be required in multiple places.
#        commands and enums can be required by one feature, removed by another, then required again by an extension.
#        :dealwithit:
#      * compatibility profiles (newer versions of OpenGL remove commands and enums added by earlier versions)
#        Non-removed stuff goes in the core folder
#        Removed stuff should go in the removed folder
#        When including headers and loading functions for contexts older than OpenGL 3.1,
#        load both core and removed functionality (because contexts that old haven't removed it yet!).
#      * Load and generate wgl and glx stuff
#      * Need main file + header that ties this all together

#Standard library
import xml.etree.ElementTree as ET
import sys
import os.path

from sys       import argv, exit, stderr
from traceback import print_exc
from os        import rmdir
from os.path   import basename as path_basename, dirname as path_dirname
from tempfile  import NamedTemporaryFile
from shutil    import move, rmtree
from re        import compile as re_compile

#Our stuff
from gll.constants import *
from gll.util import innerText, error, tagError
from gll.classes import Version, Type, Enum, Command, Feature, Extension, SourceFile, IncludeFile

#Third party
import requests

#OpenGL split into core and compatibility profiles in OpenGL 3.1
PROFILES_SINCE = Version( 3, 1 )

#Regular expression that matches "gles1" or "gles2"
RE_GLES = re_compile( "^gles1|2$" )

#Bookkeeping
includeTypes = []
types        = []
enums        = {}
commands     = {}
features     = []
extensions   = []

def main( argv ):
    try:
        argc = len( argv ) - 1
        if argc == 0:
            help()
        elif argc == 1:
            arg = argv[1];
            if   arg == "--clean":
                clean()
            elif arg == "--fetch":
                fetch()
            elif arg == "--generate":
                parse_and_generate()
            elif arg == "--version":
                print( VERSION )
            elif arg == "--help":
                help()
            else:
                raise RuntimeError( f"Unrecognized option \"{arg}\"." )
        else:
            raise RuntimeError( f"Expected at most 1 command-line argument but received {argc}." )
    except RuntimeError as e:
        if len( e.args ) > 0:
            print( f"error: {e.args[0]}", file=stderr )
        else:
            print_exc()
        return 1
    except Exception:
        print( "error: An unexpected exception occurred:", file=stderr )
        print_exc()
        return 1
    return 0

def help():
    print(
"""Usage:
    python -m gll.generate [OPTIONS]

Description:
    This program generates C++ source code and headers for Brimstone's
    OpenGL Loader (GLL) from OpenGL XML API Registry files.

    If this is your first time running this program, you should
    run this with the --fetch option to download the registry files
    needed to generate the code.

    After that, run this with the --build option to generate the C++
    source code and headers.

Options:
    --fetch     Fetch the latest OpenGL XML API Registry files.
    --clean     Delete generated C++ source code and headers.
    --generate  Generate C++ source code and headers.
    --version   Print gll.generate version and exit immediately.
    --help      Print this help text and exit immediately."""
    )

def fetch():
    """
    Fetches up-to-date copies of the OpenGL XML API Registry files.
    """
    #Create the local XML API Registry directory if it doesn't exist yet:
    os.makedirs( XML_DIR, exist_ok=True )

    #Download each file:
    for url, filepath in REGISTRY_FILES:
        directory = path_dirname(  filepath )
        prefix    = path_basename( filepath )
        if prefix != "":
            prefix += "."

        print( f"Downloading {url} to {filepath}..." )

        with requests.get( url, stream=True ) as res:
            res.raise_for_status()
            with NamedTemporaryFile( dir=directory, prefix=prefix, suffix=".part", mode="wb" ) as tfout:
                #Save temporary file name for later
                tempfile = tfout.name

                #Read up to 8KiB from the response at a time and write to the temporary file:
                for chunk in res.iter_content( 8192 ):
                    tfout.write( chunk )
                
                #If (and only if) the file was downloaded without issue, make the temporary file permanent.
                #HACK: The way we're accomplishing this here relies on an implementation detail in tempfile; changes to this module in the future may cause it to stop working:
                tfout._closer.delete = False
                
                #Move the file to its permanent location:
                move( tempfile, filepath )

def clean():
    """
    Deletes the source and header files that GLL generates.
    """
    #Ignore the FileNotFoundError generated by these functions if any
    #of these directories don't exist:
    try:
        rmtree( INC_PROJECT_DIR )
    except FileNotFoundError:
        pass
    try:
        rmdir( INC_DIR )
    except FileNotFoundError:
        pass
    try:
        rmtree( SRC_PROJECT_DIR )
    except FileNotFoundError:
        pass
    try:
        rmdir( SRC_DIR )
    except FileNotFoundError:
        pass

def parse_and_generate():
    """
    Parses the OpenGL XML API Registry files and generates source code from them.
    """
    parse()
    generate()

#Parse the gl.xml file to get the data we need to generate the headers
def parse():
    try:
        tree = ET.parse( GL_FILE )
    except FileNotFound:
        error( f"Can't find file \"{GL_FILE}\"." )
    except:
        error( f"An unexpected exception occured: {sys.exc_info()[1]}" )

    root = tree.getroot()
    if root.tag != "registry":
        error( f"Expected root node to be \"registry\", got \"{root.tag}\" instead." )

    for child in root:
        if   child.tag == "enums":
            parseEnums( child )
        elif child.tag == "feature":
            parseFeature( child )
        elif child.tag == "types":
            parseTypes( child )
        elif child.tag == "commands":
            parseCommands( child )
        elif child.tag == "extensions":
            parseExtensions( child )
        elif child.tag == "comment":
            print( f"/*{child.text}*/" )
        #ignore groups and kinds
        elif child.tag == "groups" or child.tag == "kinds":
            pass
        else:
            tagError( child )

    print( f"Parsed {len( enums      )} enums."      )
    print( f"Parsed {len( commands   )} commands."   )
    print( f"Parsed {len( features   )} features."   )
    print( f"Parsed {len( extensions )} extensions." )

def parseTypes( node ):
    global includeTypes
    global types
    for child in node:
        if child.tag == "type":
            #Note: "requires" attribute is ignored if it exists
            text = innerText( child )
            t = Type( text, child.get( "name" ), child.get( "comment" ), child.get( "api" ) )

            #Types that include headers need to go outside of namespaces
            if "#include" in text:
                includeTypes.append( t )
            else:
                types.append( t )
        else:
            tagError( child )

def parseEnums( node ):
    global enums

    for child in node:
        if child.tag == "enum":
            name  = child.attrib["name"]
            value = child.attrib["value"]
            enums[ name ] = Enum( name, value )
        #ignore "unused" tags
        elif child.tag == "unused":
            pass
        else:
            tagError( child )

def parseCommands( node ):
    global commands
    for child in node:
        if child.tag == "command":
            proto    = child.find( "proto" )
            rt, name = parseCommand_separate_return_type_and_name( proto )
            params   = [
                innerText( paramnode ).strip()
                for paramnode in child
                if paramnode.tag == "param"
            ]
            commands[ name ] = Command( rt, name, params )
        else:
            tagError( child )

def parseCommand_separate_return_type_and_name( node ):
    """
    Given a <proto> tag, which contains both the return type and the name of a function, parses the text it contains into separate return type and name parts
    and returns the parts as a tuple.
    """
    #No initial text.
    text = node.text
    if text is None:
        rt = ""
    #Initial text is present; this is part of the return type:
    else:
        rt = text
    
    noNameYet = True
    for child in node:
        #Found the <name> tag:
        if child.tag == "name":
            #This should be the last tag in <proto>.
            noNameYet = False

            #Set the name to the text inside the <name> tag, as well as any text that may follow it:
            name = innerText( child )
            text = node.tail
            if text is not None:
                name += text

        #Found part of the return type:
        elif noNameYet:
            #Add the inner text of this node, as well as any text that follows it to the return type:
            rt += innerText( child )
            text = child.tail
            if text is not None:
                rt += text
        #There shouldn't be any tags after <name>.
        else:
            raise RuntimeError( "Encountered a tag after <name> tag in <proto> tag in <command> tag." )

    #Remove whitespace from the beginning and end of the return type.
    rt = rt.strip()

    #We still don't have a return value:
    if rt == "":
        raise RuntimeError( "No return value found in <proto> tag in <command> tag." ) 

    #Remove whitespace from the beginning and end of the name.
    name = name.strip()

    #Never encountered a <name> tag, or name is empty:
    if noNameYet or name == "":
        raise RuntimeError( "Never encountered <name> tag in <proto> tag in <command> tag." )

    #We found both the return type and name as expected.
    return ( rt, name )
        

#Parse either a feature or extension
def parseModule( node, module ):
    for child in node:
        if child.tag == "require":
            for child2 in child:
                if child2.tag == "enum":
                    module.require( enums[    child2.attrib["name"] ] )
                elif child2.tag == "command":
                    module.require( commands[ child2.attrib["name"] ] )
                #ignore "type" tags
                elif child2.tag == "type":
                    pass
                else:
                    tagError( child2 )
        elif child.tag == "remove":
            for child2 in child:
                if child2.tag == "enum":
                    module.remove( enums[    child2.attrib["name"] ] )
                elif child2.tag == "command":
                    module.remove( commands[ child2.attrib["name"] ] )
                else:
                    tagError( child2 )
        else:
            tagError( child )

#Parse a feature (e.g. OpenGL 4.5, OpenGLES 1.1, etc)
def parseFeature( node ):
    feature = Feature( node.attrib["api"], node.attrib["number"] )
    parseModule( node, feature )

    features.append( feature )

#Parse an extension (e.g. GL_ARB_direct_state_access)
def parseExtensions( node ):
    for child in node:
        if child.tag == "extension":
            parseExtension( child )
        else:
            tagError( child )

    #Make sure list of extensions is sorted alphabetically by name
    extensions.sort( key = lambda x: x.name )

def parseExtension( node ):
    extension = Extension( node.attrib["name"], node.attrib["supported"].split("|") )
    parseModule( node, extension )

    extensions.append( extension )

#Generate the header files
def generate():
    #Prepare directories
    os.makedirs( SRC_PROJECT_DIR, exist_ok = True ) #src/gll
    os.makedirs( INC_PROJECT_DIR, exist_ok = True ) #include/gll

    #Write types file
    generateTypes()

    #Write one header and source file for each feature (e.g. GL 1.0, GL 4.5, GLES 1.0, etc)
    generateFeatures()

    #Write extensions header file
    #generateExtensions()

    #Generate user headers (these include the headers generated in previous steps)
    generateUserHeaders()

def generateType( typer, out ):
    #TEMP: Ignore GLES types
    api = typer.api
    if api is not None and RE_GLES.fullmatch( api ):
        return

    #If a type has a comment attribute, add this comment to the file above it
    comment = typer.comment
    if comment is not None:
        out.write( f"//{comment}\n" )
    out.write( f"{typer.content}\n" )

def generateTypes():
    if len( includeTypes ) == 0 and len( types ) == 0:
        return

    incpath = f"{TYPES_FILE}.{INC_EXT}"
    with IncludeFile( incpath ) as out:
        out.writeComment()
        out.beginIncludeGuard()

        out.write(
            "//Defines\n"
            "//GLAPI becomes APIENTRY on Windows, and disappears on other platforms\n"
            "#ifdef _WIN32\n"
            "#define GLAPI APIENTRY\n"
            "#else\n"
            "#define GLAPI\n"
            "#endif\n"
            "\n\n\n\n"
        )

        #Types with #include statements need to occur outside of a namespace
        if len( includeTypes ) > 0:
            out.write( "//Includes\n" )
            for typer in includeTypes:
                generateType( typer, out )
            out.write( "\n" )

        #All other types go in the namespace
        if len( types ) > 0:
            out.beginNamespaces()

            out.write( "//Types\n" )
            for typer in types:
                generateType( typer, out )

            out.endNamespaces()

        out.endIncludeGuard()

def generateFeatures():
    for feature in features:
        #TEMP: Don't generate gles stuff for now
        if feature.api != "gl":
            continue

        name = feature.name
        incCorePath    = f"mod_{name}.{INC_EXT}"
        incRemovedPath = f"mod_{name}_rem.{INC_EXT}"
        srcCorePath    = f"mod_{name}.{SRC_EXT}"
        srcRemovedPath = f"mod_{name}_rem.{SRC_EXT}"

        feature.computeWidths()

        GenerateFeatureInclude( feature, incCorePath )
        GenerateFeatureSource(  feature, srcCorePath, incCorePath )

        if len( feature.removedEnums ) > 0 or len( feature.removedCommands ) > 0:
            GenerateFeatureInclude( feature, incRemovedPath, True )
            GenerateFeatureSource(  feature, srcRemovedPath, incRemovedPath, True )

def GenerateFeatureInclude( feature, path, removed = False ):
    if removed:
        enums             = feature.removedEnums
        commands          = feature.removedCommands
        enumWidth         = feature.removedEnumWidth
        returnValueWidth  = feature.removedReturnValueWidth
        prototypeWidth    = feature.removedPrototypeWidth
    else:
        enums             = feature.coreEnums
        commands          = feature.coreCommands
        enumWidth         = feature.coreEnumWidth
        returnValueWidth  = feature.coreReturnValueWidth
        prototypeWidth    = feature.corePrototypeWidth

    with IncludeFile( path ) as out:
        out.writeComment()
        out.beginIncludeGuard()

        out.beginNamespaces()

        #Write enums
        if len( enums ) > 0:
            out.write( "//Enums\n" )
            for enum in enums:
                out.write( f"{enum.getDefinition( enumWidth )}\n" )
            out.write( "\n" )

        #Write prototypes
        if len( commands ) > 0:
            out.write( "//Prototypes\n" )
            for command in commands:
                out.write( f"{command.getPrototype( returnValueWidth, prototypeWidth )}\n" )

            #Write declarations
            out.write( "\n//Declarations\n" )
            for command in commands:
                out.write( f"{command.getDeclaration( prototypeWidth )}\n" )

        out.endNamespaces()

        out.endIncludeGuard()

def GenerateFeatureSource( feature, path, incpath, removed = False ):
    if removed:
        commands          = feature.removedCommands
        prototypeWidth    = feature.removedPrototypeWidth
        functionNameWidth = feature.removedFunctionNameWidth
        loadFunction      = feature.removedLoadFunction
    else:
        commands          = feature.coreCommands
        prototypeWidth    = feature.corePrototypeWidth
        functionNameWidth = feature.coreFunctionNameWidth
        loadFunction      = feature.coreLoadFunction
    
    #No commands means no need for a source file
    if len( commands ) == 0:
        return

    #Write source file
    with SourceFile( path ) as out:
        out.writeComment()

        out.write(
             "\n\n\n\n"
             "//Includes\n"
            f"#include <{PROJECT_NAME}/{TYPES_FILE}.{INC_EXT}>\n"
            f"#include <{PROJECT_NAME}/{incpath}>\n"
             "\n\n\n\n"
        )

        out.beginNamespaces()

        #TEMP
        out.write(
            "typedef void(*ProcAddress)();\n"
            "extern ProcAddress getProcAddress( const char* name );\n\n"
        )

        #Write definitions
        out.write( "//Definitions\n" )
        for command in commands:
            out.write( f"{command.getDefinition( prototypeWidth, functionNameWidth )}\n" )

        #Write loading function
        out.write(
            f"\nint {loadFunction}() {{\n"
             "    int fail = 0;\n\n"
             "    //Load Statements\n"
        )
        for command in commands:
            out.write( f"    {command.getLoadStatement( functionNameWidth, prototypeWidth )}\n" )
        out.write(
            "\n    return fail;\n"
            "}\n"
        )

        out.endNamespaces()

def generateExtensions():
    incpath = f"{EXT_FILE}.{INC_EXT}"
    with IncludeFile( incpath ) as out:
        out.writeComment()
        out.beginIncludeGuard()
        out.beginNamespaces()

        for extension in extensions:
            #Skip empty extensions
            if len( extension.enums ) == 0 and len( extension.commands ) == 0:
                continue

            out.write( f"//{extension.name}\n" )
            #Write enums
            if len( extension.enums ) > 0:
                out.write( "//Enums\n" )
                for enum in extension.enums:
                    out.write( f"{enum.getDefinition( extension.enw )}\n" )
                out.write( "\n" )

            #Write prototypes
            if len( extension.commands ) > 0:
                out.write( "//Prototypes\n" )
                for command in extension.commands:
                    out.write( f"{command.getPrototype( extension.rvw, extension.ptw )}\n" )

                #Write declarations
                out.write( "\n//Declarations\n" )
                for command in extension.commands:
                    out.write( f"{command.getDeclaration( extension.ptw )}\n" )
                out.write( "\n" )

        out.endNamespaces()
        out.endIncludeGuard()

    #Write extensions source file
    srcpath = f"{EXT_FILE}.{SRC_EXT}"
    with SourceFile( srcpath ) as out:
        out.writeComment()

        out.write(
             "\n\n\n\n"
             "//Includes\n"
            f"#include \"{EXT_FILE}.{INC_EXT}\"\n"
             "\n\n\n\n"
        )

        out.beginNamespaces()

        #Write extension struct (used in extension table)
        # fout.write(
        #     "typedef void (*load_function)();\n" +
        #     "struct ExtInfo {\n"                 +
        #     "    const char* const name;\n"      +
        #     "    bool loaded;\n"                 +
        #     "    const load_function loader;\n"  +
        #     "};"
        # );

        for extension in extensions:
            #Skip extensions with no commands (nothing to load)
            if len( extension.commands ) == 0:
                continue

            out.write(
                f"//Extension: {extension.name}\n"
                 "//Definitions\n"
            )

            for command in extension.commands:
                out.write( f"{command.getDefinition( extension.ptw, extension.fnw )}\n" )

            #Write loading function
            out.write(
                f"\nint {extension.loadFunction}() {{\n"
                 "    int fail = 0;\n\n"
                 "    //Load Statements\n"
            )

            for command in extension.commands:
                out.write( f"    {command.getLoadStatement( extension.fnw, extension.ptw )}\n" )
            out.write(
                "\n    return fail;\n"
                "}\n\n"
            )

        # fout.write( "ExtInfo extensions[] = {\n" )
        # for extension in extensions:
        #     fout.write( "    { \"%s\", false, %s },\n" % ( ( "\"%s\"," % extension.name ), extension.loadFunction if len( extension.commands ) > 0 else "nullptr" ) )
        # fout.write( "    { nullptr, false, nullptr }\n" )
        # fout.write( "};\n" )

        out.endNamespaces()

#Generates a user header for the given feature.
#User headers include the core headers for all features of the same API with versions less than or equal to the given feature.
#Writes the header to the given path.
#If compatibility is True, the header will also include the headers containing removed functionality from these features.
def generateUserHeader( feature, path, compatibility = False ):
    with IncludeFile( path ) as out:
        out.writeComment()
        out.beginIncludeGuard()
        
        out.write(
             "//Includes\n"
            f"#include \"{TYPES_FILE}.{INC_EXT}\"\n\n"
        )

        #We need to include the core headers for this version and every version that came before it
        for feature2 in features:
            if feature2.api == feature.api and feature2.version <= feature.version:
                out.write( f"#include \"mod_{feature2.name}.{INC_EXT}\"\n" )

                #As well as the removed headers, if we're generating a compatibility header
                if compatibility and ( len( feature2.removedEnums ) > 0 or len( feature2.removedCommands ) > 0 ):
                    out.write( f"#include \"mod_{feature2.name}_rem.{INC_EXT}\"\n" )

        out.endIncludeGuard()

#Generates files the user can include
def generateUserHeaders():
    for feature in features:
        corePath   = f"{feature.name}.{INC_EXT}"
        compatPath = f"{feature.name}_comp.{INC_EXT}"

        #We may or may not need to generate additional headers when generating for the GL api.
        if feature.api == "gl":
            #For GL 3.0 and below, a single header that includes both core and removed headers is generated.
            if feature.version < PROFILES_SINCE:
                generateUserHeader( feature, corePath, True )
            #For GL 3.1 and above, two headers (core and compatibility) are generated.
            #The former includes only the core headers, while the latter includes both core and removed headers.
            #The compatibility header has a "_comp" suffix added to distinguish it from the core header.
            else:
                generateUserHeader( feature, corePath )
                generateUserHeader( feature, compatPath, True )
        #For all other APIs we generate only a single header
        else:
            generateUserHeader( feature, corePath, True )

#Enter into main()
if __name__ == "__main__":
    exit( main( argv ) )
