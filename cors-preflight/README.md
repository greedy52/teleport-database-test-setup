# cors-preflight

Three Teleport apps to exercise CORS preflight: `target` has a CORS policy
listing `allowed` as an origin; `evil` is not listed. Loading either app in the
browser fetches `target` cross-origin — allowed succeeds, evil is blocked.

The `target` backend is a tiny Python server that handles `POST` and echoes
`Access-Control-Allow-Origin` on the actual response (in addition to Teleport's
preflight headers), so the browser can read the response when the origin is
allowed.

## Run

```bash
docker-compose up -d
```

Host ports: `target` → 9000, `allowed` → 9001, `evil` → 9002.

Replace `<cluster>` in `fetcher/index.html`, then restart:

```bash
docker-compose restart
```

## Teleport config

```yaml
app_service:
  enabled: true
  apps:
    - name: target
      uri: http://localhost:9000
      public_addr: target.<cluster>
      cors:
        allowed_origins: ["https://allowed.<cluster>"]
        allowed_methods: ["GET", "POST"]
        allowed_headers: ["X-Custom"]
        allow_credentials: true
    - name: allowed
      uri: http://localhost:9001
      public_addr: allowed.<cluster>
    - name: evil
      uri: http://localhost:9002
      public_addr: evil.<cluster>
```

## Verify

In the Web UI with devtools → Network:
- Click `target` first so the browser has a session cookie for it.
- Click `allowed` → preflight returns `Access-Control-Allow-Origin`, `POST` fires, page shows `OK 200`.
- Click `evil` → preflight returns no allow-origin header, browser blocks, page shows `BLOCKED …`.

Hard-reload (Cmd/Ctrl+Shift+R) between toggles so cached preflights don't mask changes.
