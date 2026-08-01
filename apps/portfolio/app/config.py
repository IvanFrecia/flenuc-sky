"""Application settings."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


APP_DIR = Path(__file__).resolve().parent
PACKAGE_ROOT = APP_DIR.parent  # apps/portfolio (local) or /app (Docker)
REPO_ROOT = PACKAGE_ROOT.parent.parent  # flenuc-sky (local monorepo)

def _resolve_legal_dir() -> Path:
    candidates = [
        REPO_ROOT / "packages" / "legal",
        PACKAGE_ROOT / "packages" / "legal",  # Docker: /app/packages/legal
        Path("/app/packages/legal"),
        APP_DIR / "legal_md",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return APP_DIR / "legal_md"


LEGAL_MD_DIR = _resolve_legal_dir()



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    port: int = 8080
    host: str = "0.0.0.0"
    env: str = "development"
    public_base_url: str = "http://localhost:8080"

    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_publishable_key: str | None = None

    ledger_path: str | None = None
    contact_email: str = "ifrecia@skylabs-developments.tech"
    site_name: str = "Ivan Frecia · SkyLabs"
    copyright_year: int = 2026

    @property
    def stripe_enabled(self) -> bool:
        return bool(self.stripe_secret_key)

    @property
    def is_demo_mode(self) -> bool:
        return not self.stripe_enabled

    def resolve_ledger_path(self) -> Path:
        if self.ledger_path:
            return Path(self.ledger_path)
        # Cloud Run / containers: prefer /tmp (writable)
        if os.environ.get("K_SERVICE") or self.env == "production":
            return Path("/tmp/flenuc-sky-ledger.json")
        data_dir = PACKAGE_ROOT / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir / "ledger.json"


@lru_cache
def get_settings() -> Settings:
    return Settings()
