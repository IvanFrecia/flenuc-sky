#!/usr/bin/env bash
# Deploy flenuc-sky portfolio service to Cloud Run.
#
# Defaults target the *live interim* host (billing-linked project) used for
# the public portfolio. Override env vars for the dedicated flenuc-sky project
# once billing is linked (see docs/BILLING_QUOTA.md).
#
# Examples:
#   ./infra/scripts/deploy-stg.sh
#   PROJECT_ID=flenuc-sky SERVICE=flenuc-sky-web ./infra/scripts/deploy-stg.sh
#
# Prerequisites: gcloud authenticated; Cloud Run + Cloud Build APIs enabled.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
# Live portfolio defaults (interim host with billing)
PROJECT_ID="${PROJECT_ID:-skylabs-devops}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-sky-portfolio}"
TAG="${TAG:-$(git -C "${ROOT}" rev-parse --short HEAD 2>/dev/null || echo stg)}"
IMAGE="${IMAGE:-gcr.io/${PROJECT_ID}/${SERVICE}:${TAG}}"
DEMO_MODE="${DEMO_MODE:-true}"

echo "==> Project: ${PROJECT_ID}  Region: ${REGION}  Service: ${SERVICE}"
echo "==> Image:  ${IMAGE}"
echo "==> Root:   ${ROOT}"

gcloud config set project "${PROJECT_ID}"

echo "==> Building image ${IMAGE}"
gcloud builds submit "${ROOT}" --tag "${IMAGE}"

ENV_VARS="ENV=production,LEDGER_PATH=/tmp/flenuc-sky-ledger.json,DEMO_MODE=${DEMO_MODE}"

echo "==> Deploying Cloud Run service"
gcloud run deploy "${SERVICE}" \
  --image "${IMAGE}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 5 \
  --set-env-vars "${ENV_VARS}" \
  --labels "app=sky-portfolio,owner=ivan-frecia,product=portfolio" \
  --quiet

SERVICE_URL="$(gcloud run services describe "${SERVICE}" --region "${REGION}" --format='value(status.url)')"
echo "==> Service URL: ${SERVICE_URL}"

if [[ "${UPDATE_PUBLIC_URL:-1}" == "1" ]]; then
  echo "==> Setting PUBLIC_BASE_URL=${SERVICE_URL}"
  gcloud run services update "${SERVICE}" \
    --region "${REGION}" \
    --update-env-vars "PUBLIC_BASE_URL=${SERVICE_URL}" \
    --quiet
fi

echo "==> Health check"
curl -sfS "${SERVICE_URL}/api/health" | head -c 500 || true
echo
echo "Done. Visit ${SERVICE_URL}"
