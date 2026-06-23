#!/usr/bin/env bash
#
# deploy2.sh — build the production image ON the server, then (optionally) restart.
#
# Model: the server ALREADY has its own docker-compose.prod.yml (defining app, db,
# redis). We do NOT ship a compose file from here. This script only builds a fresh
# app image on the server's Docker daemon (via a remote Docker context). You then
# point the app service's `image:` at the tag below and recreate the app container.
#
# `docker --context <ctx> build` runs the build on the REMOTE daemon, so the image
# is produced with the server's native architecture (amd64) — no emulation, no
# registry, no image transfer.
#
# >>> The deploy/restart step (2) is COMMENTED OUT on purpose. <<<
# This version is for testing the IMAGE BUILD only.
#
# One-time setup on the operator machine:
#   ssh-copy-id -p 2222 root@funding.wiki
#   docker context create fundingwiki-prod --docker "host=ssh://root@funding.wiki:2222"
#
# Usage:
#   ./deploy2.sh
#   IMAGE_TAG="$(git rev-parse --short HEAD)" ./deploy2.sh

set -euo pipefail

CONTEXT="${DOCKER_CONTEXT:-fundingwiki-prod}"
IMAGE_NAME="${IMAGE_NAME:-fundingwiki-app}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

# Used only by the (commented) restart step below.
REMOTE_SSH="${REMOTE_SSH:-root@funding.wiki}"
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
docker --context "$CONTEXT" build --progress=plain -t "$IMAGE_NAME:$IMAGE_TAG" -f Dockerfile .

echo "=== Build complete. Image is on the server's daemon: ==="
docker --context "$CONTEXT" image ls "$IMAGE_NAME"

# 2. Deploy / restart  --  DISABLED FOR NOW ---------------------------------
# Once the server's $COMPOSE_FILE points the app service at
# "image: $IMAGE_NAME:$IMAGE_TAG", uncomment the block below to migrate and
# recreate the app container with the freshly built image. The compose file
# lives on the server, so we drive it over plain SSH (not the remote context).
#
# echo "=== Migrating + restarting app on $REMOTE_SSH ==="
# ssh -p "$SSH_PORT" "$REMOTE_SSH" "cd '$REMOTE_DIR' && \
#     docker compose -f '$COMPOSE_FILE' run --rm app python manage.py migrate --noinput && \
#     docker compose -f '$COMPOSE_FILE' up -d app"
#
# echo "=== Deploy complete ==="
# ssh -p "$SSH_PORT" "$REMOTE_SSH" "cd '$REMOTE_DIR' && docker compose -f '$COMPOSE_FILE' ps"

echo "(deploy/restart step is commented out — build-only run)"
