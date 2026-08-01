"""Rewards campaign, tiers, and transparent ledger (demo + Stripe-ready)."""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import get_settings

# Campaign defaults (demo) — rewards only, NOT equity
CAMPAIGN: dict[str, Any] = {
    "id": "skylabs-rewards-2026",
    "title": "SkyLabs Rewards Campaign",
    "tagline": "Back multi-model systems R&D — earn rewards, not equity.",
    "currency": "USD",
    "goal_cents": 2_500_000,  # $25,000
    "status": "live",
    "disclaimer": (
        "This is a rewards / pre-order style campaign. Contributions are NOT equity, "
        "securities, or investment contracts. There is NO guaranteed profit and NO assured ROI. "
        "You receive the stated reward (if any), not ownership or profit share."
    ),
    "use_of_funds": [
        {"category": "Product R&D (sky-colab & multi-model tooling)", "pct": 40},
        {"category": "Infrastructure & compute", "pct": 25},
        {"category": "Security, compliance & legal templates", "pct": 15},
        {"category": "Community, docs & support", "pct": 12},
        {"category": "Operations & contingency", "pct": 8},
    ],
    "tiers": [
        {
            "id": "supporter",
            "name": "Supporter",
            "price_cents": 1500,
            "description": "Thank-you credit on the transparency page + exclusive progress email updates.",
            "perks": ["Name on supporters list (optional)", "Quarterly update emails"],
            "limit": None,
        },
        {
            "id": "early-access",
            "name": "Early Access",
            "price_cents": 4900,
            "description": "Early access invite to sky-colab beta features when released.",
            "perks": ["Everything in Supporter", "Beta access queue priority", "Private changelog"],
            "limit": 200,
        },
        {
            "id": "builder",
            "name": "Builder",
            "price_cents": 14900,
            "description": "Builder kit: templates, architecture notes, and a 30-min async Q&A credit.",
            "perks": [
                "Everything in Early Access",
                "Architecture notes pack",
                "One async Q&A (written, 30 min equivalent)",
            ],
            "limit": 50,
        },
        {
            "id": "sponsor",
            "name": "Sponsor",
            "price_cents": 49900,
            "description": "Sponsor recognition + optional logo on campaign page + priority roadmap input.",
            "perks": [
                "Everything in Builder",
                "Sponsor recognition on fund page",
                "Roadmap input session (async)",
            ],
            "limit": 15,
        },
    ],
}


