---
district: thinker-sites
status: active
depends_on: [Levinese, SOMA]
capabilities: [astro, netlify, auth, xai]
last_reviewed: 2026-06-23
---

# Joscha (Joschese) — a field guide to Joscha Bach's ideas (Levinese clone whose corpus is X threads + talks, not papers)

**Where work happens:** `ingest/pull_joscha_x.py` (xAI `x_search` → `ingest/out/xposts/*.json` + `terms_candidates.json`) · `src/content/{xposts,videos,terms}` (the spine; `papers` de-emphasized) · `src/pages` + `src/layouts` · `public/joscha-guide-config.js` (Joscha-grounded AI guide)

**Key docs** (read in this order):
- [BUILD-JOSCHA.md](BUILD-JOSCHA.md) — the spec: ingest → scaffold-from-Levinese → guide → deploy; also the program plan for Friston/Fields.
- [BUILD-REPORT.md](BUILD-REPORT.md) — what the v0 worker actually built.
- [.grok-task.md](.grok-task.md) — the headless worker brief (no-deploy/no-push constraints).

**Skills**
- gap: same thinker-site ingest/scaffold spine as Levinese — author once, share.

**Depends on / used by:** scaffolded from `Levinese` (same Astro/Tailwind template, guide widget, SomaAuth from SOMA). Ingestion needs xAI/Grok.

**Live site + hub:** this IS the canonical live Joscha Bach ("Joschese") site for AGI-2026 → **joschese.netlify.app** (linked from the hub roster at agi2026.netlify.app). `src/layouts/Base.astro` carries a "← Back to AGI 2026" bar; keep it pointing at agi2026.netlify.app. Git remote is **github.com/eldrgeek/joschese** and GitHub CD is wired (2026-07-05) — `git push origin master` auto-deploys. To (re)wire CD use the `netlify-deploy` skill (expect recipe; never pipe input into `netlify init`).

**Gotchas**
- BLOCKED on `XAI_API_KEY`: `.env` currently only holds leftover `PUBLIC_LEVIN_ASK_*` tokens — no Grok key, so `pull_joscha_x.py` cannot run real ingestion. Paste the key into `.env` first.
- Build is two-step like Levinese (`aggregate-content.mjs` then `astro build`); Cowork Linux sandbox can't build Astro against the macOS node_modules — build on the Mac.
- The `.grok-task.md` "no deploy / no push / no new site" rule was the *original headless-worker* constraint; superseded 2026-07-05 — the repo now has a remote and live CD (Mike authorized). Normal push/deploy is fine now.
