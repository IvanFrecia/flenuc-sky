"""Load and render legal markdown from packages/legal."""

from __future__ import annotations

from pathlib import Path

import markdown

from app.config import LEGAL_MD_DIR, APP_DIR


LEGAL_SLUGS = {
    "privacy": "privacy.md",
    "terms": "terms.md",
    "rewards": "rewards.md",
    "risk": "risk.md",
    "refunds": "refunds.md",
}

TITLES = {
    "privacy": "Privacy Policy",
    "terms": "Terms of Use",
    "rewards": "Rewards Campaign Terms",
    "risk": "Risk Disclosures",
    "refunds": "Refund Policy",
}


def legal_path(slug: str) -> Path | None:
    filename = LEGAL_SLUGS.get(slug)
    if not filename:
        return None
    primary = LEGAL_MD_DIR / filename
    if primary.exists():
        return primary
    # Fallback: app-bundled copies (for Docker single-context builds)
    fallback = APP_DIR / "legal_md" / filename
    if fallback.exists():
        return fallback
    return None


def render_legal_html(slug: str) -> tuple[str, str] | None:
    path = legal_path(slug)
    if not path:
        return None
    raw = path.read_text(encoding="utf-8")
    html = markdown.markdown(
        raw,
        extensions=["extra", "sane_lists", "toc"],
    )
    title = TITLES.get(slug, slug.replace("-", " ").title())
    return title, html
