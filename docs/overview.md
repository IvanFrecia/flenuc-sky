# Flenuc Sky — Overview

Single-service MVP for:

1. Personal + SkyLabs portfolio site  
2. Rewards / pre-order crowdfunding (not equity)  
3. KPI dashboard with non-guarantee disclaimers  
4. Legal template pages  
5. Cloud Run deployment  

## Stack

- Python 3.12 + FastAPI + Jinja2 + static CSS/JS  
- JSON file ledger (`/tmp` on Cloud Run)  
- Stripe Checkout optional; demo pledges when `STRIPE_SECRET_KEY` unset  

## Campaign defaults

| Field | Value |
|-------|-------|
| Goal | $25,000 USD |
| Tiers | Supporter $15, Early Access $49, Builder $149, Sponsor $499 |
| Status | live |
| Contact | ifrecia@skylabs-developments.tech |

## Security notes

- Do not commit secrets.  
- Enable Stripe webhook signature verification in production.  
- Ledger on Cloud Run `/tmp` is instance-local (acceptable for demo; use Firestore/GCS for multi-instance production).  
