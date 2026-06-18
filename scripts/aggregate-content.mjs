#!/usr/bin/env node
// Pre-build aggregation for client-side MiniSearch.
//  - src/content/papers/*.json   → src/data/papers.json
//  - src/content/{xposts,videos,blog,magazine,substack}/*.json
//                                → src/data/corpus-non-papers.json
// The corpus page imports both and feeds them to MiniSearch. Without this,
// non-paper items (e.g. the X corpus) render as DOM rows but are invisible to
// search. ids here MUST match the corpus row ids (the filename slug).

import { readdirSync, readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const root = new URL('..', import.meta.url).pathname;
const contentDir = join(root, 'src/content');

function readColl(name) {
  const dir = join(contentDir, name);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter(f => f.endsWith('.json'))
    .sort()
    .map(f => ({ slug: f.replace(/\.json$/, ''), data: JSON.parse(readFileSync(join(dir, f), 'utf8')) }));
}

// ── papers.json (unchanged behaviour) ──────────────────────────────────────
const papers = readColl('papers').map(({ slug, data }) => ({ slug, ...data }));
writeFileSync(join(root, 'src/data/papers.json'), JSON.stringify(papers, null, 2));
console.log(`Aggregated ${papers.length} papers → src/data/papers.json`);

// ── corpus-non-papers.json (search index for everything else) ──────────────
const NON_PAPER = ['xposts', 'videos', 'blog', 'magazine', 'substack'];
const TYPE = { xposts: 'xpost', videos: 'video', blog: 'blog', magazine: 'magazine', substack: 'substack' };

const nonPapers = [];
for (const coll of NON_PAPER) {
  for (const { slug, data } of readColl(coll)) {
    nonPapers.push({
      id: slug,                 // matches the corpus row id (item.slug)
      type: TYPE[coll],
      title: data.title ?? '',
      excerpt: data.excerpt ?? '',
    });
  }
}
writeFileSync(join(root, 'src/data/corpus-non-papers.json'), JSON.stringify(nonPapers, null, 2));
console.log(`Aggregated ${nonPapers.length} non-paper items → src/data/corpus-non-papers.json`);
