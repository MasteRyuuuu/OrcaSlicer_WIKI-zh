#!/usr/bin/env python3
"""Validate translated pages against their prepared English source.

usage: check.py [page ...]     (default: every file under zh/)
Reports per page: placeholder mismatches, heading structure mismatches, leftover English.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import PH, headings_of

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZH, EN, META = ROOT / 'zh', ROOT / 'work' / 'en', ROOT / 'work' / 'meta'
SUMMARY_MARK = '<!-- summary -->'


def leftover_english(text):
    """Lines that still look like untranslated English prose."""
    bad = []
    lines = text.split('\n')
    skip = False
    for line in lines:
        if re.match(r'^\s*(?:>\s*)?(`{3,}|~{3,}|\$\$)', line):
            skip = not skip
            continue
        if skip:
            continue
        t = PH.sub(' ', line)
        t = re.sub(r'`[^`]*`', ' ', t)
        t = re.sub(r'\$[^$]*\$', ' ', t)
        t = re.sub(r'\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', ' ', t)
        t = re.sub(r'<[^>]+>', ' ', t)
        cjk = len(re.findall(r'[一-鿿]', t))
        words = re.findall(r'[A-Za-z]{3,}', t)
        if len(words) >= 6 and cjk < len(words):
            bad.append(line.strip()[:90])
    return bad


def check(rel):
    zh = (ZH / rel).read_text(encoding='utf-8')
    en = (EN / rel).read_text(encoding='utf-8')
    problems = []
    if zh.startswith(SUMMARY_MARK):
        # release-note summary: free structure; only unknown placeholders and leftover English matter
        pe = {m.group(0) for m in PH.finditer(en)}
        extra = sorted({m.group(0) for m in PH.finditer(zh)} - pe)
        if extra:
            problems.append('unknown ' + ' '.join(extra))
        left = leftover_english(zh)
        if left:
            problems.append(f'{len(left)} english-looking lines, e.g. «{left[0]}»')
        meta = json.loads((META / pathlib.Path(rel).with_suffix('.json')).read_text(encoding='utf-8'))
        return problems, len(meta['headings'])
    pe = [m.group(0) for m in PH.finditer(en)]
    pz = [m.group(0) for m in PH.finditer(zh)]
    missing = sorted(set(pe) - set(pz), key=lambda x: (x[2], int(x[3:-2])))
    extra = sorted(set(pz) - set(pe))
    dup = sorted({p for p in pz if pz.count(p) > 1 and pe.count(p) == 1})
    if missing:
        problems.append('missing ' + ' '.join(missing))
    if extra:
        problems.append('unknown ' + ' '.join(extra))
    if dup:
        problems.append('duplicated ' + ' '.join(dup))
    # placeholders that stood alone on a line must still stand alone
    alone_en = {m.group(1) for m in re.finditer(r'^\s*(\{\{[CMT]\d+\}\})\s*$', en, re.M)}
    alone_zh = {m.group(1) for m in re.finditer(r'^\s*(\{\{[CMT]\d+\}\})\s*$', zh, re.M)}
    if alone_en - alone_zh:
        problems.append('not on own line ' + ' '.join(sorted(alone_en - alone_zh)))
    he = [lv for lv, _ in headings_of(en)]
    hz = [lv for lv, _ in headings_of(zh)]
    if he != hz:
        k = next((i for i, (a, b) in enumerate(zip(he, hz)) if a != b), min(len(he), len(hz)))
        problems.append(f'headings differ: en {len(he)} zh {len(hz)}, first mismatch at #{k + 1}')
    left = leftover_english(zh)
    if left:
        problems.append(f'{len(left)} english-looking lines, e.g. «{left[0]}»')
    meta = json.loads((META / pathlib.Path(rel).with_suffix('.json')).read_text(encoding='utf-8'))
    return problems, len(meta['headings'])


def main():
    rels = [a if a.endswith('.md') else a + '.md' for a in sys.argv[1:]] or \
        sorted(str(p.relative_to(ZH)) for p in ZH.rglob('*.md'))
    bad = 0
    for rel in rels:
        if not (ZH / rel).exists():
            print(f'-- {rel}: not translated yet')
            continue
        probs, _ = check(rel)
        if probs:
            bad += 1
            print(f'!! {rel}')
            for p in probs:
                print('     ' + p)
    done = len(list(ZH.rglob('*.md')))
    total = len(list(EN.rglob('*.md')))
    print(f'{len(rels) - bad}/{len(rels)} checked pages OK; {done}/{total} pages translated overall')


if __name__ == '__main__':
    main()
