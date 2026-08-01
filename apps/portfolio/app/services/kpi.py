"""KPI snapshot — product + fund metrics with explicit non-guarantee framing."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.fund import campaign_payload, get_ledger


# Static / illustrative product metrics (not financial projections)
PRODUCT_METRICS: list[dict[str, Any]] = [
    {
        "id": "sky_colab_repos",
        "label": "sky-colab open modules",
        "value": 1,
        "unit": "repo",
        "note": "Public reference: github.com/IvanFrecia/sky-colab",
    },
    {
        "id": "models_integrated",
        "label": "Model integrations (design)",
        "value": 4,
        "unit": "providers",
        "note": "Architecture target for multi-model orchestration",
    },
    {
        "id": "docs_pages",
        "label": "Documentation pages (scaffold)",
        "value": 12,
        "unit": "pages",
        "note": "Growing with product releases",
    },
    {
        "id": "uptime_target",
        "label": "Service uptime target",
        "value": 99.5,
        "unit": "%",
        "note": "Operational target only — not a contractual SLA in demo",
    },
]


def kpi_snapshot() -> dict[str, Any]:
    ledger = get_ledger()
    stats = ledger.stats()
    campaign = campaign_payload()

    econ = campaign.get("economics") or {}
    time_state = campaign.get("time") or {}

    fund_metrics = [
        {
            "id": "raised",
            "label": "Rewards sprint raised",
            "value": round(stats["raised_cents"] / 100, 2),
            "unit": "USD",
            "note": "Sum of demo + confirmed pledges only",
        },
        {
            "id": "goal",
            "label": "Sprint goal (costs + $10 floor)",
            "value": round(stats["goal_cents"] / 100, 2),
            "unit": "USD",
            "note": campaign.get("goal_formula", "costs + profit floor"),
        },
        {
            "id": "cost_coverage",
            "label": "Ops cost coverage",
            "value": econ.get("cost_coverage_pct", 0),
            "unit": "%",
            "note": "Raised applied to published 5-day ops costs first",
        },
        {
            "id": "profit_floor",
            "label": "Profit floor progress (founder)",
            "value": econ.get("profit_progress_pct", 0),
            "unit": "%",
            "note": "Surplus after costs vs $10 floor — not a backer return",
        },
        {
            "id": "progress",
            "label": "Progress toward goal",
            "value": stats["progress_pct"],
            "unit": "%",
            "note": "Raised ÷ goal",
        },
        {
            "id": "pledges",
            "label": "Pledge count",
            "value": stats["pledge_count"],
            "unit": "pledges",
            "note": "Includes demo pledges when Stripe is disabled",
        },
        {
            "id": "time_left",
            "label": "Campaign time remaining",
            "value": time_state.get("remaining_label", "—"),
            "unit": "",
            "note": f"Phase: {time_state.get('phase', '—')} · ends {campaign.get('ends_at', '')[:10]}",
        },
    ]

    return {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "disclaimer": (
            "These metrics are operational and campaign transparency indicators only. "
            "They are NOT financial advice, profit forecasts, or guaranteed outcomes. "
            "The founder profit floor is an internal target after cost recovery — not a return to backers. "
            "Rewards campaign contributions are NOT equity or securities. "
            "Past or current figures do not imply future performance or ROI."
        ),
        "fund": {
            "campaign_id": campaign["id"],
            "status": campaign["status"],
            "demo_mode": campaign["demo_mode"],
            "duration_days": campaign.get("duration_days"),
            "metrics": fund_metrics,
            "economics": econ,
            "time": time_state,
            "cost_breakdown": campaign.get("cost_breakdown", []),
            "by_tier": stats.get("by_tier", {}),
            "use_of_funds": campaign["use_of_funds"],
        },
        "product": {
            "metrics": PRODUCT_METRICS,
        },
        "health": {
            "api": "ok",
            "ledger": "ok",
            "host": "Cloud Run interim host (flenuc-sky pending billing quota)",
        },
    }
