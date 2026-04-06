# teleport-db-via-ws

Test client for Teleport's database websocket API (`/webapi/sites/:site/db/exec/ws`).

Connects to a database through the Teleport Web UI websocket endpoint — the same path the browser uses.

## Setup

```
uv sync
```

Edit `config.toml` with your proxy address, database info, and auth credentials.

Auth values can be grabbed from browser DevTools:
- **Bearer token** (expires frequently — grab a fresh one each run): Network tab -> any `/webapi/` XHR -> Headers -> `Authorization: Bearer <token>`
- **Session cookie**: Network tab -> any `/webapi/` XHR -> Headers -> `Cookie` -> value of `__Host-session`

The script will prompt for auth values at runtime if left empty in config (recommended for bearer token).

## Usage

```bash
# Interactive SQL shell (default)
uv run main.py

# Single probe query (select user) and exit
uv run main.py ping

# Use a different config file
uv run main.py --config other.toml
```
