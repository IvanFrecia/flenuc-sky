# Flenuc Sky — Overview

Single-service MVP for:

1. Personal portfolio site (Ivan Frecia)  
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
| Campaign id | `ivan-frecia-rewards-5d-202608` |
| Goal | ops costs + $10 profit floor (see fund service) |
| Status | live |
| Contact | freciaivan@gmail.com |

## Security notes

- Do not commit secrets.  
- Enable Stripe webhook signature verification in production.  
- Ledger on Cloud Run `/tmp` is instance-local (acceptable for demo; use Firestore/GCS for multi-instance production).  
