"""HTML page routes (Jinja2)."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import APP_DIR, get_settings
from app.services.fund import campaign_payload, get_ledger
from app.services.kpi import kpi_snapshot
from app.services.legal import render_legal_html, LEGAL_SLUGS
from app.services.social import get_social

templates = Jinja2Templates(directory=str(APP_DIR / "templates"))
router = APIRouter(tags=["pages"])


def _ctx(**extra):
    settings = get_settings()
    base = {
        "site_name": settings.site_name,
        "contact_email": settings.contact_email,
        "copyright_year": settings.copyright_year,
        "public_base_url": settings.public_base_url.rstrip("/"),
        "demo_mode": settings.is_demo_mode,
        "nav_active": extra.pop("nav_active", ""),
        "page_title": extra.pop("page_title", settings.site_name),
        "page_description": extra.pop(
            "page_description",
            "Ivan Frecia — multi-model systems, personal portfolio, and rewards campaign.",
        ),
        "og_image": extra.pop("og_image", "/static/img/og-default.png"),
        "social": get_social(),
    }
    base.update(extra)
    return base


def render(request: Request, name: str, status_code: int = 200, **extra):
    return templates.TemplateResponse(
        request,
        name,
        _ctx(**extra),
        status_code=status_code,
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return render(
        request,
        "home.html",
        nav_active="home",
        page_title="Ivan Frecia",
        page_description="Multi-model systems, applied AI engineering, and personal product work.",
    )


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return render(
        request,
        "about.html",
        nav_active="about",
        page_title="About · Ivan Frecia",
    )


@router.get("/work", response_class=HTMLResponse)
def work(request: Request):
    # Public repos only (IvanFrecia). No private client brands.
    projects = [
        {
            "title": "Sky Colab",
            "summary": (
                "Multi-model collaboration with transparent work-product boards: "
                "structured handoffs, challenge mode, audit trail. CLI duo · Apache-2.0."
            ),
            "tags": ["Multi-agent", "Python", "Transparency", "OSS"],
            "status": "Open source",
            "url": "https://github.com/IvanFrecia/sky-colab",
        },
        {
            "title": "Pred Sys Sky Fútbol",
            "summary": (
                "Beacon-anchored football predictive system — ratings, outcomes, "
                "and financial potential analysis. Local-first · MIT."
            ),
            "tags": ["ML", "Sports", "Python", "MIT"],
            "status": "Open source",
            "url": "https://github.com/IvanFrecia/pred-sys-sky-futbol",
        },
        {
            "title": "Motion Detection Tracking",
            "summary": (
                "Sports video motion detection with a smooth virtual-camera viewport "
                "that follows primary action. Python · OpenCV · NumPy."
            ),
            "tags": ["Computer vision", "OpenCV", "Python"],
            "status": "Open source",
            "url": "https://github.com/IvanFrecia/motion_detection_tracking",
        },
        {
            "title": "Self-hosted rotating VPN (lab)",
            "summary": "Learning project for self-hosted, rotating VPN free-tier patterns.",
            "tags": ["Infra", "Networking", "Lab"],
            "status": "Open source",
            "url": "https://github.com/IvanFrecia/self_hosted-rotating_vpn-free-tier",
        },
        {
            "title": "LSTM stock notebook",
            "summary": "LSTM forecasting notebook (AMZN/NVDA-style market series exploration).",
            "tags": ["Deep learning", "Time series", "Notebook"],
            "status": "Open source",
            "url": "https://github.com/IvanFrecia/LSTM_NVDA_STOCK_NOTEBOOK",
        },
        {
            "title": "Web structure Angular",
            "summary": "Angular Material + UnoCSS + SSR structure reference for modern web apps.",
            "tags": ["Angular", "SSR", "Frontend"],
            "status": "Open source",
            "url": "https://github.com/IvanFrecia/web-structure-angular",
        },
    ]
    return render(
        request,
        "work.html",
        nav_active="work",
        page_title="Work · Ivan Frecia",
        projects=projects,
    )


@router.get("/sky-colab", response_class=HTMLResponse)
def sky_colab(request: Request):
    return render(
        request,
        "sky_colab.html",
        nav_active="sky-colab",
        page_title="sky-colab · Ivan Frecia",
        page_description="sky-colab — multi-model collaboration tooling by Ivan Frecia.",
    )


@router.get("/fund", response_class=HTMLResponse)
def fund(request: Request):
    campaign = campaign_payload()
    ledger = get_ledger()
    return render(
        request,
        "fund.html",
        nav_active="fund",
        page_title="Rewards Campaign · Ivan Frecia",
        page_description="Support personal R&D with rewards tiers. Not equity. No guaranteed profit.",
        campaign=campaign,
        ledger_entries=ledger.public_ledger(limit=30),
        success=request.query_params.get("success"),
        canceled=request.query_params.get("canceled"),
    )


@router.get("/kpi", response_class=HTMLResponse)
def kpi_page(request: Request):
    snap = kpi_snapshot()
    return render(
        request,
        "kpi.html",
        nav_active="kpi",
        page_title="KPI Dashboard · Ivan Frecia",
        page_description="Operational metrics and campaign transparency. Not financial guarantees.",
        snapshot=snap,
    )


@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return render(
        request,
        "contact.html",
        nav_active="contact",
        page_title="Contact · Ivan Frecia",
    )


@router.get("/legal", response_class=HTMLResponse)
def legal_index(request: Request):
    return render(
        request,
        "legal/index.html",
        nav_active="legal",
        page_title="Legal · Ivan Frecia",
        slugs=list(LEGAL_SLUGS.keys()),
    )


@router.get("/legal/{slug}", response_class=HTMLResponse)
def legal_page(request: Request, slug: str):
    if slug not in LEGAL_SLUGS:
        return RedirectResponse(url="/legal", status_code=302)
    rendered = render_legal_html(slug)
    if not rendered:
        return render(
            request,
            "legal/page.html",
            status_code=404,
            nav_active="legal",
            page_title="Legal · Ivan Frecia",
            legal_title="Document unavailable",
            legal_html="<p>This document could not be loaded.</p>",
        )
    title, html = rendered
    return render(
        request,
        "legal/page.html",
        nav_active="legal",
        page_title=f"{title} · Ivan Frecia",
        legal_title=title,
        legal_html=html,
    )
