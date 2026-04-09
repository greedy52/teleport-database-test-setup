#!/bin/bash
# Test the Teleport database connection diagnostic endpoint.
# This hits the same API as the Discover "Test Connection" button.
#
# Usage:
#   ./test-conntest.sh
#
# Auth: needs both session cookie and bearer token.
#   Bearer token: DevTools → Network → any /webapi/ XHR → Authorization: Bearer <token>
#   Session cookie: DevTools → Network → any /webapi/ XHR → Cookie → __Host-session value

PROXY_HOST="${PROXY_HOST:-steve-beams.cloud.gravitational.io}"
CLUSTER="${CLUSTER:-$PROXY_HOST}"
DB_SERVICE="${DB_SERVICE:-test}"
DB_USER="${DB_USER:-teleport-admin}"
DB_NAME="${DB_NAME:-test}"

if [ -z "$BEARER_TOKEN" ]; then
  echo "Bearer token (DevTools → Network → /webapi/ XHR → Authorization: Bearer <token>):"
  read -r BEARER_TOKEN
fi

if [ -z "$SESSION_COOKIE" ]; then
  echo "Session cookie (DevTools → Network → /webapi/ XHR → Cookie → __Host-session):"
  read -r SESSION_COOKIE
fi

URL="https://${PROXY_HOST}/v1/webapi/sites/${CLUSTER}/diagnostics/connections"

echo "→ POST $URL"
echo "  resource=db  service=$DB_SERVICE  user=$DB_USER  db=$DB_NAME"
echo

curl -s -X POST "$URL" \
  -H "Authorization: Bearer $BEARER_TOKEN" \
  -H "Cookie: __Host-session=$SESSION_COOKIE" \
  -H "Content-Type: application/json" \
  -d "{
    \"resource_kind\": \"db\",
    \"resource_name\": \"$DB_SERVICE\",
    \"database_user\": \"$DB_USER\",
    \"database_name\": \"$DB_NAME\"
  }" | python3 -m json.tool

echo
