from importlib.metadata import version, PackageNotFoundError
from .example_mod import do_primes
__all__ = ['do_primes']


try:
    __version__ = version("pvnnch")
except PackageNotFoundError:
    # package is not installed
    pass
