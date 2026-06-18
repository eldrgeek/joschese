#!/usr/bin/env python3
"""
pull_joscha_x.py — Grok/xAI ingestion for the Joscha Bach thinker-site.

Mirrors the role of the Levin corpus pipeline, but Joscha's output lives mostly
on X. We use xAI's server-side `x_search` tool (the successor to the retired
Live Search API) to let Grok read his posts/threads directly, then emit content
in the SAME schema the Levinese Astro site uses (collections: xposts, terms).

Docs (verified 2026-06-18):
  https://docs.x.ai/developers/tools/x-search
  - endpoint: POST https://api.x.ai/v1/responses  (OpenAI-compatible)
  - model:    grok-4.3
  - tool:     {"type":"x_search","allowed_x_handles":[...],"from_date":"YYYY-MM-DD","to_date":"YYYY-MM-DD"}

Outputs (consumed by the site scaffold step — see ../BUILD-JOSCHA.md):
  ingest/out/xposts/<slug>.json     one per notable post/thread (Astro `xposts` schema)
  ingest/out/terms_candidates.json  candidate dictionary entries (Astro `terms` schema seed)
  ingest/raw/<topic>-<window>.json  raw model responses (for audit / re-parsing)

Usage:
  pip install -r requirements.txt
  # put XAI_API_KEY in ../.env  (gitignored)
  python pull_joscha_x.py                 # full run
  python pull_joscha_x.py --dry-run       # print plan, no API calls
  python pull_joscha_x.py --since 2023-01-01 --until 2026-06-18
"""

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUT = ROOT / "out"
RAW = ROOT / "raw"

MODEL = "grok-4.3"
XAI_BASE = "https://api.x.ai/v1"

# Joscha's central themes — used as semantic search seeds so Grok surfaces the
# threads where he actually develops each idea (not just mentions it).
TOPICS = [
    "consciousness as a simulation / the self as a story the brain tells",
    "computational functionalism and substrate independence of mind",
    "cyber-animism, spirits as self-organizing software agents",
    "the nature of meaning, language models, and understanding",
    "AI alignment, agency, and machine sentience",
    "the lebenswelt, dreaming, and perception as controlled hallucination",
    "free will, determinism, and the control model of the self",
    "physics, computation, and whether the universe is a cellular automaton",
    "intelligence vs. consciousness vs. agency distinctions",
    "spirituality, religion, and rationality reinterpreted computationally",
]

# Coined / characteristically-Joscha terms to seed the dictionary. The model is
# asked to ground each in his own posts (provenance = post URLs).
SEED_TERMS = [
    "cyber-animism", "the self as a story", "computational functionalism",
    "lebenswelt", "controlled hallucination", "substrate independence",
    "software agent (mind as)", "coherence (as truth criterion)",
    "the second-person perspective", "sentience vs. intelligence",
]

SYSTEM = (
    "You are a research archivist building a faithful, well-sourced corpus of "
    "Joscha Bach's PUBLIC thinking as expressed on X. Use the x_search tool to "
    "read his actual posts. Never invent posts, quotes, URLs, or dates: every "
    "item you output must correspond to a real post you found, with its real "
    "permalink and date. If you are unsure a post exists, omit it. Prefer "
    "substantive threads and standalone insights over replies and chit-chat."
)


def out_schema_prompt(topic: str) -> str:
    return f"""Find Joscha Bach's most substantive X posts/threads about: {topic}

Return STRICT JSON (no prose, no markdown fences) of this shape:
{{
  "xposts": [
    {{
      "title": "<= 90 char editorial title capturing the idea",
      "url": "https://x.com/Plinz/status/...",   // real permalink
      "date": "YYYY-MM-DD",
      "excerpt": "1-3 sentence faithful summary or short quoted core of the post",
      "handle": "Plinz",
      "thread_id": "<status id or null>"
    }}
  ],
  "terms": [
    {{
      "title": "term as Joscha uses it",
      "definition": "2-4 sentences, in his conceptual register, grounded in the posts",
      "provenance": ["https://x.com/Plinz/status/..."]
    }}
  ]
}}
Aim for 5-12 high-quality xposts and 0-4 terms for this topic. Omit anything you cannot source to a real post."""


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return (s or "post")[:70]


