#!/bin/bash
# Deploy project to Raspberry Pi over SSH
# Usage: ./deploy.sh [--restart]
#
# Configure connection in .deploy.env (copy from .deploy.env.example)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.deploy.env"

# ── Load config ────────────────────────────────────────────────────────────────
if [[ ! -f "$ENV_FILE" ]]; then
    echo "Error: $ENV_FILE not found."
    echo "Copy .deploy.env.example to .deploy.env and fill in your Pi's details."
    exit 1
fi

# shellcheck source=/dev/null
source "$ENV_FILE"

RPI_HOST="${RPI_HOST:?RPI_HOST is not set in .deploy.env}"
RPI_USER="${RPI_USER:?RPI_USER is not set in .deploy.env}"
RPI_PORT="${RPI_PORT:-22}"
REMOTE_DIR="${REMOTE_DIR:-~/flame_detector}"
SERVICE_NAME="${SERVICE_NAME:-flame-detector}"

# ── Parse args ─────────────────────────────────────────────────────────────────
RESTART=false
for arg in "$@"; do
    case $arg in
        --restart) RESTART=true ;;
        *) echo "Unknown option: $arg"; exit 1 ;;
    esac
done

# ── Deploy ─────────────────────────────────────────────────────────────────────
echo "Deploying to ${RPI_USER}@${RPI_HOST}:${REMOTE_DIR} ..."

rsync -avz --progress \
    -e "ssh -p ${RPI_PORT}" \
    --exclude='.git/' \
    --exclude='.deploy.env' \
    --exclude='__pycache__/' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='*.log' \
    "$SCRIPT_DIR/" \
    "${RPI_USER}@${RPI_HOST}:${REMOTE_DIR}/"

echo "Sync complete."

# ── Restart service (optional) ─────────────────────────────────────────────────
if [[ "$RESTART" == true ]]; then
    echo "Restarting ${SERVICE_NAME} service on Pi..."
    ssh -p "${RPI_PORT}" "${RPI_USER}@${RPI_HOST}" \
        "sudo systemctl restart ${SERVICE_NAME} && sudo systemctl status ${SERVICE_NAME} --no-pager"
    echo "Service restarted."
fi

echo "Done."
