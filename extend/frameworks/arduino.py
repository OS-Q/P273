from os.path import isdir, join

from SCons.Script import DefaultEnvironment


env = DefaultEnvironment()
platform = env.PioPlatform()
board_config = env.BoardConfig()

FRAMEWORK_DIR = platform.get_package_dir("framework-arduinoxmc")
assert isdir(FRAMEWORK_DIR)

env.Append(
    CPPDEFINES=[
        "ARDUINO_ARCH_ARM",
        ("ARDUINO", 10805)
    ],

    CFLAGS=[
        "-std=gnu11"
    ],

    CXXFLAGS=[
        "-std=gnu++11"
    ],

    LINKFLAGS=[
        "-T", env.BoardConfig().get("build.ldscript", join(
            platform.get_package_dir("framework-arduinoxmc"),
            "variants", env.BoardConfig().get("build.mcu"), "linker_script.ld")
        )
    ],

    CPPPATH=[
        join(FRAMEWORK_DIR, "cores"),
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "CMSIS", "NN", "Include"),  # comment out if no NN needed
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "CMSIS", "DSP", "Include"),  # comment out if no DSP needed
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "CMSIS", "Include"),
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "LIBS"),
        join(FRAMEWORK_DIR, "cores", "xmc_lib", "XMCLib", "inc"),
        join(FRAMEWORK_DIR, "cores", "usblib"),
        join(FRAMEWORK_DIR, "cores", "usblib","Class"),
        join(FRAMEWORK_DIR, "cores", "usblib","Class","Device"),
        join(FRAMEWORK_DIR, "cores", "usblib","Common"),
        join(FRAMEWORK_DIR, "cores", "usblib","Core"),
        join(FRAMEWORK_DIR, "cores", "usblib","Core","XMC4000"),
        join(FRAMEWORK_DIR, "cores", "avr"),
        join(FRAMEWORK_DIR, "variants", board_config.get("build.mcu"),
             "config", board_config.get("build.board_variant"))
    ],
)

env.Append(
    LIBSOURCE_DIRS=[
        join(FRAMEWORK_DIR, "libraries")
    ]
)

#
# Target: Build Core Library
#

libs = []

if "build.variant" in env.BoardConfig():
    env.Append(
        CPPPATH=[
            join(FRAMEWORK_DIR, "variants", board_config.get("build.mcu"))
        ]
    )
    libs.append(env.BuildLibrary(
        join("$BUILD_DIR", "FrameworkArduinoVariant"),
        join(FRAMEWORK_DIR, "variants", board_config.get("build.mcu"))
    ))

libs.append(env.BuildLibrary(
    join("$BUILD_DIR", "FrameworkArduino"),
    join(FRAMEWORK_DIR, "cores")
))
env.Prepend(LIBS=libs)
