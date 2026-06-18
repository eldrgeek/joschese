# Joscha Bach thinker-site — build brief & program plan

A "Levinese for Joscha." Same architecture as `~/Projects/Levinese` (Astro +
Tailwind, Netlify, the shared SOMA Guide widget). The differences are all about
**source material**: Levin's corpus is journal papers; Joscha's is X threads,
podcasts, and talks. The Levinese content model already anticipates this — it
has an `xposts` collection — so the template fits with almost no schema change.

---

## Status (set 2026-06-18, in Cowork)

- ✅ Ingestion pipeline written and dry-run-verified: `ingest/pull_joscha_x.py`
  (uses xAI `x_search`, emits the Levinese `xposts` + `terms` schema).
- ⏳ **Blocked on**: `XAI_API_KEY` in `.env` (paste it), then run ingestion.
- ⏳ Site scaffold + build + deploy: do via a worker on the Mac (the Cowork
  Linux sandbox can't build Astro against macOS-installed node_modules).

---

## Step 1 — Ingest Joscha's content (needs the Grok key)

```bash
cd ~/Projects/Joscha/ingest
pip install -r requirements.txt
# ensure XAI_API_KEY is set in ~/Projects/Joscha/.env
python pull_joscha_x.py            # ~60 searches; writes ingest/out/
```

Produces `ingest/out/xposts/*.json` and `ingest/out/terms_candidates.json`.

> Alternative worker path Mike flagged: **Grok Build** (xAI's terminal coding
> agent, on his SuperGrok/X Premium+ subscription — `~/.grok-build/`). Because
> Grok has native X access, a Grok Build run can do ingestion AND scaffolding in
> one headless session (`docs.x.ai/build/cli/headless-scripting`). Either path
> yields the same `ingest/out/` content; pick one.

## Step 2 — Scaffold the site from the Levinese template

Worker prompt (works for Grok Build, `claude -p`, or cc-dispatch):

> Clone the structure of `~/Projects/Levinese` into `~/Projects/Joscha` WITHOUT
> its content. Copy: `src/layouts`, `src/components`, `src/pages`,
> `src/content/config.ts`, `astro.config.mjs`, `tailwind.config.mjs`,
> `tsconfig.json`, `netlify.toml`, `package.json`, `scripts/`, `public/`
> (excluding `public/levinese-guide-config.js`). Do NOT copy `node_modules`,
> `dist`, `.astro`, `.git`, `.netlify`, `src/content/{papers,videos,blog,magazine,substack,terms,xposts}` data files.
>
> Then Joscha-ize:
> - Rename brand "Levinese" → the Joscha site name (Mike to confirm wordmark;
>   working title **"Joschese — a field guide to Joscha Bach's ideas"**).
> - Rewrite home/`index.astro`, `colophon`, and nav copy for Joscha.
> - The site's spine is **xposts** (primary) + **videos** (talks/podcasts) +
>   **terms** (dictionary) + **atlas**. De-emphasize the `papers` collection
>   (Joscha has few formal papers) — keep the corpus page but source it from
>   xposts/videos. Keep `ask/` and the guide widget.
> - Drop `ingest/out/xposts/*.json` into `src/content/xposts/`.
> - Seed `src/content/terms/*.md` from `ingest/out/terms_candidates.json`
>   (one markdown file per term, frontmatter matching the Levinese `terms`
>   schema: letter, title, authored_by: "Joscha Bach", source, provenance[],
>   related[], tags[]).
> - Run `npm install`, then `npm run build`. Fix all type/content-schema errors
>   until the build passes.

## Step 3 — Guide persona for Joscha

Create `public/joscha-guide-config.js` modeled on the new
`Levinese/public/levinese-guide-config.js` (Levin guide). Same framing rule:
the guide is an **AI guide grounded in Joscha's public corpus**, not Joscha
himself. Give it a Joscha-appropriate ConvAI agent + voice:
- If a `joscha` persona exists on the SOMA Campus (`~/Projects/SOMA/personas/`,
  `FrontRow/.../office/src/data/personas.ts`), reuse its `convaiAgentId`.
- Otherwise create one with the proven ElevenLabs ConvAI recipe in
  `~/Projects/SOMA/audits/20260617T221216Z-campus-convai.md` (public agent,
  `eleven_turbo_v2`, a concise persona prompt + the no-tasks guardrail), and a
  fitting voice (e.g. a crisp, fast, German-inflected register).

Wire it into the Joscha `Base.astro` exactly like Levinese (incl. the SomaAuth
visitor-auth block for a persistent relationship — copy `public/js/soma-auth*.js`
and the head scripts from the updated Levinese `Base.astro`).

## Step 4 — Deploy

New Netlify site (suggest `joschese` / `joscha-bach`). `netlify.toml` already
has the right build command + SPA fallback. **Get Mike's go-ahead before
creating the site / first deploy** (new public site = explicit-permission).

---

## Program plan — the other thinkers

| Thinker | Primary sources | Pipeline | Notes |
|---|---|---|---|
| **Joscha Bach** | X (@Plinz), podcasts, talks | `x_search` (this repo) | first; X-heavy |
| **Karl Friston** | journal papers (huge), talks | Levin-style paper pipeline (`SOMA/coach/levin_*.py`) + DOI fetch | free-energy principle / active inference; mostly formal papers — closest to the Levin template |
| **Chris Fields** | papers + preprints, some talks | same paper pipeline | quantum information / cognition; arXiv-heavy |

Reusable spine for every site:
1. **Source adapter** (papers via DOI/arXiv, or X via `x_search`, or YouTube
   transcripts) → normalized into the Astro collections (`papers|videos|xposts`).
2. **Dictionary builder** — extract each thinker's coined/repurposed terms with
   provenance (the `terms` collection).
3. **Atlas** — concept graph (`scripts/build_atlas.py` from Levinese).
4. **Guide** — per-site `*-guide-config.js`, an AI guide grounded in that
   thinker's corpus (never impersonating the living person), + SomaAuth.
5. **Deploy** — Netlify, one site each.

Next after Joscha: **Friston** (reuses the Levin paper pipeline almost verbatim —
swap the author and DOIs), then **Fields**.
