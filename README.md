# OddsHawk Python SDK

Installable client for the OddsHawk public odds catalog (`https://www.odds.software`).

```bash
pip install -e ".[dev]"
pytest
```

```python
from oddshawk_sdk import Rest

client = Rest("username", "api-password")
print(client.sports())
```

Auth: `X-OH-User` / `X-OH-Hash` (time-based HMAC-SHA256), same wire format as `@oddshawk/oddshawk-sdk`.

PyPI publish is Nathan-only (cn-123).
