#!/usr/bin/env python3
"""
Teleport /webapi/sites/:site/db/exec/ws test client.

Usage:
    Fill in config.toml, then:
        uv run main.py ping                    # single probe query
        uv run main.py interactive              # interactive SQL shell
        uv run main.py ping --config other.toml
"""

import argparse
import asyncio
import json

import ssl
import sys
import urllib.parse

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # pip install tomli for <3.11


# ---------------------------------------------------------------------------
# Protobuf encoder/decoder for the Envelope message
#
# message Envelope {
#   string Version = 1;
#   string Type    = 2;
#   string Payload = 3;
# }
# ---------------------------------------------------------------------------

def _varint(n: int) -> bytes:
    out = []
    while n > 0x7F:
        out.append((n & 0x7F) | 0x80)
        n >>= 7
    out.append(n)
    return bytes(out)


def _field(number: int, value: str) -> bytes:
    tag = (number << 3) | 2  # wire type 2 = length-delimited
    b = value.encode()
    return bytes([tag]) + _varint(len(b)) + b


def encode_envelope(version: str, msg_type: str, payload: str) -> bytes:
    return _field(1, version) + _field(2, msg_type) + _field(3, payload)


def decode_envelope(data: bytes) -> tuple[str, str, str]:
    """Returns (version, type, payload)."""
    fields: dict[int, str] = {}
    i = 0
    while i < len(data):
        tag = data[i]; i += 1
        field_no = tag >> 3
        # all fields are wire type 2
        length = 0; shift = 0
        while True:
            b = data[i]; i += 1
            length |= (b & 0x7F) << shift
            shift += 7
            if not (b & 0x80):
                break
        fields[field_no] = data[i : i + length].decode()
        i += length
    return fields.get(1, ""), fields.get(2, ""), fields.get(3, "")


# Message type constants (lib/defaults/defaults.go)
T_RAW      = "r"
T_RESIZE   = "w"
T_DB_CONN  = "d"
T_META     = "s"
T_MFA      = "n"
T_CLOSE    = "c"
T_ERROR    = "e"


# ---------------------------------------------------------------------------
# Mode helpers
# ---------------------------------------------------------------------------

async def _drain(ws) -> None:
    """Read and print all remaining output until the server closes."""
    import websockets.exceptions
    try:
        async for msg in ws:
            if not isinstance(msg, bytes):
                continue
            _, t, payload = decode_envelope(msg)
            if t == T_RAW:
                sys.stdout.write(payload)
                sys.stdout.flush()
            elif t == T_ERROR:
                print(f"[error] {payload}", file=sys.stderr)
            elif t == T_CLOSE:
                break
    except websockets.exceptions.ConnectionClosed:
        pass


async def _ping(ws, protocol: str) -> None:
    """Send a single probe query then quit."""
    if protocol == "postgres":
        query, quit_cmd = "select user;\n", "\\q\n"
    elif protocol == "mysql":
        query, quit_cmd = "select user();\n", "exit\n"
    else:
        sys.exit(f"Unsupported protocol for probe query: {protocol}")

    print(f"Sending: {query.strip()}", file=sys.stderr)
    await ws.send(encode_envelope("1", T_RAW, query))
    await ws.send(encode_envelope("1", T_RAW, quit_cmd))
    await _drain(ws)


async def _interactive(ws) -> None:
    """Interactive SQL shell — read lines from stdin, send to server."""
    import websockets.exceptions

    loop = asyncio.get_event_loop()

    async def _reader():
        """Read from websocket and print output."""
        try:
            async for msg in ws:
                if not isinstance(msg, bytes):
                    continue
                _, t, payload = decode_envelope(msg)
                if t == T_RAW:
                    sys.stdout.write(payload)
                    sys.stdout.flush()
                elif t in (T_ERROR, T_CLOSE):
                    if t == T_ERROR:
                        print(f"[error] {payload}", file=sys.stderr)
                    break
        except websockets.exceptions.ConnectionClosed:
            pass

    async def _writer():
        """Read lines from stdin and send to websocket."""
        try:
            while True:
                line = await loop.run_in_executor(None, sys.stdin.readline)
                if not line:  # EOF (Ctrl-D)
                    break
                await ws.send(encode_envelope("1", T_RAW, line))
        except (websockets.exceptions.ConnectionClosed, EOFError):
            pass

    # Run reader and writer concurrently; when either finishes, cancel the other.
    reader = asyncio.create_task(_reader())
    writer = asyncio.create_task(_writer())
    done, pending = await asyncio.wait(
        [reader, writer], return_when=asyncio.FIRST_COMPLETED
    )
    for task in pending:
        task.cancel()


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

