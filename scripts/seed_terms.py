#!/usr/bin/env python3
"""Seed src/content/terms/*.md from ingest/out/terms_candidates.json."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "ingest/out/terms_candidates.json"
TERMS_DIR = ROOT / "src/content/terms"


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return (s or "term")[:70]


def letter_for(title: str) -> str:
    for ch in title:
        if ch.isalpha():
            return ch.upper()
    return "?"


def yaml_list(items):
    if not items:
        return "  []"
    return "\n".join(f'  - "{item}"' for item in items)


def main():
    if not CANDIDATES.exists():
        print(f"No candidates file at {CANDIDATES}; skipping.")
        return
    data = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    TERMS_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for t in data:
        title = (t.get("title") or "").strip()
        if not title:
            continue
        slug = slugify(title)
        definition = (t.get("definition") or "").strip()
        provenance = t.get("provenance") or []
        source = provenance[0] if provenance else "Joscha Bach on X (@Plinz)"
        related = t.get("related") or []
        tags = t.get("tags") or ["core concept"]
        body = f"""---
letter: "{letter_for(title)}"
title: "{title.replace('"', '\\"')}"
authored_by: "Joscha Bach"
source: "{source.replace('"', '\\"')}"
provenance:
{yaml_list(provenance)}
related:
{yaml_list(related)}
tags:
{yaml_list(tags)}
is_new: true
---

{definition}
"""
        (TERMS_DIR / f"{slug}.md").write_text(body, encoding="utf-8")
        count += 1
    print(f"Seeded {count} terms → {TERMS_DIR}")


if __name__ == "__main__":
    main()