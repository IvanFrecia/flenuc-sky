#!/usr/bin/env bash
# Deploy flenuc-sky portfolio service to Cloud Run (staging).
# Prerequisites: gcloud authenticated; project flenuc-sky exists; APIs enabled.
# Does NOT create the GCP project (infra agent owns that).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROJECT_ID="${PROJECT_ID:-flenuc-sky}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-flenuc-sky-web}"
IMAGE="${IMAGE:-gcr.io/${PROJECT_ID}/${SERVICE}:stg}"
PUBLIC_BASE_URL="${PUBLIC_BASE_URL:-https://${SERVICE}-PLACEHOLDER.run.app}"

echo "==> Project: ${PROJECT_ID}  Region: ${REGION}  Service: ${SERVICE}"
echo "==> Root: ${ROOT}"

gcloud config set project "${PROJECT_ID}"

echo "==> Building image ${IMAGE}"
gcloud builds submit "${ROOT}" --tag "${IMAGE}"

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
  --set-env-vars "ENV=production,LEDGER_PATH=/tmp/flenuc-sky-ledger.json" \
  --quiet

SERVICE_URL="$(gcloud run services describe "${SERVICE}" --region "${REGION}" --format='value(status.url)')"
echo "==> Service URL: ${SERVICE_URL}"

# Optionally update PUBLIC_BASE_URL for OG / Stripe redirects
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
