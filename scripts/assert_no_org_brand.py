#!/usr/bin/env python3
"""Fail if SkyLabs Developments org brand leaks into product surface."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = [
    ROOT / "apps",
    ROOT / "packages",
    ROOT / "content",
    ROOT / "README.md",
]
# Allowed product name only via separate check
FORBIDDEN = re.compile(
    r"SkyLabs Developments|ifrecia@skylabs|@SkyLabsDev|SkyLabs Rewards|/ SkyLabs|· SkyLabs",
    re.I,
)
# Marketing company brand (not Sky Colab)
FORBIDDEN_SKYLABS_WORD = re.compile(r"\bSkyLabs\b")
ALLOW_EXT = {".py", ".html", ".md", ".json", ".txt", ".example", ".js", ".css", ".yml", ".yaml", ".sh"}
SKIP_PARTS = {".venv", ".git", "__pycache__", "node_modules"}

def iter_files():
    for base in SCAN:
        if base.is_file():
            yield base
            continue
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if not p.is_file():
                continue
            if any(part in SKIP_PARTS for part in p.parts):
                continue
            if p.suffix.lower() not in ALLOW_EXT and p.name not in {".env.example"}:
                continue
            yield p

bad = []
for path in iter_files():
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue
    for i, line in enumerate(text.splitlines(), 1):
        if FORBIDDEN.search(line):
            bad.append(f"{path.relative_to(ROOT)}:{i}: {line.strip()[:120]}")
            continue
        if FORBIDDEN_SKYLABS_WORD.search(line) and "Sky Colab" not in line and "sky-colab" not in line.lower():
            # allow sky-colab product paths
            if "sky-colab" in line.lower() or "sky_colab" in line.lower():
                continue
            bad.append(f"{path.relative_to(ROOT)}:{i}: {line.strip()[:120]}")

if bad:
    print("ORG BRAND LEAKS:")
    print("\n".join(bad[:50]))
    sys.exit(1)
print("assert_no_org_brand: OK")
