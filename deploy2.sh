#!/usr/bin/env bash
#
# deploy2.sh — build the production image ON the server, then migrate & restart.
#
# Model: the server ALREADY has its own docker-compose.prod.yml (defining app, db,
# redis) pointing the app service at this image. We do NOT ship a compose file
# from here. This script:
#   1. builds a fresh app image on the server's Docker daemon (remote context)
#   2. over SSH on the server: applies migrations and recreates the app container
#
# `docker --context <ctx> build` runs the build on the REMOTE daemon, so the image
# is produced with the server's native architecture (amd64) — no emulation, no
# registry, no image transfer.
#
# One-time setup on the operator machine:
#   ssh-copy-id -p 2222 al@funding.wiki
#   docker context create fundingwiki-prod --docker "host=ssh://al@funding.wiki:2222"
#
# Usage:
#   ./deploy2.sh
#   IMAGE_TAG="$(git rev-parse --short HEAD)" ./deploy2.sh

set -euo pipefail

CONTEXT="${DOCKER_CONTEXT:-fundingwiki-prod}"
IMAGE_NAME="${IMAGE_NAME:-fundingwiki-app}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

# Used by the migrate/restart step below (SSH onto the server).
REMOTE_SSH="${REMOTE_SSH:-al@funding.wiki}"
SSH_PORT="${SSH_PORT:-2222}"
REMOTE_DIR="${REMOTE_DIR:-/home/al/espacio_de_trabajo/fundingwiki}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"

cd "$(dirname "$0")"

# 0. Preconditions ----------------------------------------------------------
if ! docker context inspect "$CONTEXT" >/dev/null 2>&1; then
    echo "ERROR: docker context '$CONTEXT' not found. Create it once with:" >&2
    echo "  docker context create $CONTEXT --docker \"host=ssh://$REMOTE_SSH:$SSH_PORT\"" >&2
    exit 1
fi

# 1. Build the image on the server's daemon ---------------------------------
echo "=== Building $IMAGE_NAME:$IMAGE_TAG on context '$CONTEXT' (server-side, native arch) ==="
# BuildKit's gRPC session breaks over an SSH docker context ("failed to list
# workers / file already closed"), so use the legacy builder, which builds
# straight through the daemon API. It streams full plain output by default.
DOCKER_BUILDKIT=0 docker --context "$CONTEXT" build -t "$IMAGE_NAME:$IMAGE_TAG" -f Dockerfile .

echo "=== Build complete. Image is on the server's daemon: ==="
docker --context "$CONTEXT" image ls "$IMAGE_NAME"

# 2. Migrate + restart on the server --------------------------------------
# The compose file lives on the server (it references $IMAGE_NAME:$IMAGE_TAG),
# so we drive it over plain SSH (not the remote context). db/redis are brought
# up first so migrate has something to connect to, then the app is recreated
# with the freshly built image.
echo "=== Migrating + restarting app on $REMOTE_SSH ==="
ssh -p "$SSH_PORT" "$REMOTE_SSH" "cd '$REMOTE_DIR' && \
    docker compose -f '$COMPOSE_FILE' up -d db redis && \
    docker compose -f '$COMPOSE_FILE' run --rm app python manage.py migrate --noinput && \
    docker compose -f '$COMPOSE_FILE' up -d app"

echo "=== Deploy complete ==="
ssh -p "$SSH_PORT" "$REMOTE_SSH" "cd '$REMOTE_DIR' && docker compose -f '$COMPOSE_FILE' ps"
