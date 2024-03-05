--Supported platforms
local build_platforms = { "x64", "x32" }

--Supported configurations
local build_configurations = { "release", "debug" }

--[[
Table of all supported builds, one for each combination of build_platforms and build_configurations.
Each build is a table with four members: platform, configuration, filter, suffix.
platform and configuration are the premake platform and configurations for this build.
filter can be passed to premake's filter() function to match this specific build.
suffix is the filename suffix that should be used for this build.
]]--
local builds = {}
function doBuilds()
    --Translation table from premake's platform strings to CPU architecture strings
    local pfToArch = {
        x64 = "x86-64",
        x32 = "x86"
    }

    --Create a list of builds. Builds are a cartesian product of platforms and configurations.
    for _,x in ipairs( build_platforms ) do
        for _,y in ipairs( build_configurations ) do
            table.insert( builds, {
                platform = x,
                configuration = y,
                filter = {
                    "architecture:"..x,
                    "configurations:"..y
                },
                suffix = pfToArch[x]..(y == "debug" and "d" or "")
            } )
        end
    end

    --Set platforms and configurations.
    platforms( build_platforms )
    configurations( build_configurations )
end

function doFlags()
    --Use C++20 and give extra warnings in all builds
    filter( {} )
        cppdialect( "C++20" )
        warnings( "Extra" )

    --The x32 platform uses the x86 architecture
    filter( "platforms:x32" )
        architecture( "x86" )

    --The x64 platform uses the x86-64 architecture
    filter( "platforms:x64" )
        architecture( "x86_64" )

    --Enable debugging symbols in debug builds
    filter( "configurations:debug" )
        symbols( "On" )

    --Optimize for speed in release builds
    filter( "configurations:release" )
        optimize( "Speed" )

    --[[
    When compiling with G++:
    * -Wno-unknown-pragmas: Don't generate warnings for unknown pragmas (e.g. pragmas compatible with MSVC but not other compilers)
    ]]--
    filter( "toolset:gcc" )
        buildoptions( {
            "-Wno-unknown-pragmas"
        } )
end

--Use the appropriate suffix for each build
function doSuffixes()
    for _, build in ipairs( builds ) do
        filter( build.filter )
            targetsuffix( "_"..build.suffix )
    end
end

solution( "gll" )
    doBuilds()

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
        filter( "system:not windows" )
            --excludes( {} )

        --Exclude Linux files when compiling for non-linux OSes
        filter( "system:not linux" )
            --excludes( {} )

        doFlags()

        --The output library name is different depending on the
        --architecture and whether or not this is the debug/release version
        doSuffixes()
