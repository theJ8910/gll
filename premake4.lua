builds = {
    { "x32", "debug"   },
    { "x32", "release" },
    { "x64", "debug"   },
    { "x64", "release" }
}
local pfToArch = {
    x32 = "x86",
    x64 = "x64"
}
function getSuffix( build )
    return pfToArch[build[1]]..(build[2] == "debug" and "d" or "")
end

solution( "gll" )
    configurations( { "debug", "release" } )
    platforms( { "x32", "x64" } )

    project( "gll" )
        kind( "StaticLib" )
        language( "C++" )
        files( {
            "src/gll/**.cpp",
            "include/gll/**.hpp"
        } )

        includedirs( "include" )
        targetdir( "lib" )

        --Exclude Windows files when compiling for non-window OSes
        configuration( "not windows" )
            --excludes( {} )

        --Exclude Linux files when compiling for non-linux OSes
        configuration( "not linux" )
            --excludes( {} )

        configuration( {} )
            flags( { "ExtraWarnings" } )
        
        --We need to specify that we want to use the C++11 standard when compiling with G++
        configuration( "gmake" )
            buildoptions( {
                "-std=c++11"
            } )

        --Debug builds add symbols to generated libraries / executables to enable debugging
        configuration( "debug" )
            flags( { "Symbols" } )

        --Release builds optimize for speed
        configuration( "release" )
            flags( { "OptimizeSpeed" } )

        --The output library name is different depending on the
        --architecture and whether or not this is the debug/release version
        for _,build in pairs( builds ) do
            configuration( build )
                targetname( "gll_"..getSuffix( build ) )
        end