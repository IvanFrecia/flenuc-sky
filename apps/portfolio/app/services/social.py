"""Social link set (consultant-recommended handles)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.config import APP_DIR

_DEFAULT: dict[str, Any] = {
    "github": "https://github.com/IvanFrecia",
    "github_sky_colab": "https://github.com/IvanFrecia/sky-colab",
    "website": "https://sky-portfolio-6k4smyyquq-uc.a.run.app",
    "blog": "https://sky-portfolio-6k4smyyquq-uc.a.run.app",
    "x": "https://x.com/IvanFrecia",
    "x_handle": "@IvanFrecia",
    "linkedin": "https://www.linkedin.com/in/ivanfrecia",
    "email": "freciaivan@gmail.com",
}


@lru_cache
def get_social() -> dict[str, Any]:
    path = APP_DIR / "data" / "social.json"
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                merged = {**_DEFAULT, **{k: v for k, v in data.items() if k != "notes"}}
                return merged
        except (OSError, json.JSONDecodeError):
            pass
    return dict(_DEFAULT)
