# Billing quota blocker — flenuc-sky

## Status
- Project `flenuc-sky` (**276614846326**) created under org skylabs-developments.tech
- Link to billing account `013E4C-2C3967-D5AD20` (skylabs) **FAILED**: Cloud billing **project quota exceeded**
- Currently billed projects (5):
  1. skylabs-devops
  2. molisud-cereales-pro
  3. moli-pwa-production
  4. teckers-final
  5. molisud-aceptacion

Self-serve Google Cloud billing accounts often cap at **5 projects** with billing enabled.

## Unblock options (pick one)

### A) Request quota increase (preferred if all 5 are needed)
https://support.google.com/code/contact/billing_quota_increase

### B) Unlink billing from one non-critical project
**Requires your explicit approval** — unlinking stops paid APIs on that project.

```bash
# Example only after you name the project to free:
# gcloud billing projects unlink PROJECT_ID
gcloud billing projects link flenuc-sky --billing-account=013E4C-2C3967-D5AD20
```

### C) Temporary deploy into skylabs-devops
Deploy service `sky-portfolio` there with labels `app=sky-portfolio,owner=ivan-frecia` until flenuc-sky has billing.

## After billing links

```bash
gcloud config set project flenuc-sky
gcloud services enable run.googleapis.com cloudbuild.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com \
  cloudscheduler.googleapis.com logging.googleapis.com monitoring.googleapis.com \
  firestore.googleapis.com storage.googleapis.com iam.googleapis.com
# then ./infra/scripts/bootstrap-infra.sh && ./infra/scripts/deploy-stg.sh
```
