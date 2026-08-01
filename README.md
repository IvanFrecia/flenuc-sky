# Flenuc Sky

**Ivan Frecia · SkyLabs Developments** — portfolio site, rewards campaign, KPI dashboard, and legal pages. Single FastAPI service, Cloud Run ready.

> Rewards are **not equity/securities**. **No guaranteed profit** / **no assured ROI**.

## Quick start (local)

```bash
cd /home/skye/Projects/flenuc-sky
chmod +x infra/scripts/*.sh
./infra/scripts/run-local.sh
# → http://localhost:8080
```

Or manually:

```bash
cd apps/portfolio
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
export PORT=8080
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Routes

| Path | Description |
|------|-------------|
| `/` | Hero — Ivan Frecia · SkyLabs · multi-model systems |
| `/about` | About |
| `/work` | Project cards (pending approval #1–3) |
| `/sky-colab` | Product page → github.com/IvanFrecia/sky-colab |
| `/fund` | Rewards campaign, tiers, ledger |
| `/kpi` | Metrics + disclaimer banner |
| `/contact` | Contact |
| `/legal/*` | Privacy, terms, rewards, risk, refunds |
| `/api/health` | Health check |
| `/api/fund/campaign` | Campaign JSON |
| `/api/fund/ledger` | Public ledger |
| `/api/fund/demo-pledge` | POST demo pledge (no Stripe) |
| `/api/fund/checkout` | Stripe Checkout session (when configured) |
| `/api/fund/webhook` | Stripe webhook |
| `/api/kpi/snapshot` | KPI JSON |

## Demo pledges

With `STRIPE_SECRET_KEY` unset, the Fund page uses **demo mode**:

```bash
curl -s -X POST http://localhost:8080/api/fund/demo-pledge \
  -H 'Content-Type: application/json' \
  -d '{"tier_id":"supporter","display_name":"Ada","public":true}'
```

Ledger file: `apps/portfolio/data/ledger.json` (local) or `/tmp/flenuc-sky-ledger.json` (production/Cloud Run).

## Stripe (optional)

```bash
export STRIPE_SECRET_KEY=sk_test_...
export STRIPE_WEBHOOK_SECRET=whsec_...
export STRIPE_PUBLISHABLE_KEY=pk_test_...
export PUBLIC_BASE_URL=https://your-domain.example
```

## Docker

```bash
# from repo root
docker build -t flenuc-sky .
docker run --rm -p 8080:8080 -e PORT=8080 flenuc-sky
curl -s http://localhost:8080/api/health
```

## Cloud Run (staging)

```bash
# Requires: gcloud auth, project `flenuc-sky` already created, APIs enabled
./infra/scripts/deploy-stg.sh
```

- Project: `flenuc-sky`  
- Region: `us-central1`  
- Health: `/api/health`  
- Listens on `PORT` (default 8080)

## Repo layout

```
flenuc-sky/
  apps/portfolio/     # deployable FastAPI app
  packages/legal/     # markdown legal sources
  infra/scripts/      # run-local + deploy-stg
  docs/
  Dockerfile
  README.md
```

## Contact

**ifrecia@skylabs-developments.tech**  
© 2026 Ivan Frecia / SkyLabs Developments
