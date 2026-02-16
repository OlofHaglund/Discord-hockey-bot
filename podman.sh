#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="discord-hockey-bot"
ENV_FILE=".env"

usage() {
  cat <<'USAGE'
Usage: ./podman.sh [build|run]

build  Build the Podman image
run    Run the container using .env for DISCORD_TOKEN
USAGE
}

case "${1:-}" in
  build)
    podman build -t "$IMAGE_NAME" .
    ;;
  run)
    if [[ ! -f "$ENV_FILE" ]]; then
      echo "Missing $ENV_FILE. Copy .env.example to .env and set DISCORD_TOKEN." >&2
      exit 1
    fi
    running_ids="$(podman ps --filter ancestor=localhost/discord-hockey-bot:latest --format '{{.ID}}')"
    if [[ -n "$running_ids" ]]; then
      echo "Stopping existing bot containers: $running_ids"
      podman stop $running_ids >/dev/null
    fi
    mkdir -p data
    podman run --rm --env-file "$ENV_FILE" -v "$(pwd)/data:/app/data:Z" "$IMAGE_NAME"
    ;;
  *)
    usage
    exit 1
    ;;
 esac
