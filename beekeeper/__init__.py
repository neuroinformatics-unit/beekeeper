from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("beekeeper")
except PackageNotFoundError:
    # package is not installed
    pass
