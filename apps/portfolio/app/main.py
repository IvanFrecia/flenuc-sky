"""FastAPI application entrypoint — portfolio + rewards fund MVP."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.config import APP_DIR, get_settings
from app.routers import api, pages

settings = get_settings()

app = FastAPI(
    title="Flenuc Sky — Ivan Frecia / SkyLabs",
    version=__version__,
    docs_url="/api/docs" if settings.env != "production" else None,
    redoc_url=None,
)

static_dir = APP_DIR / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

app.include_router(api.router)
app.include_router(pages.router)


@app.on_event("startup")
def on_startup() -> None:
    # Ensure ledger path is writable
    from app.services.fund import get_ledger

    get_ledger()
