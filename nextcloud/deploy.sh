#!/usr/bin/env bash
# Deploy Nextcloud do CPA no Docker Swarm.
#
# Rodar no manager. Lê .env na mesma pasta.
#
# Usage:
#   bash deploy.sh

set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo ".env missing — copie .env.example e preencha os valores." >&2
  exit 1
fi
set -a; source .env; set +a

STACK_NAME="${STACK_NAME:-nextcloud}"

echo "→ docker stack deploy (${STACK_NAME})"
docker stack deploy --with-registry-auth -c docker-compose.yml "$STACK_NAME"

echo "✓ Deployed."
