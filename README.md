# flenuc-sky — Ivan Frecia portfolio

[![CI](https://github.com/IvanFrecia/flenuc-sky/actions/workflows/ci.yml/badge.svg)](https://github.com/IvanFrecia/flenuc-sky/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Live](https://img.shields.io/badge/Cloud%20Run-live-success)](https://sky-portfolio-6k4smyyquq-uc.a.run.app)

**Ivan Frecia** — personal portfolio site, rewards campaign (demo), KPI dashboard, and legal pages.  
Single **FastAPI** service, **Cloud Run** ready. Apache-2.0.

> Rewards are **not equity/securities**. **No guaranteed profit** / **no assured ROI**.

| | |
|--|--|
| **Live** | https://sky-portfolio-6k4smyyquq-uc.a.run.app |
| **Owner** | Ivan Frecia |
| **Contact** | freciaivan@gmail.com |
| **Related OSS** | [Sky Colab](https://github.com/IvanFrecia/sky-colab) |

## Quick start (local)

```bash
git clone https://github.com/IvanFrecia/flenuc-sky.git
cd flenuc-sky
chmod +x infra/scripts/*.sh
make local
# → http://localhost:8080
```

Or:

```bash
cd apps/portfolio
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Desktop access (Linux)

After install on the maintainer machine:

| Icon | Action |
|------|--------|
| **Ivan Portfolio** | Opens the live Cloud Run site |
| **Task Development** | Opens active Sky Colab task + transparency UI |
| **Sky Colab** | Multi-model collab board (`duo ui`) |

```bash
# CLI launchers (PATH)
portfolio-launcher live    # production URL
portfolio-launcher local   # start run-local.sh + browser
task-dev-launcher          # active duo task + UI
```

## Routes

| Path | Description |
|------|-------------|
| `/` | Hero — Ivan Frecia · multi-model systems |
| `/about` | About |
| `/work` | Project cards (public OSS) |
| `/sky-colab` | Product page → github.com/IvanFrecia/sky-colab |
| `/fund` | Rewards campaign, tiers, ledger |
| `/kpi` | Metrics + disclaimer banner |
| `/contact` | Contact |
| `/legal/*` | Privacy, terms, rewards, risk, refunds |
| `/api/health` | Health check |
| `/api/fund/*` | Campaign, ledger, demo pledge, Stripe |
| `/api/kpi/snapshot` | KPI JSON |

## Demo pledges

With `STRIPE_SECRET_KEY` unset, the Fund page uses **demo mode**:

```bash
curl -s -X POST http://localhost:8080/api/fund/demo-pledge \
  -H 'Content-Type: application/json' \
  -d '{"tier_id":"supporter","display_name":"Ada","public":true}'
```

## Docker

```bash
docker build -t flenuc-sky .
docker run --rm -p 8080:8080 -e PORT=8080 flenuc-sky
curl -s http://localhost:8080/api/health
```

## Cloud Run deploy

```bash
# Live interim host (default) — service sky-portfolio
make deploy
# or
./infra/scripts/deploy-stg.sh

# Dedicated project (when billing is linked)
PROJECT_ID=flenuc-sky SERVICE=flenuc-sky-web ./infra/scripts/deploy-stg.sh
```

| Item | Value |
|------|--------|
| Service | `sky-portfolio` |
| Region | `us-central1` |
| Health | `/api/health` |
| Mode | Demo ledger when Stripe unset |

GitHub Actions: **CI** on every PR; **Deploy Cloud Run** via `workflow_dispatch` (optional Workload Identity secrets).

## Repo layout

```
flenuc-sky/
  apps/portfolio/     # deployable FastAPI app
  packages/legal/     # markdown legal sources
  infra/scripts/      # run-local + deploy
  docs/               # ops notes
  .github/            # CI, PR/issue templates
  Dockerfile
  Makefile
  README.md
```

## Open-source docs

- [CONTRIBUTING.md](CONTRIBUTING.md)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- [SECURITY.md](SECURITY.md)
- [CHANGELOG.md](CHANGELOG.md)
- [LICENSE](LICENSE) (Apache-2.0)

## Contact

**freciaivan@gmail.com**  
© 2026 Ivan Frecia
