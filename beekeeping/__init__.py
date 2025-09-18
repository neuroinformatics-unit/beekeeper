from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("beekeeping")
except PackageNotFoundError:
    # package is not installed
    pass