class FundLedger:
    """Thread-safe JSON ledger for demo pledges (and Stripe-confirmed events)."""

    def __init__(self, path: Path | None = None) -> None:
        settings = get_settings()
        self.path = path or settings.resolve_ledger_path()
        self._lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(
                {
                    "version": 1,
                    "campaign_id": CAMPAIGN["id"],
                    "entries": [],
                    "updated_at": _now_iso(),
                }
            )

    def _read(self) -> dict[str, Any]:
        with open(self.path, encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: dict[str, Any]) -> None:
        data["updated_at"] = _now_iso()
        tmp = self.path.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.replace(self.path)

    def list_entries(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._lock:
            data = self._read()
            entries = list(reversed(data.get("entries", [])))
            return entries[:limit]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            data = self._read()
            entries = data.get("entries", [])
            confirmed = [e for e in entries if e.get("status") in ("confirmed", "demo")]
            raised_cents = sum(int(e.get("amount_cents", 0)) for e in confirmed)
            by_tier: dict[str, int] = {}
            for e in confirmed:
                tid = e.get("tier_id") or "unknown"
                by_tier[tid] = by_tier.get(tid, 0) + 1
            goal = int(CAMPAIGN["goal_cents"])
            pct = min(100.0, (raised_cents / goal * 100.0) if goal else 0.0)
            return {
                "raised_cents": raised_cents,
                "goal_cents": goal,
                "progress_pct": round(pct, 2),
                "pledge_count": len(confirmed),
                "by_tier": by_tier,
                "currency": CAMPAIGN["currency"],
                "status": CAMPAIGN["status"],
            }

    def add_demo_pledge(
        self,
        *,
        tier_id: str,
        email: str | None = None,
        display_name: str | None = None,
        public: bool = False,
    ) -> dict[str, Any]:
        tier = _tier_by_id(tier_id)
        if not tier:
            raise ValueError(f"Unknown tier: {tier_id}")
        if CAMPAIGN["status"] != "live":
            raise ValueError("Campaign is not live")

        entry = {
            "id": f"demo_{uuid.uuid4().hex[:12]}",
            "type": "pledge",
            "source": "demo",
            "status": "demo",
            "tier_id": tier["id"],
            "tier_name": tier["name"],
            "amount_cents": int(tier["price_cents"]),
            "currency": CAMPAIGN["currency"],
            "email_hash": _mask_email(email) if email else None,
            "display_name": (display_name or "Anonymous")[:64] if public else "Anonymous",
            "public": public,
            "created_at": _now_iso(),
            "note": "Demo pledge (no payment processed)",
        }
        with self._lock:
            data = self._read()
            data.setdefault("entries", []).append(entry)
            self._write(data)
        return entry

    def add_stripe_pledge(
        self,
        *,
        session_id: str,
        tier_id: str,
        amount_cents: int,
        email: str | None = None,
        payment_intent: str | None = None,
    ) -> dict[str, Any]:
        tier = _tier_by_id(tier_id) or {"id": tier_id, "name": tier_id}
        entry = {
            "id": f"stripe_{session_id[:16]}",
            "type": "pledge",
            "source": "stripe",
            "status": "confirmed",
            "tier_id": tier.get("id", tier_id),
            "tier_name": tier.get("name", tier_id),
            "amount_cents": int(amount_cents),
            "currency": CAMPAIGN["currency"],
            "email_hash": _mask_email(email) if email else None,
            "display_name": "Supporter",
            "public": False,
            "stripe_session_id": session_id,
            "payment_intent": payment_intent,
            "created_at": _now_iso(),
            "note": "Stripe Checkout completed",
        }
        with self._lock:
            data = self._read()
            # Idempotency: skip if session already recorded
            for e in data.get("entries", []):
                if e.get("stripe_session_id") == session_id:
                    return e
            data.setdefault("entries", []).append(entry)
            self._write(data)
        return entry

    def public_ledger(self, limit: int = 50) -> list[dict[str, Any]]:
        """Sanitized ledger for transparency UI / API."""
        out = []
        for e in self.list_entries(limit=limit):
            out.append(
                {
                    "id": e.get("id"),
                    "status": e.get("status"),
                    "source": e.get("source"),
                    "tier_name": e.get("tier_name"),
                    "amount_cents": e.get("amount_cents"),
                    "currency": e.get("currency"),
                    "display_name": e.get("display_name") if e.get("public") else "Anonymous",
                    "created_at": e.get("created_at"),
                }
            )
        return out


_ledger: FundLedger | None = None


def get_ledger() -> FundLedger:
    global _ledger
    if _ledger is None:
        _ledger = FundLedger()
    return _ledger


def campaign_payload() -> dict[str, Any]:
    ledger = get_ledger()
    stats = ledger.stats()
    settings = get_settings()
    return {
        **CAMPAIGN,
        "stats": stats,
        "demo_mode": settings.is_demo_mode,
        "stripe_publishable_key": settings.stripe_publishable_key,
    }


def _tier_by_id(tier_id: str) -> dict[str, Any] | None:
    for t in CAMPAIGN["tiers"]:
        if t["id"] == tier_id:
            return t
    return None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mask_email(email: str) -> str:
    email = email.strip().lower()
    if "@" not in email:
        return "***"
    local, domain = email.split("@", 1)
    if len(local) <= 2:
        masked = "*" * len(local)
    else:
        masked = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked}@{domain}"
