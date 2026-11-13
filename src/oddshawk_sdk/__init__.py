"""The package root: one import yields the REST client and the signature helper.

``__version__`` is this distribution's version, not the API's.
"""

from oddshawk_sdk.hashing import generate_hash
from oddshawk_sdk.rest import Rest

__all__ = ["Rest", "generate_hash"]
__version__ = "0.1.0"
