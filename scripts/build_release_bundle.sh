#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

mkdir -p "$DIST_DIR"
rm -f "$DIST_DIR"/flight-ai-backend.zip "$DIST_DIR"/flight-ai-frontend.tar.gz

(
  cd "$BACKEND_DIR"
  zip -r "$DIST_DIR/flight-ai-backend.zip" app requirements.txt Dockerfile >/dev/null
)

(
  cd "$FRONTEND_DIR"
  tar -czf "$DIST_DIR/flight-ai-frontend.tar.gz" Dockerfile package.json src
)

echo "Release bundle created in $DIST_DIR"
ls -lh "$DIST_DIR"
