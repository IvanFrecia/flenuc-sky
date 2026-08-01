"""Rewards campaign, tiers, and transparent ledger (demo + Stripe-ready)."""

from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.config import get_settings

# Fixed launch window: 5-day rewards sprint (UTC).
# Goal = published ops cost estimate + $10 profit floor (not a valuation).
_CAMPAIGN_START = datetime(2026, 8, 1, 20, 0, 0, tzinfo=timezone.utc)
_CAMPAIGN_END = _CAMPAIGN_START + timedelta(days=5)

# Transparent cost model for this sprint (USD cents)
COST_BREAKDOWN: list[dict[str, Any]] = [
    {
        "id": "cloud_run",
        "label": "Cloud Run (5d, scale-to-zero, light traffic)",
        "cents": 500,
        "note": "Estimate; actual bill may be lower under free-tier allowances",
    },
    {
        "id": "artifact_registry",
        "label": "Container image storage",
        "cents": 100,
        "note": "Artifact Registry retention for deploy images",
    },
    {
        "id": "logging_monitoring",
        "label": "Logging & monitoring",
        "cents": 100,
        "note": "Cloud Logging / Monitoring beyond free quota buffer",
    },
    {
        "id": "payment_reserve",
        "label": "Payment processing reserve",
        "cents": 200,
        "note": "Stripe/network fees if live payments enabled",
    },
    {
        "id": "contingency",
        "label": "Ops contingency",
        "cents": 100,
        "note": "Buffer for traffic spikes or redeploys",
    },
]
COST_TOTAL_CENTS = sum(int(c["cents"]) for c in COST_BREAKDOWN)  # $10.00
PROFIT_FLOOR_CENTS = 1_000  # $10.00 minimum profit target
GOAL_CENTS = COST_TOTAL_CENTS + PROFIT_FLOOR_CENTS  # $20.00

# Campaign — rewards only, NOT equity
CAMPAIGN: dict[str, Any] = {
    "id": "skylabs-rewards-5d-202608",
    "title": "5-Day SkyLabs Rewards Sprint",
    "tagline": "Cover real ops costs + a $10 profit floor — rewards only, not equity.",
    "currency": "USD",
    "goal_cents": GOAL_CENTS,
    "status": "live",
    "duration_days": 5,
    "starts_at": _CAMPAIGN_START.isoformat(),
    "ends_at": _CAMPAIGN_END.isoformat(),
    "cost_total_cents": COST_TOTAL_CENTS,
    "profit_floor_cents": PROFIT_FLOOR_CENTS,
    "cost_breakdown": COST_BREAKDOWN,
    "goal_formula": "goal = estimated_5d_ops_costs ($10) + profit_floor ($10) = $20",
    "disclaimer": (
        "This is a rewards / pre-order style campaign. Contributions are NOT equity, "
        "securities, or investment contracts. There is NO guaranteed profit to backers and NO assured ROI. "
        "The $10 profit floor is a founder target after published cost recovery — not a promise to contributors. "
        "You receive the stated reward (if any), not ownership or profit share."
    ),
    "use_of_funds": [
        {"category": "Cover published 5-day ops costs", "pct": 50},
        {"category": "Founder profit floor (target ≥ $10)", "pct": 50},
    ],
    "tiers": [
        {
            "id": "cheer",
            "name": "Cheer",
            "price_cents": 500,
            "description": "Quick boost toward cost recovery. Optional public thank-you.",
            "perks": ["Optional name on transparency ledger", "Campaign update email"],
            "limit": None,
        },
        {
            "id": "supporter",
            "name": "Supporter",
            "price_cents": 1000,
            "description": "Covers ~half the ops stack for the sprint + thank-you credit.",
            "perks": ["Everything in Cheer", "Supporter badge on fund page"],
            "limit": None,
        },
        {
            "id": "builder",
            "name": "Builder",
            "price_cents": 2500,
            "description": "Push past cost recovery into the profit floor + early Sky Colab notes.",
            "perks": [
                "Everything in Supporter",
                "Sky Colab architecture one-pager PDF",
                "Priority reply on GitHub Discussions (7 days)",
            ],
            "limit": 40,
        },
        {
            "id": "sponsor",
            "name": "Sponsor",
            "price_cents": 5000,
            "description": "Sponsor the full sprint goal alone + roadmap shout-out.",
            "perks": [
                "Everything in Builder",
                "Sponsor recognition on fund + home pages",
                "30-min async written Q&A credit",
            ],
            "limit": 10,
        },
    ],
}


def campaign_time_state(now: datetime | None = None) -> dict[str, Any]:
    """Countdown / window state for UI and KPI."""
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    starts = _CAMPAIGN_START
    ends = _CAMPAIGN_END
    total_s = (ends - starts).total_seconds()
    if now < starts:
        phase = "scheduled"
        remaining_s = (starts - now).total_seconds()
        elapsed_s = 0.0
    elif now > ends:
        phase = "ended"
        remaining_s = 0.0
        elapsed_s = total_s
    else:
        phase = "live"
        remaining_s = (ends - now).total_seconds()
        elapsed_s = (now - starts).total_seconds()
    days = int(remaining_s // 86400)
    hours = int((remaining_s % 86400) // 3600)
    minutes = int((remaining_s % 3600) // 60)
    return {
        "phase": phase,
        "starts_at": starts.isoformat(),
        "ends_at": ends.isoformat(),
        "remaining_seconds": int(max(0, remaining_s)),
        "elapsed_seconds": int(max(0, elapsed_s)),
        "remaining_label": f"{days}d {hours}h {minutes}m",
        "window_progress_pct": round(min(100.0, (elapsed_s / total_s) * 100.0), 1) if total_s else 0.0,
    }


def economics(stats: dict[str, Any]) -> dict[str, Any]:
    """Cost recovery + profit-floor tracking (founder economics, not backer returns)."""
    raised = int(stats.get("raised_cents", 0))
    costs = COST_TOTAL_CENTS
    profit_floor = PROFIT_FLOOR_CENTS
    cost_covered = min(raised, costs)
    surplus = max(0, raised - costs)
    cost_coverage_pct = round((cost_covered / costs) * 100.0, 1) if costs else 0.0
    profit_progress_pct = round(min(100.0, (surplus / profit_floor) * 100.0), 1) if profit_floor else 0.0
    shortfall_to_goal = max(0, GOAL_CENTS - raised)
    return {
        "raised_cents": raised,
        "cost_total_cents": costs,
        "cost_covered_cents": cost_covered,
        "cost_coverage_pct": cost_coverage_pct,
        "surplus_after_costs_cents": surplus,
        "profit_floor_cents": profit_floor,
        "profit_progress_pct": profit_progress_pct,
        "profit_floor_met": surplus >= profit_floor,
        "costs_covered": raised >= costs,
        "goal_met": raised >= GOAL_CENTS,
        "shortfall_to_goal_cents": shortfall_to_goal,
        "note": (
            "Founder economics only: surplus after published costs is tracked against a $10 "
            "profit floor. This is not a return to backers and is not guaranteed."
        ),
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
    time_state = campaign_time_state()
    # Soft-close: still accept demo after end, but mark phase ended for UI
    status = CAMPAIGN["status"]
    if time_state["phase"] == "ended" and status == "live":
        status = "ended"
    return {
        **CAMPAIGN,
        "status": status,
        "stats": stats,
        "time": time_state,
        "economics": economics(stats),
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
