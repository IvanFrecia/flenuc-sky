# Domain: skylabs-developments.com (Hostinger → Cloud Run)

## Prerequisites
- Project `flenuc-sky` with **billing linked**
- Cloud Run service `sky-portfolio` (prod) deployed in `us-central1`
- Access to Hostinger DNS for `skylabs-developments.com`

## 1. Map domain on GCP

```bash
gcloud config set project flenuc-sky
gcloud config set account ifrecia@skylabs-developments.tech

# Modern approach: domain mapping / load balancer
# Cloud Run domain mappings (beta may vary by account):
gcloud beta run domain-mappings create \
  --service=sky-portfolio \
  --domain=skylabs-developments.com \
  --region=us-central1

# Optional www
gcloud beta run domain-mappings create \
  --service=sky-portfolio \
  --domain=www.skylabs-developments.com \
  --region=us-central1
```

Then list required DNS records:

```bash
gcloud beta run domain-mappings describe \
  --domain=skylabs-developments.com \
  --region=us-central1
```

## 2. Hostinger DNS (paste values from describe)

Typical records (confirm against `describe` output):

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A or AAAA | @ | (Google values) | 300 |
| CNAME | www | ghs.googlehosted.com. | 300 |

Or CNAME for subdomain-only if apex not supported by your plan.

## 3. Verify

```bash
curl -I https://skylabs-developments.com/api/health
```

Wait for Google-managed certificate (can take 15–60 min after DNS propagates).

## Interim URL

Until DNS is ready, use the `*.run.app` URL printed by `gcloud run services describe sky-portfolio`.
