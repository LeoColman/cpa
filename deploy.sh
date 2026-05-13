#!/usr/bin/env bash
# Build + roll out o site do CPA no Docker Swarm.
#
# Rodar no manager. Lê .env na raiz do repo.
#
# Usage:
#   bash deploy.sh           # build + docker stack deploy (full reapply)
#   bash deploy.sh rebuild   # só rebuilda a imagem + service update
#
# Env vars:
#   STACK_NAME   default cpa
#   IMAGE_TAG    default latest

set -euo pipefail
cd "$(dirname "$0")"

export DOCKER_BUILDKIT=1

if [[ ! -f .env ]]; then
  echo ".env missing — copie .env.example e preencha os valores." >&2
  exit 1
fi
set -a; source .env; set +a

STACK_NAME="${STACK_NAME:-cpa}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "→ build cpa-site:${IMAGE_TAG}"
docker build -t "cpa-site:${IMAGE_TAG}" .

echo "→ docker stack deploy (${STACK_NAME})"
export IMAGE_TAG
set +e
docker stack deploy --with-registry-auth -c docker-compose.yml "$STACK_NAME" 2>&1 \
  | tee /tmp/stack-deploy-cpa.log \
  | grep -E "Updating|Creating|error|Error" | head -20
stack_rc=${PIPESTATUS[0]}
set -e
if [[ $stack_rc -ne 0 ]]; then
  echo "⚠ stack deploy retornou $stack_rc (non-fatal). Seguindo com service update."
  echo "   Log: /tmp/stack-deploy-cpa.log"
fi

echo "→ docker service update --force ${STACK_NAME}_site"
docker service update --force --image "cpa-site:${IMAGE_TAG}" "${STACK_NAME}_site" >/dev/null

echo "✓ Deployed."
