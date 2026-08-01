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

    fund_metrics = [
        {
            "id": "raised",
            "label": "Rewards campaign raised",
            "value": round(stats["raised_cents"] / 100, 2),
            "unit": "USD",
            "note": "Sum of demo + confirmed pledges only",
        },
        {
            "id": "goal",
            "label": "Campaign goal",
            "value": round(stats["goal_cents"] / 100, 2),
            "unit": "USD",
            "note": "Soft goal for transparency; not a valuation",
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
    ]

    return {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "disclaimer": (
            "These metrics are operational and campaign transparency indicators only. "
            "They are NOT financial advice, profit forecasts, or guaranteed outcomes. "
            "Rewards campaign contributions are NOT equity or securities. "
            "Past or current figures do not imply future performance or ROI."
        ),
        "fund": {
            "campaign_id": campaign["id"],
            "status": campaign["status"],
            "demo_mode": campaign["demo_mode"],
            "metrics": fund_metrics,
            "by_tier": stats.get("by_tier", {}),
            "use_of_funds": campaign["use_of_funds"],
        },
        "product": {
            "metrics": PRODUCT_METRICS,
        },
        "health": {
            "api": "ok",
            "ledger": "ok",
        },
    }
