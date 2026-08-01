# Security Policy — flenuc-sky (Ivan Frecia portfolio)

## Supported versions

| Version | Supported |
|---------|-----------|
| `main` / 0.1.x | Yes |

## Scope

This repository hosts a **public personal portfolio** and optional **demo rewards ledger**:

- Deployed as a single FastAPI service on **Google Cloud Run**.
- Stripe is optional; without keys the app runs in **demo mode** (no real charges).
- Ledger files may contain display names from demo pledges — treat production data carefully.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security-sensitive reports.

1. Email **freciaivan@gmail.com** or open a **private** GitHub security advisory on [IvanFrecia/flenuc-sky](https://github.com/IvanFrecia/flenuc-sky) if available.
2. Include: affected revision/URL, reproduction steps, impact, and (if possible) a suggested fix.
3. Allow reasonable time for a fix before public disclosure.

## Safe defaults

- No secrets committed (`.env` gitignored; use `.env.example`).
- Non-root container user in the Dockerfile.
- Production disables OpenAPI docs (`/api/docs`).
- Webhook endpoints require Stripe signature verification when Stripe is enabled.

## Operator hardening

- Keep Stripe secrets in Secret Manager or Cloud Run env — never in git.
- Prefer least-privilege runtime service accounts.
- Review Cloud Run IAM (`allUsers` invoker only if the site must be public).
- Rotate keys if a secret is ever exposed in logs or a PR.
