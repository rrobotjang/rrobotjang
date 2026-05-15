#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIDS=()
NGINX_PID=""

cleanup() {
  echo "Shutting down local stack..."
  for pid in "${PIDS[@]:-}"; do
    if kill -0 "$pid" 2>/dev/null; then
      kill "$pid" || true
    fi
  done

  if [[ -n "${NGINX_PID:-}" ]] && kill -0 "$NGINX_PID" 2>/dev/null; then
    kill "$NGINX_PID" || true
  fi
}
trap cleanup EXIT INT TERM

start_service() {
  local name="$1"
  echo "Starting ${name}..."
  (cd "$ROOT_DIR/services/$name" && gradle bootRun) > "$ROOT_DIR/.${name}.log" 2>&1 &
  PIDS+=("$!")
}

start_service auth-service
start_service user-profile-service
start_service api-gateway

if command -v nginx >/dev/null 2>&1; then
  echo "Starting nginx on :8090 using infra/nginx/nginx.conf"
  nginx -c "$ROOT_DIR/infra/nginx/nginx.conf" -p "$ROOT_DIR" -g 'daemon off;' > "$ROOT_DIR/.nginx.log" 2>&1 &
  NGINX_PID="$!"
else
  echo "nginx not found. Install nginx to enable reverse proxy on :8090"
fi

echo "Local stack running."
echo "- API Gateway UI: http://localhost:8080/"
echo "- NGINX entrypoint: http://localhost:8090/"
echo "Press Ctrl+C to stop."

wait