async def connect(cfg: dict, mode: str) -> None:
    import websockets
    import websockets.exceptions

    proxy   = cfg["proxy"]
    cluster = cfg["cluster"]
    db      = cfg["database"]
    term    = cfg["terminal"]
    auth    = cfg["auth"]

    if not cluster.get("site"):
        cluster["site"] = proxy["host"]

    if not auth.get("bearer_token"):
        print("Bearer token not set in config.toml.", file=sys.stderr)
        print("  → DevTools → Network → any /webapi/ XHR → Headers tab → Authorization: Bearer <token>", file=sys.stderr)
        auth["bearer_token"] = input("Paste bearer token: ").strip()
    if not auth.get("session_cookie"):
        print("Session cookie not set in config.toml.", file=sys.stderr)
        print("  → DevTools → Network → any /webapi/ XHR → Headers tab → Cookie → value of __Host-session", file=sys.stderr)
        auth["session_cookie"] = input("Paste session cookie: ").strip()

    params = urllib.parse.quote(json.dumps({"term": {"h": term["rows"], "w": term["cols"]}}))
    scheme = "ws" if proxy.get("insecure") else "wss"
    url = f"{scheme}://{proxy['host']}:{proxy['port']}/v1/webapi/sites/{cluster['site']}/db/exec/ws?params={params}"

    headers = {"Cookie": f"__Host-session={auth['session_cookie']}"}

    connect_kwargs: dict = dict(additional_headers=headers, max_size=10 * 1024 * 1024)
    if proxy.get("insecure"):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        connect_kwargs["ssl"] = ctx
    else:
        connect_kwargs["ssl"] = True

    print(f"→ {url}", file=sys.stderr)
    print(f"  service={db['service_name']}  protocol={db['protocol']}  db={db['db_name']}  user={db['db_user']}", file=sys.stderr)

    try:
        async with websockets.connect(url, **connect_kwargs) as ws:
            # ── 1. bearer token exchange ──────────────────────────────────
            await ws.send(json.dumps({"token": auth["bearer_token"]}))
            raw = await ws.recv()
            resp = json.loads(raw if isinstance(raw, str) else raw.decode())
            if resp.get("status") != "ok":
                sys.exit(f"Auth failed: {resp}")
            print("Authenticated.", file=sys.stderr)

            # ── 2. send DatabaseSessionRequest ───────────────────────────
            req = {
                "serviceName": db["service_name"],
                "protocol":    db["protocol"],
                "dbName":      db["db_name"],
                "dbUser":      db["db_user"],
                "dbRoles":     db.get("db_roles", []),
            }
            await ws.send(encode_envelope("1", T_DB_CONN, json.dumps(req)))
            print(f"DB connect request sent: {req}", file=sys.stderr)

            # ── 3. wait for session metadata (may get RAW output first) ───
            while True:
                msg = await ws.recv()
                if not isinstance(msg, bytes):
                    print(f"unexpected text frame: {msg}", file=sys.stderr)
                    continue
                ver, t, payload = decode_envelope(msg)
                if t == T_ERROR:
                    sys.exit(f"Server error: {payload}")
                elif t == T_CLOSE:
                    print(f"Session closed: {payload}", file=sys.stderr)
                    return
                elif t == T_MFA:
                    sys.exit("MFA required — not implemented in this client")
                elif t == T_META:
                    print(f"Session metadata: {payload}", file=sys.stderr)
                    break
                elif t == T_RAW:
                    sys.stdout.write(payload)
                    sys.stdout.flush()

            # ── 4. run mode ───────────────────────────────────────────────
            if mode == "ping":
                await _ping(ws, db["protocol"])
            else:
                await _interactive(ws)

    except websockets.exceptions.InvalidStatus as e:
        print(f"HTTP {e.response.status_code}", file=sys.stderr)
        print(f"Headers: {dict(e.response.headers)}", file=sys.stderr)
        print(f"Body: {e.response.body.decode(errors='replace')}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Teleport DB websocket test client")
    parser.add_argument("--config", default="config.toml")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("ping", help="Send a single probe query and exit")
    sub.add_parser("interactive", aliases=["i"], help="Interactive SQL shell")

    args = parser.parse_args()
    if not args.command:
        args.command = "interactive"

    with open(args.config, "rb") as f:
        cfg = tomllib.load(f)

    mode = "interactive" if args.command in ("interactive", "i") else "ping"
    asyncio.run(connect(cfg, mode))


if __name__ == "__main__":
    main()
