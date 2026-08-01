# Personal rebrand complete — Ivan Frecia portfolio

**Date:** 2026-08-01  
**Scope:** Remove all **SkyLabs Developments** / company marketing brand from this personal portfolio.  
**Operator:** Ivan Frecia (individual)  
**Public contact:** `freciaivan@gmail.com`

## Summary

This repo is now framed as **Ivan Frecia’s personal portfolio**, not a corporate SkyLabs Developments site. Product name **Sky Colab** is kept as personal OSS. GCP project IDs and technical domain ops remain as infrastructure identifiers only.

## Rebrand map applied

| Old | New |
|-----|-----|
| SkyLabs Developments | removed / Ivan Frecia (individual) |
| SkyLabs (company) | omitted or “personal portfolio” |
| `site_name` “Ivan Frecia · SkyLabs” | `Ivan Frecia` |
| SkyLabs Rewards Campaign / Sprint | `Ivan Frecia · 5-Day Rewards Sprint` |
| Contact brand SkyLabs | Ivan Frecia · `freciaivan@gmail.com` |
| Footer brand | Ivan Frecia · personal portfolio |
| Copyright | © 2026 Ivan Frecia |
| Campaign id `skylabs-rewards-5d-202608` | `ivan-frecia-rewards-5d-202608` |
| Social company LinkedIn / `@SkyLabsDev` | personal only (`@IvanFrecia`, LinkedIn personal) |
| Legal party SkyLabs Developments | Ivan Frecia (individual) |

## Files changed

### App config & services
- `apps/portfolio/app/config.py` — contact email + site_name
- `apps/portfolio/app/main.py` — FastAPI title
- `apps/portfolio/app/__init__.py` — package docstring
- `apps/portfolio/app/routers/pages.py` — all page titles / descriptions
- `apps/portfolio/app/services/fund.py` — campaign id + title
- `apps/portfolio/app/services/social.py` — default social links / email / X handle
- `apps/portfolio/app/services/stripe_service.py` — Stripe line-item name
- `apps/portfolio/app/services/kpi.py` — host label (no company project name in UI)
- `apps/portfolio/app/data/social.json` — personal links; no company page strategy
- `apps/portfolio/data/ledger.json` — campaign_id

### Templates (UI-facing)
- `apps/portfolio/app/templates/partials/nav.html` — brand-sub → “Portfolio”
- `apps/portfolio/app/templates/partials/footer.html` — personal portfolio + © Ivan Frecia
- `apps/portfolio/app/templates/home.html`
- `apps/portfolio/app/templates/about.html`
- `apps/portfolio/app/templates/sky_colab.html`
- `apps/portfolio/app/templates/contact.html`
- `apps/portfolio/app/templates/legal/page.html`

### Legal (operator = individual)
- `packages/legal/{privacy,terms,rewards,risk,refunds}.md`
- `apps/portfolio/app/legal_md/*` (synced from packages/legal)

### Content & docs
- `content/social/HANDLES_AND_CALENDAR.md` — personal-only strategy
- `content/social/LAUNCH_KIT.md`
- `README.md`
- `docs/overview.md`
- `docs/DOMAIN_HOSTINGER.md` — reframed as “domain you own”, not org site
- `docs/BILLING_QUOTA.md` — GCP ids labeled technical
- `docs/LIVE.md` — project id note
- `.env.example` — optional CONTACT_EMAIL / SITE_NAME
- `infra/scripts/bootstrap-infra.sh` — comment: GCP login ≠ public contact

### Intentionally unchanged (or historical)
- **Sky Colab** product name everywhere
- `github.com/IvanFrecia` and project repo names
- GCP project IDs (`skylabs-devops`, etc.) as technical infra
- Domain hostname strings in DOMAIN_HOSTINGER for DNS ops (reframed as owned domain)
- Default gcloud `ACCOUNT` in bootstrap (technical login; documented)
- `docs/AUDIT_PERSONAL_BRAND.md` — historical pre-fix audit inventory (not UI copy)

## Verification

### Zero org brand in product surfaces
```
apps/     — no "SkyLabs Developments", no marketing "SkyLabs", no ifrecia@skylabs
packages/ — clean
content/  — clean
README.md — clean
```

### Remaining `skylabs*` (acceptable technical only)
| Location | Why kept |
|----------|----------|
| `docs/DOMAIN_HOSTINGER.md` | Domain you own + DNS/gcloud commands |
| `docs/BILLING_QUOTA.md` / `docs/LIVE.md` | GCP project id `skylabs-devops` |
| `infra/scripts/bootstrap-infra.sh` | Technical GCP account email default |
| `docs/AUDIT_PERSONAL_BRAND.md` | Pre-rebrand audit report |

### Python smoke check (venv present)
```
site_name: Ivan Frecia
contact_email: freciaivan@gmail.com
campaign_id: ivan-frecia-rewards-5d-202608
campaign_title: Ivan Frecia · 5-Day Rewards Sprint
social_email: freciaivan@gmail.com
social_x: @IvanFrecia
OK: imports and brand checks passed
```

## Deploy notes
- Redeploy Cloud Run so live HTML/legal pick up changes.
- If a local ledger still has the old `campaign_id`, new writes use `ivan-frecia-rewards-5d-202608` (repo `ledger.json` already updated).
- Public primary URL remains the `*.run.app` service until personal domain strategy is intentional.
