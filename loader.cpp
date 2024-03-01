/*
loader.cpp
-----------------------
Copyright (c) 2015, theJ89

Description:
    Loaders are defined here.
*/

//Includes
#include <cstddef>      //std::ptrdiff_t

#ifdef _WIN32
#else
#include <GL/glx.h>     //glXGetProcAddress
#endif




namespace gll {




//Typedefs
//Prototype for gll loaders
typedef int (LoadFunction)();
//Prototype for loaded OpenGL functions
typedef void(*ProcAddress)();




//Module loaders
//TODO: autogenerate
LoadFunction load_mod_gl_1_0;
LoadFunction load_mod_gl_1_0_rem;
LoadFunction load_mod_gl_1_1;
LoadFunction load_mod_gl_1_1_rem;
LoadFunction load_mod_gl_1_2;
LoadFunction load_mod_gl_1_3;
LoadFunction load_mod_gl_1_3_rem;
LoadFunction load_mod_gl_1_4;
LoadFunction load_mod_gl_1_4_rem;
LoadFunction load_mod_gl_1_5;
LoadFunction load_mod_gl_2_0;
LoadFunction load_mod_gl_2_1;
LoadFunction load_mod_gl_3_0;
LoadFunction load_mod_gl_3_1;
LoadFunction load_mod_gl_3_2;
LoadFunction load_mod_gl_3_3;
LoadFunction load_mod_gl_4_0;
LoadFunction load_mod_gl_4_1;
LoadFunction load_mod_gl_4_2;
LoadFunction load_mod_gl_4_3;
LoadFunction load_mod_gl_4_4;
LoadFunction load_mod_gl_4_5;
LoadFunction load_mod_gl_4_6;




//Returns the process address
#if defined( _WIN32 )

ProcAddress getProcAddress( const char* name ) {
    //Try to grab the function with wglGetProcAddress.
    //Note: this requires an active context; it will fail immediately if one is not found.
    ProcAddress    ptr = (ProcAddress)wglGetProcAddress( name );
    std::ptrdiff_t rv  = (std::ptrdiff_t)ptr;

    //MSDN states that wglGetProcAddress returns NULL (0) on failure.
    //However, the OpenGL wiki claims that other implementations can additionally return 1, 2, 3, and -1 to indicate failures,
    //so we check for all 5 possible failure codes here:
    if( rv >= -1 && rv <= 3 )
        return nullptr;

    //TODO: Load the OpenGL dll and grab the functions from it directly if wglGetProcAddress fails.
    return ptr;
}

#else

ProcAddress getProcAddress( const char* name ) {
    return glXGetProcAddress( reinterpret_cast<const GLubyte*>( name ) );
}

#endif


int load_gl_1_0() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem();
}
int load_gl_1_1() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem();
}
int load_gl_1_2() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2();
}
int load_gl_1_3() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem();
}
int load_gl_1_4() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem();
}
int load_gl_1_5() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5();
}
int load_gl_2_0() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0();
}
int load_gl_2_1() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1();
}
int load_gl_3_0() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0();
}
int load_gl_3_1() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1();
}
int load_gl_3_1_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1();
}
int load_gl_3_2() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2();
}
int load_gl_3_2_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2();
}
int load_gl_3_3() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3();
}
int load_gl_3_3_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3();
}
int load_gl_4_0() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0();
}
int load_gl_4_0_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0();
}
int load_gl_4_1() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1();
}
int load_gl_4_1_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1();
}
int load_gl_4_2() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2();
}
int load_gl_4_2_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2();
}
int load_gl_4_3() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3();
}
int load_gl_4_3_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3();
}
int load_gl_4_4() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3()     +
           load_mod_gl_4_4();
}
int load_gl_4_4_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3()     +
           load_mod_gl_4_4();
}
int load_gl_4_5() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3()     +
           load_mod_gl_4_4()     +
           load_mod_gl_4_5();
}
int load_gl_4_5_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3()     +
           load_mod_gl_4_4()     +
           load_mod_gl_4_5();
}

int load_gl_4_6() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_1()     +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_4()     +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3()     +
           load_mod_gl_4_4()     +
           load_mod_gl_4_5();
           load_mod_gl_4_6();
}
int load_gl_4_6_comp() {
    return load_mod_gl_1_0()     +
           load_mod_gl_1_0_rem() +
           load_mod_gl_1_1()     +
           load_mod_gl_1_1_rem() +
           load_mod_gl_1_2()     +
           load_mod_gl_1_3()     +
           load_mod_gl_1_3_rem() +
           load_mod_gl_1_4()     +
           load_mod_gl_1_4_rem() +
           load_mod_gl_1_5()     +
           load_mod_gl_2_0()     +
           load_mod_gl_2_1()     +
           load_mod_gl_3_0()     +
           load_mod_gl_3_1()     +
           load_mod_gl_3_2()     +
           load_mod_gl_3_3()     +
           load_mod_gl_4_0()     +
           load_mod_gl_4_1()     +
           load_mod_gl_4_2()     +
           load_mod_gl_4_3()     +
           load_mod_gl_4_4()     +
           load_mod_gl_4_5();
           load_mod_gl_4_6();
}

/*
Load
----

Description:
    Call to load all available bindings and extensions for the currently active context.

Arguments:
    N/A

Returns:
    int: The number of bindings that failed to load.
*/
int Load() {
    return load_gl_4_6_comp();
}

}
