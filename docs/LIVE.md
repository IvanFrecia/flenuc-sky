# Live deployment

## Current production (interim host)

| Item | Value |
|------|--------|
| Service | `sky-portfolio` |
| Project | `skylabs-devops` (GCP project id; interim host with billing) |
| Target project | `flenuc-sky` (created; **billing blocked by 5-project quota**) |
| Region | `us-central1` |
| URL | https://sky-portfolio-6k4smyyquq-uc.a.run.app |
| Alt URL | https://sky-portfolio-125699337180.us-central1.run.app |
| Mode | `DEMO_MODE=true` (rewards demo ledger; Stripe optional) |
| Domain | Pending Hostinger DNS → see DOMAIN_HOSTINGER.md |

## GitHub
- Portfolio (private): https://github.com/IvanFrecia/flenuc-sky
- Sky Colab OSS: https://github.com/IvanFrecia/sky-colab

## Migrate to flenuc-sky when billing links
1. Resolve docs/BILLING_QUOTA.md
2. `./infra/scripts/bootstrap-infra.sh`
3. Deploy with `PROJECT=flenuc-sky ./infra/scripts/deploy-stg.sh` then prod
4. Remap domain
