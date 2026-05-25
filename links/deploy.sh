#!/usr/bin/env bash
# Deploy do LinkStack do CPA no Docker Swarm.
#
# Rodar no manager. Lê .env na mesma pasta.
#
# Usage:
#   bash deploy.sh

set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo ".env missing — copie .env.example e preencha." >&2
  exit 1
fi
set -a; source .env; set +a

STACK_NAME="${STACK_NAME:-cpa-links}"

echo "→ docker stack deploy (${STACK_NAME})"
docker stack deploy --with-registry-auth -c docker-compose.yml "$STACK_NAME"

echo "✓ Deployed."
echo "Wizard de install: https://${LINKS_HOST}"
