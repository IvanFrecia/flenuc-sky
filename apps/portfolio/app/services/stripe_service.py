"""Stripe Checkout + webhook helpers. Falls back to demo mode when no secret key."""

from __future__ import annotations

from typing import Any

from app.config import get_settings
from app.services.fund import CAMPAIGN, get_ledger, _tier_by_id


def create_checkout_session(
    *,
    tier_id: str,
    success_url: str,
    cancel_url: str,
    customer_email: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    tier = _tier_by_id(tier_id)
    if not tier:
        raise ValueError(f"Unknown tier: {tier_id}")

    if not settings.stripe_enabled:
        return {
            "mode": "demo",
            "message": "Stripe not configured. Use demo pledge endpoint instead.",
            "checkout_url": None,
            "tier_id": tier_id,
        }

    import stripe

    stripe.api_key = settings.stripe_secret_key
    session = stripe.checkout.Session.create(
        mode="payment",
        success_url=success_url + ("&" if "?" in success_url else "?") + "session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        customer_email=customer_email,
        line_items=[
            {
                "price_data": {
                    "currency": CAMPAIGN["currency"].lower(),
                    "unit_amount": int(tier["price_cents"]),
                    "product_data": {
                        "name": f"SkyLabs Rewards — {tier['name']}",
                        "description": (
                            "Rewards/pre-order contribution. NOT equity or securities. "
                            "No guaranteed profit or ROI."
                        )[:500],
                    },
                },
                "quantity": 1,
            }
        ],
        metadata={
            "campaign_id": CAMPAIGN["id"],
            "tier_id": tier["id"],
            "kind": "rewards_pledge",
        },
    )
    return {
        "mode": "stripe",
        "checkout_url": session.url,
        "session_id": session.id,
        "tier_id": tier_id,
    }


def handle_webhook(payload: bytes, sig_header: str | None) -> dict[str, Any]:
    settings = get_settings()
    if not settings.stripe_enabled:
        return {"ok": False, "error": "Stripe not configured"}

    import stripe

    stripe.api_key = settings.stripe_secret_key
    event: Any
    if settings.stripe_webhook_secret and sig_header:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    else:
        # Dev fallback: parse without verification (not for production)
        import json

        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        meta = session.get("metadata") or {}
        tier_id = meta.get("tier_id") or "unknown"
        amount = int(session.get("amount_total") or 0)
        get_ledger().add_stripe_pledge(
            session_id=session.get("id") or "unknown",
            tier_id=tier_id,
            amount_cents=amount,
            email=session.get("customer_details", {}).get("email")
            if isinstance(session.get("customer_details"), dict)
            else session.get("customer_email"),
            payment_intent=session.get("payment_intent"),
        )
        return {"ok": True, "handled": event["type"]}

    return {"ok": True, "handled": event["type"], "ignored": True}
