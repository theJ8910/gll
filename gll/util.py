"""
This module implements various utilities for GLL.
"""
from sys import stderr, exit

def innerText( node ):
    """
    Returns the text content of a node as a complete string.
    This function is called recursively on child nodes of the given node;
    e.g. "<span>A, <bold>B<bold>, <italics>C</italics></span>" becomes "A, B, C"
    """
    text = node.text
    rv = "" if text is None else text
    for child in node:
        text = child.tail
        rv += innerText( child ) + ( "" if text is None else text )
    return rv

def error( msg ):
    """Prints the given error message and exits with code 1."""
    print( msg, file=stderr )
    exit( 1 )

def tagError( node ):
    """Called when encountering an unrecognized tag during parsing."""
    error( f"Unrecognized tag: \"{node.tag}\"" )
