from .result import Result
from .run_catching import run_catching, run_catching_with

__all__ = ['Result', 'run_catching', 'run_catching_with']

# Version will be dynamically set by poetry-dynamic-versioning
try:
    from ._version import __version__
except ImportError:
    # Fallback for development
    __version__ = '0.0.0'
