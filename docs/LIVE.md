# Live deployment

## Current production (interim host)

| Item | Value |
|------|--------|
| Service | `sky-portfolio` |
| Project | interim GCP project with billing (see deploy defaults) |
| Target project | `flenuc-sky` (created; billing blocked by project quota) |
| Region | `us-central1` |
| URL | https://sky-portfolio-6k4smyyquq-uc.a.run.app |
| Alt URL | https://sky-portfolio-125699337180.us-central1.run.app |
| Mode | Demo ledger when Stripe unset |
| Domain | Pending custom DNS → see DOMAIN_HOSTINGER.md |

## GitHub

- Portfolio (public OSS): https://github.com/IvanFrecia/flenuc-sky
- Sky Colab OSS: https://github.com/IvanFrecia/sky-colab

## Deploy

```bash
# Defaults: live service sky-portfolio on interim host
make deploy
# or
./infra/scripts/deploy-stg.sh
```

## Migrate to flenuc-sky when billing links

1. Resolve docs/BILLING_QUOTA.md (operator notes; may contain internal IDs)
2. `./infra/scripts/bootstrap-infra.sh` (requires `BILLING` env)
3. `PROJECT_ID=flenuc-sky SERVICE=flenuc-sky-web ./infra/scripts/deploy-stg.sh`
4. Remap domain
