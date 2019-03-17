from platform import platform

SYSTEM = platform()

if "Linux" == SYSTEM:
    from .linux_color import LinuxColorizer as Colorizer
