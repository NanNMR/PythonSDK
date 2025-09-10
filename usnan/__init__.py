"""USNAN SDK - Python SDK for USNAN API"""

from .client import USNANClient
from . import models

try:
    from importlib.metadata import version
except ImportError:
    # Python < 3.8 fallback
    from importlib_metadata import version

try:
    __version__ = version("usnan")
except Exception:
    # Fallback version when package metadata is not available
    __version__ = "dev"

del version
__all__ = ["USNANClient", "models"]
