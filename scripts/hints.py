#!/usr/bin/env python3
"""Per-page terminology hints from OrcaSlicer's own zh_CN UI translation and the wiki glossary.

usage: hints.py <wiki_src_dir> <po_file> <work_dir>
writes work/hints/<page>.txt and work/terms.json (normalized english -> [zh, ...])
"""
import json
import pathlib
import re
import sys
from collections import Counter

SRC = pathlib.Path(sys.argv[1]).resolve()
PO = pathlib.Path(sys.argv[2]).resolve()
WORK = pathlib.Path(sys.argv[3]).resolve()


def parse_po(path):
    entries, cur, key = [], {}, None
    fuzzy = False
    for line in path.read_text(encoding='utf-8').split('\n'):
        if line.startswith('#,') and 'fuzzy' in line:
            fuzzy = True
        elif line.startswith('msgctxt '):
            if cur.get('msgstr') is not None:
                entries.append((cur, fuzzy)); fuzzy = False
            cur, key = {'msgctxt': line[8:].strip()[1:-1]}, 'msgctxt'
        elif line.startswith('msgid '):
            if cur.get('msgstr') is not None:
                entries.append((cur, fuzzy)); fuzzy = False
                cur = {}
            cur['msgid'], key = line[6:].strip()[1:-1], 'msgid'
        elif line.startswith('msgstr '):
            cur['msgstr'], key = line[7:].strip()[1:-1], 'msgstr'
        elif line.startswith('"') and key:
            cur[key] = cur.get(key, '') + line.strip()[1:-1]
    if cur.get('msgstr') is not None:
        entries.append((cur, fuzzy))
    out = []
    for e, fz in entries:
        mid, mstr = e.get('msgid', ''), e.get('msgstr', '')
        if not mid or not mstr or fz:
            continue
        mid = mid.replace('\\"', '"').replace('\\n', ' ').strip()
        mstr = mstr.replace('\\"', '"').replace('\\n', ' ').strip()
        out.append((mid, mstr))
    return out


def norm(s):
    s = s.replace('&', '').strip().rstrip(':').strip()
    return re.sub(r'\s+', ' ', s).lower()


terms = {}   # norm english -> Counter of zh
source = {}  # norm english -> 'ui' / 'glossary'
for mid, mstr in parse_po(PO):
    if re.search(r'%|\{\}|\\t|<|>', mid):
        continue
    n = norm(mid)
    words = n.split()
    if not (1 <= len(words) <= 7) or len(n) < 3:
        continue
    terms.setdefault(n, Counter())[mstr.rstrip('：:').strip()] += 1
    source.setdefault(n, 'ui')

gl = SRC / 'developer_reference' / 'glossary' / 'zh_CN.tsv'
for row in gl.read_text(encoding='utf-8-sig').split('\n')[1:]:
    parts = row.split('\t')
    if len(parts) >= 3 and parts[0].strip() and parts[2].strip():
        n = norm(parts[0])
        terms.setdefault(n, Counter())[parts[2].strip()] += 5
        source[n] = 'glossary'

(WORK / 'terms.json').write_text(json.dumps({k: [z for z, _ in v.most_common()] for k, v in terms.items()},
                                            ensure_ascii=False), encoding='utf-8')
maxlen = 7
for f in sorted((WORK / 'en').rglob('*.md')):
    rel = f.relative_to(WORK / 'en')
    text = f.read_text(encoding='utf-8')
    meta = json.loads((WORK / 'meta' / rel.with_suffix('.json')).read_text(encoding='utf-8'))
    heads = {norm(re.sub(r'\s*\((beta|experimental)\)\s*$', '', h['en'], flags=re.I)) for h in meta['headings']}
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", re.sub(r'\{\{[A-Z]\d+\}\}', ' ', text).lower())
    found = Counter()
    for i in range(len(words)):
        for L in range(maxlen, 0, -1):
            if i + L > len(words):
                continue
            g = ' '.join(words[i:i + L])
            if g in terms:
                found[g] += 1
    picked = []
    for g, c in found.items():
        single = len(g.split()) == 1
        if single and source.get(g) != 'glossary' and g not in heads:
            continue
        if not single and c < 1:
            continue
        score = (g in heads) * 1000 + (source.get(g) == 'glossary') * 100 + len(g.split()) * 10 + min(c, 9)
        picked.append((score, g))
    picked.sort(reverse=True)
    lines = []
    for _, g in picked[:90]:
        zh = ' / '.join(z for z, _ in terms[g].most_common(2))
        tag = 'H' if g in heads else ('G' if source.get(g) == 'glossary' else '')
        lines.append(f'{tag:1s} {g} = {zh}')
    out = WORK / 'hints' / rel.with_suffix('.txt')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('terms:', len(terms))
