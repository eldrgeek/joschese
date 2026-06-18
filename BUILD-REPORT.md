# Joschese build report — 2026-06-18

## Summary

Built **Joschese** — a field guide to Joscha Bach's ideas — as a local Astro site scaffolded from Levinese. Ingestion, content seeding, guide config, and production build all completed. **No deploy, no git push, no Netlify site created.**

## What was built

| Component | Status |
|-----------|--------|
| X corpus ingestion (`ingest/pull_joscha_x.py`) | ✅ 60/60 searches completed |
| Astro site scaffold (Levinese template) | ✅ |
| `src/content/xposts/` | ✅ 298 JSON files |
| `src/content/terms/` | ✅ 60 markdown entries |
| `public/joscha-guide-config.js` | ✅ text-only guide (voice TODO) |
| SomaAuth wiring (`public/js/soma-auth*.js` + Base.astro) | ✅ |
| `npm run build` | ✅ passes (8 pages, ~1.8s) |
| Local git init + commit | ✅ |

## File counts

- **xposts**: 298 unique posts (from @Plinz, 2021–2026)
- **terms**: 60 dictionary entries (`authored_by: "Joscha Bach"`)
- **papers**: 0 (de-emphasized per spec)
- **videos**: 0 (placeholder collection; talks to be ingested in v1)
- **pages built**: 8 (`/`, `/dictionary/`, `/corpus/`, `/atlas/`, `/ask/`, `/colophon/`, `/collaborators/`, `/transcript-coming-soon/`)

## Build result

```
npm run build
→ Aggregated 0 papers → src/data/papers.json
→ 8 page(s) built in 1.83s
→ [build] Complete!
```

Warnings during build are expected: empty `papers`, `videos`, `blog`, `magazine`, `substack` collections log Astro notices but do not fail the build.

## Suggested Netlify site name (NOT created)

**`joschese`** (alt: `joscha-bach`)

`netlify.toml` is ready with `npm run build` + SPA fallback. Awaiting Mike's explicit go-ahead before `netlify init` or first deploy.

## Left for Mike

1. **Deploy** — say the word; suggest site name `joschese.netlify.app`
2. **ConvAI voice agent** — no `joscha` persona found in SOMA Campus / FrontRow. `joscha-guide-config.js` has `voiceAgentId: null` with TODO. Create agent per `SOMA/audits/20260617T221216Z-campus-convai.md` recipe, then wire the ID.
3. **Atlas** — `src/data/atlas.json` is a v0 stub (empty points). Run `scripts/build_atlas.py` locally (needs ML deps) once terms stabilize.
4. **Videos / talks** — ingest YouTube/podcast transcripts into `src/content/videos/` (Joscha's secondary corpus spine)
5. **Corpus search** — `corpus-non-papers.json` is empty; MiniSearch won't index xposts client-side until aggregated (DOM rows still render)
6. **Collaborators page** — still Levin template copy at `/collaborators/`; removed from nav but page remains
7. **Wordmark confirmation** — working title "Joschese — a field guide to Joscha Bach's ideas" used throughout

## Local dev

```bash
cd ~/Projects/Joscha
npm run dev      # preview at localhost:4321
npm run build    # production build → dist/
```

## Git

Local repo initialized on `master`. `.env` is gitignored and was never committed.