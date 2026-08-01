#!/usr/bin/env bash
set -euo pipefail
PROJECT="${PROJECT:-flenuc-sky}"
REGION="${REGION:-us-central1}"
# Technical GCP login (not public portfolio contact; public = freciaivan@gmail.com)
ACCOUNT="${ACCOUNT:-}"
# Never commit real billing account IDs — pass BILLING=XXXXXX-XXXXXX-XXXXXX
BILLING="${BILLING:-}"

if [[ -n "${ACCOUNT}" ]]; then
  gcloud config set account "$ACCOUNT"
fi
gcloud config set project "$PROJECT"
gcloud config set run/region "$REGION"

# Link billing (fails if quota full)
if [[ -z "${BILLING}" ]]; then
  echo "Set BILLING=ACCOUNT_ID to link billing (see docs/BILLING_QUOTA.md)" >&2
  echo "Continuing without billing link…" >&2
else
  gcloud billing projects link "$PROJECT" --billing-account="$BILLING" || {
    echo "Billing link failed — see docs/BILLING_QUOTA.md" >&2
    exit 1
  }
fi

gcloud services enable \
  run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com \
  secretmanager.googleapis.com cloudscheduler.googleapis.com logging.googleapis.com \
  monitoring.googleapis.com iam.googleapis.com cloudresourcemanager.googleapis.com \
  storage.googleapis.com firestore.googleapis.com compute.googleapis.com

gcloud artifacts repositories create sky \
  --repository-format=docker --location="$REGION" \
  --description="Flenuc Sky container images" 2>/dev/null || true

gcloud iam service-accounts create sky-portfolio-run \
  --display-name="Sky Portfolio Cloud Run" 2>/dev/null || true

SA="sky-portfolio-run@${PROJECT}.iam.gserviceaccount.com"
# minimal runtime roles
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${SA}" \
  --role="roles/logging.logWriter" --condition=None >/dev/null
gcloud projects add-iam-policy-binding "$PROJECT" \
  --member="serviceAccount:${SA}" \
  --role="roles/secretmanager.secretAccessor" --condition=None >/dev/null || true

# Budget $50 (best-effort; API shape varies)
echo "Create budget in console if CLI unavailable: $50/month on $PROJECT"
echo "Bootstrap complete for $PROJECT"
