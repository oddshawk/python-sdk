"""OddsHawk Python SDK — REST client for the OddsHawk REST API."""

from oddshawk_sdk.hashing import generate_hash
from oddshawk_sdk.rest import Rest

__all__ = ["Rest", "generate_hash"]
__version__ = "0.1.0"
