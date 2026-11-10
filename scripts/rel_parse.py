#!/usr/bin/env python3
"""Parse a prepared English release-notes page into: headings, section prose, bullet items (title + PR links).
usage: rel_parse.py <key>   -> writes work/rel/<key>.json and prints a numbered outline
(the outline numbers are the TSV keys used by rel_build.py: S<i> heading, P<i>.<j> prose, <n> item)"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def parse(text):
    secs = []   # each: {level, title, prose:[para], items:[{title, rest, links}]}
    cur, para, in_item = None, [], False

    def flush_para():
        nonlocal para
        if para and cur is not None:
            p = ' '.join(x.strip() for x in para).strip()
            if p:
                cur['prose'].append(p)
        para = []

    for ln in text.split('\n'):
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            flush_para()
            in_item = False
            cur = {'level': len(m.group(1)), 'title': m.group(2).strip(), 'prose': [], 'items': []}
            secs.append(cur)
            continue
        if cur is None:
            continue
        mi = re.match(r'^\*\s+\*\*(.+?)\*\*\s*(.*)$', ln)
        if mi:
            flush_para()
            in_item = True
            rest = mi.group(2)
            links = re.findall(r'\[([^\]]+)\]\((\{\{L\d+\}\})\)', rest)
            cur['items'].append({'title': mi.group(1), 'rest': rest, 'links': links})
            continue
        if in_item:
            # indented continuation of an item (description, images) — skipped in summaries
            if ln.startswith('    ') or not ln.strip():
                continue
            in_item = False
        if not ln.strip():
            flush_para()
            continue
        if ln.startswith('>') or ln.startswith('<') or ln.strip() == '---':
            flush_para()
            continue
        para.append(ln)
    flush_para()
    return secs


def outline(secs):
    n = 0
    for si, s in enumerate(secs):
        print(f'S{si} {"#" * s["level"]} {s["title"]}')
        for p in s['prose']:
            print(f'   P: {p}')
        for it in s['items']:
            n += 1
            print(f'   {n}. {it["title"]}')


def main():
    key = sys.argv[1]
    secs = parse((ROOT / 'work/en/releases' / f'{key}.md').read_text(encoding='utf-8'))
    (ROOT / 'work/rel').mkdir(exist_ok=True)
    (ROOT / 'work/rel' / f'{key}.json').write_text(json.dumps(secs, ensure_ascii=False, indent=1),
                                                   encoding='utf-8')
    outline(secs)


if __name__ == '__main__':
    main()
