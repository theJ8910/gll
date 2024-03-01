"""
This module implements various utilities for GLL.
"""
from sys import stderr

#Return the text content of a node as a complete string
#This function is called recursively on child nodes of the given node
#e.g. "<span>A, <bold>B<bold>, <italics>C</italics></span>" becomes "A, B, C"
def innerText( node ):
    str = node.text if node.text != None else ""
    for child in node:
        str += innerText( child ) + ( child.tail if child.tail != None else "" )
    return str

#Print error message, exit with code 1
def error( msg ):
    print( msg, file=stderr )
    exit( 1 )

#Called when encountering an unrecognized tag during parsing
def tagError( node ):
    error( "Unrecognized tag: \"%s\"" % node.tag )

#Returns the length of the longest item in iterable, or zero if iterable is empty.
def maxOrZero( iterable ):
    def generator():
        yield 0
        for x in iterable:
            yield x
    return max( generator() )
