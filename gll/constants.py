#Constants
#The directory to look for the OpenGL Registry files in: gl.xml, glx.xml, wgl.xml
XML_DIR        = "xml"
GL_FILE        = "%s/gl.xml"  % XML_DIR
WGL_FILE       = "%s/wgl.xml" % XML_DIR
GLX_FILE       = "%s/glx.xml" % XML_DIR

#Extension to use for includes (headers) and source files, respectively
INC_EXT        = "hpp"
SRC_EXT        = "cpp"

#Name of the project; affects folder names
PROJECT_NAME   = "gll"

#Source and include directories
SRC_DIR        = "src"
INC_DIR        = "include"

#Source and include files will be output to these directories
SRC_PROJECT_DIR = SRC_DIR + "/" + PROJECT_NAME
INC_PROJECT_DIR = INC_DIR + "/" + PROJECT_NAME

#Namespaces to use, in order of nesting level
NAMESPACES     = ( "gll", )

#All #include guards will be prefixed with this string
GUARD_PREFIX   = "GLL_"

#The name that will be given to the types and extensions files (sans extension), respectively
TYPES_FILE     = "gl_types"
EXT_FILE       = "gl_ext"