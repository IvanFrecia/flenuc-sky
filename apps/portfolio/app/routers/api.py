"""JSON APIs: health, fund, KPI, Stripe webhook."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from app import __version__
from app.config import get_settings
from app.services.fund import campaign_payload, get_ledger
from app.services.kpi import kpi_snapshot
from app.services import stripe_service

router = APIRouter(prefix="/api", tags=["api"])


class DemoPledgeBody(BaseModel):
    tier_id: str = Field(..., min_length=1, max_length=64)
    email: str | None = Field(default=None, max_length=254)
    display_name: str | None = Field(default=None, max_length=64)
    public: bool = False


class CheckoutBody(BaseModel):
    tier_id: str = Field(..., min_length=1, max_length=64)
    email: str | None = Field(default=None, max_length=254)


@router.get("/health")
def health() -> dict[str, Any]:
    settings = get_settings()
    return {
        "status": "ok",
        "version": __version__,
        "env": settings.env,
        "demo_mode": settings.is_demo_mode,
    }


@router.get("/fund/campaign")
def fund_campaign() -> dict[str, Any]:
    return campaign_payload()


@router.get("/fund/ledger")
def fund_ledger(limit: int = 50) -> dict[str, Any]:
    limit = max(1, min(limit, 200))
    ledger = get_ledger()
    return {
        "campaign_id": campaign_payload()["id"],
        "stats": ledger.stats(),
        "entries": ledger.public_ledger(limit=limit),
        "disclaimer": campaign_payload()["disclaimer"],
    }


@router.post("/fund/demo-pledge")
def fund_demo_pledge(body: DemoPledgeBody) -> dict[str, Any]:
    settings = get_settings()
    # Allow demo pledges always in demo mode; also allow for testing when Stripe is on
    try:
        entry = get_ledger().add_demo_pledge(
            tier_id=body.tier_id,
            email=body.email,
            display_name=body.display_name,
            public=body.public,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {
        "ok": True,
        "entry": {
            "id": entry["id"],
            "tier_name": entry["tier_name"],
            "amount_cents": entry["amount_cents"],
            "status": entry["status"],
            "created_at": entry["created_at"],
        },
        "stats": get_ledger().stats(),
        "demo_mode": settings.is_demo_mode,
        "message": "Demo pledge recorded. No payment was processed.",
    }


@router.post("/fund/checkout")
def fund_checkout(body: CheckoutBody, request: Request) -> dict[str, Any]:
    settings = get_settings()
    base = settings.public_base_url.rstrip("/")
    success = f"{base}/fund?success=1"
    cancel = f"{base}/fund?canceled=1"
    try:
        result = stripe_service.create_checkout_session(
            tier_id=body.tier_id,
            success_url=success,
            cancel_url=cancel,
            customer_email=body.email,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Checkout failed: {e}") from e
    return result


@router.post("/fund/webhook")
async def fund_webhook(request: Request) -> dict[str, Any]:
    payload = await request.body()
    sig = request.headers.get("stripe-signature")
    try:
        return stripe_service.handle_webhook(payload, sig)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/kpi/snapshot")
def kpi() -> dict[str, Any]:
    return kpi_snapshot()
