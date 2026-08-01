"""HTML page routes (Jinja2)."""

from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import APP_DIR, get_settings
from app.services.fund import campaign_payload, get_ledger
from app.services.kpi import kpi_snapshot
from app.services.legal import render_legal_html, LEGAL_SLUGS

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
            "Ivan Frecia · SkyLabs — multi-model systems, portfolio, and rewards campaign.",
        ),
        "og_image": extra.pop("og_image", "/static/img/og-default.png"),
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
        page_title="Ivan Frecia · SkyLabs",
        page_description="Multi-model systems, applied AI engineering, and SkyLabs product work.",
    )


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return render(
        request,
        "about.html",
        nav_active="about",
        page_title="About · Ivan Frecia / SkyLabs",
    )


@router.get("/work", response_class=HTMLResponse)
def work(request: Request):
    projects = [
        {
            "title": "Pending approval #1",
            "summary": "Confidential client engagement — details pending public approval.",
            "tags": ["Systems", "Integration"],
            "status": "Private",
        },
        {
            "title": "Pending approval #2",
            "summary": "Confidential client engagement — details pending public approval.",
            "tags": ["AI", "Platform"],
            "status": "Private",
        },
        {
            "title": "Pending approval #3",
            "summary": "Confidential client engagement — details pending public approval.",
            "tags": ["Cloud", "Ops"],
            "status": "Private",
        },
    ]
    return render(
        request,
        "work.html",
        nav_active="work",
        page_title="Work · Ivan Frecia / SkyLabs",
        projects=projects,
    )


@router.get("/sky-colab", response_class=HTMLResponse)
def sky_colab(request: Request):
    return render(
        request,
        "sky_colab.html",
        nav_active="sky-colab",
        page_title="sky-colab · SkyLabs",
        page_description="sky-colab — multi-model collaboration tooling by SkyLabs.",
    )


@router.get("/fund", response_class=HTMLResponse)
def fund(request: Request):
    campaign = campaign_payload()
    ledger = get_ledger()
    return render(
        request,
        "fund.html",
        nav_active="fund",
        page_title="Rewards Campaign · SkyLabs",
        page_description="Support SkyLabs R&D with rewards tiers. Not equity. No guaranteed profit.",
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
        page_title="KPI Dashboard · SkyLabs",
        page_description="Operational metrics and campaign transparency. Not financial guarantees.",
        snapshot=snap,
    )


@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return render(
        request,
        "contact.html",
        nav_active="contact",
        page_title="Contact · Ivan Frecia / SkyLabs",
    )


@router.get("/legal", response_class=HTMLResponse)
def legal_index(request: Request):
    return render(
        request,
        "legal/index.html",
        nav_active="legal",
        page_title="Legal · SkyLabs",
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
            page_title="Legal · SkyLabs",
            legal_title="Document unavailable",
            legal_html="<p>This document could not be loaded.</p>",
        )
    title, html = rendered
    return render(
        request,
        "legal/page.html",
        nav_active="legal",
        page_title=f"{title} · SkyLabs",
        legal_title=title,
        legal_html=html,
    )
