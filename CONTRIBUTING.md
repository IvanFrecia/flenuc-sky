# Contributing to flenuc-sky

Thanks for helping improve **Ivan Frecia’s personal portfolio** (FastAPI + Cloud Run).

## Ground rules

1. This is a **personal portfolio** for **Ivan Frecia** — not a company marketing site.
2. Prefer small, reviewable diffs.
3. **No secrets** in commits, issues, or sample data (Stripe keys, service accounts, billing IDs).
4. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
5. Legal copy under `packages/legal/` is source of truth; keep disclaimers (no equity, no guaranteed ROI).

## Development setup

```bash
git clone https://github.com/IvanFrecia/flenuc-sky.git
cd flenuc-sky
chmod +x infra/scripts/*.sh
./infra/scripts/run-local.sh
# → http://localhost:8080
```

Requirements: Python 3.11+ (3.12 recommended), optional Docker, optional `gcloud` for deploy.

```bash
# Docker smoke
docker build -t flenuc-sky .
docker run --rm -p 8080:8080 -e PORT=8080 flenuc-sky
curl -sfS http://localhost:8080/api/health
```

## Project layout

```
apps/portfolio/     # deployable FastAPI app
packages/legal/     # markdown legal sources
infra/scripts/      # run-local, deploy-*, bootstrap
docs/               # ops + brand notes
Dockerfile          # Cloud Run image
```

## How to contribute

1. Fork and branch from `main` (`feat/…`, `fix/…`, `docs/…`).
2. Keep style consistent with nearby code (type hints, small modules).
3. Smoke-test:
   - `./infra/scripts/run-local.sh` and hit `/` + `/api/health`
   - or `python -m pytest` if tests are present
4. Open a PR with: **what / why / how tested**.

## Coding notes

- Settings via `pydantic-settings` + env (see `.env.example`).
- Demo fund mode when `STRIPE_SECRET_KEY` is unset.
- Cloud Run listens on `PORT` (default 8080); ledger defaults to `/tmp` in production.
- Do not reintroduce third-party company branding into UI copy.

## License of contributions

By submitting a pull request, you agree that your contribution is licensed under the **Apache License 2.0**, and that you have the right to license it under those terms. See [LICENSE](LICENSE).

## Security

See [SECURITY.md](SECURITY.md). Do not open public issues for sensitive reports.