def windows(since: dt.date, until: dt.date, months: int = 12):
    cur = since
    while cur < until:
        nxt = min(until, cur + dt.timedelta(days=30 * months))
        yield cur.isoformat(), nxt.isoformat()
        cur = nxt


def call_grok(client, handle, topic, from_date, to_date):
    resp = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": out_schema_prompt(topic)},
        ],
        tools=[{
            "type": "x_search",
            "allowed_x_handles": [handle],
            "from_date": from_date,
            "to_date": to_date,
        }],
    )
    return getattr(resp, "output_text", None) or str(resp)


def parse_json_blob(text: str):
    # Be lenient: strip fences, grab the outermost {...}.
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2021-01-01")
    ap.add_argument("--until", default=dt.date.today().isoformat())
    ap.add_argument("--handle", default=os.getenv("JOSCHA_X_HANDLE", "Plinz"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if load_dotenv:
        load_dotenv(PROJECT / ".env")
    key = os.getenv("XAI_API_KEY", "").strip()

    since = dt.date.fromisoformat(args.since)
    until = dt.date.fromisoformat(args.until)
    plan = [(t, fd, td) for t in TOPICS for (fd, td) in windows(since, until)]

    print(f"Joscha ingestion plan: handle=@{args.handle}, "
          f"{len(TOPICS)} topics x date windows = {len(plan)} searches "
          f"({args.since} → {args.until}).")
    if args.dry_run:
        for t, fd, td in plan[:6]:
            print(f"  - [{fd}..{td}] {t}")
        print("  ... (--dry-run: no API calls made)")
        return
    if not key:
        sys.exit("ERROR: XAI_API_KEY is empty. Paste your key into ../.env and re-run.")
    if OpenAI is None:
        sys.exit("ERROR: `openai` not installed. Run: pip install -r requirements.txt")

    client = OpenAI(api_key=key, base_url=XAI_BASE)
    (OUT / "xposts").mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    seen_urls, all_terms = set(), []
    for i, (topic, fd, td) in enumerate(plan, 1):
        print(f"[{i}/{len(plan)}] {topic}  [{fd}..{td}]")
        try:
            text = call_grok(client, args.handle, topic, fd, td)
        except Exception as e:  # noqa: BLE001
            print(f"   ! API error: {e}")
            continue
        (RAW / f"{slugify(topic)}-{fd}.json").write_text(text, encoding="utf-8")
        data = parse_json_blob(text)
        if not data:
            print("   ! could not parse JSON; raw saved for review")
            continue
        for p in data.get("xposts", []):
            url = (p.get("url") or "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            rec = {
                "title": p.get("title", "").strip(),
                "url": url,
                "date": p.get("date"),
                "excerpt": p.get("excerpt", "").strip(),
                "source_host": "x.com",
                "handle": p.get("handle", args.handle),
                "thread_id": p.get("thread_id"),
            }
            slug = slugify((rec["date"] or "") + "-" + rec["title"])
            (OUT / "xposts" / f"{slug}.json").write_text(
                json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
        all_terms.extend(data.get("terms", []))

    # Dedup terms by lowercased title.
    by_title = {}
    for t in all_terms:
        key_t = (t.get("title") or "").strip().lower()
        if key_t and key_t not in by_title:
            by_title[key_t] = t
    (OUT / "terms_candidates.json").write_text(
        json.dumps(list(by_title.values()), indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nDone. {len(seen_urls)} unique xposts → {OUT/'xposts'}; "
          f"{len(by_title)} candidate terms → {OUT/'terms_candidates.json'}.")
    print("Next: run the site scaffold/build step in ../BUILD-JOSCHA.md.")


if __name__ == "__main__":
    main()
