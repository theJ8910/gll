"""
This module contains constants used in GLL.
"""

#GLL version:
VERSION = "1.0"

#The URLs to fetch OpenGL XML API Registry files from.
#Currently we're downloading these from Khronos Group's GitHub repos:
#    https://github.com/KhronosGroup/OpenGL-Registry/tree/main/xml/
GL_XML_API_REGISTRY_BASE_URL  = "https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/main/xml"
GL_URL  = f"{GL_XML_API_REGISTRY_BASE_URL}/gl.xml"
GLX_URL = f"{GL_XML_API_REGISTRY_BASE_URL}/glx.xml"
WGL_URL = f"{GL_XML_API_REGISTRY_BASE_URL}/wgl.xml"

#The XML API for EGL is found in a different repository:
#    https://github.com/KhronosGroup/EGL-Registry/main/api/
EGL_XML_API_REGISTRY_BASE_URL = "https://raw.githubusercontent.com/KhronosGroup/EGL-Registry/main/api"
EGL_URL                       = f"{EGL_XML_API_REGISTRY_BASE_URL}/egl.xml"

#The directory to look for the OpenGL Registry files in: gl.xml, glx.xml, wgl.xml, egl.xml
XML_DIR  = "xml"
GL_FILE  = f"{XML_DIR}/gl.xml"
GLX_FILE = f"{XML_DIR}/glx.xml"
WGL_FILE = f"{XML_DIR}/wgl.xml"
EGL_FILE = f"{XML_DIR}/egl.xml"

#List of registry files; each entry is a tuple consisting of the URL it can be found at and the path it should be stored at locally
REGISTRY_FILES = (
    ( EGL_URL, EGL_FILE ),
    ( GL_URL,  GL_FILE  ),
    ( GLX_URL, GLX_FILE ),
    ( WGL_URL, WGL_FILE )
)

#Extension to use for source files and includes (headers), respectively
SRC_EXT = "cpp"
INC_EXT = "hpp"

#Name of the project; affects folder names
PROJECT_NAME = "gll"

#Source and include directories
SRC_DIR = "src"
INC_DIR = "include"

#Source and include files will be output to these directories
SRC_PROJECT_DIR = f"{SRC_DIR}/{PROJECT_NAME}"
INC_PROJECT_DIR = f"{INC_DIR}/{PROJECT_NAME}"

#Namespaces to use, in order of nesting level
NAMESPACES = ( "gll", )

#All #include guards will be prefixed with this string
GUARD_PREFIX = "GLL_"

#The name that will be given to the types and extensions files (sans extension), respectively
TYPES_FILE = "gl_types"
EXT_FILE   = "gl_ext"
