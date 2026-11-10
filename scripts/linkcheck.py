#!/usr/bin/env python3
"""Check the built site: every internal #link resolves, element ids are unique, every image exists.
usage: linkcheck.py        (reads site/index.html; exit 1 when something is broken)"""
import collections
import json
import pathlib
import re
import sys
from urllib.parse import unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'


def main():
    html = (SITE / 'index.html').read_text(encoding='utf-8')
    data = json.loads(re.search(r'<script[^>]*id="wiki-data"[^>]*>(.*?)</script>', html, re.S).group(1))
    page_ids = {p['id'] for p in data['pages']}
    ids = collections.Counter()
    for p in data['pages']:
        ids.update(re.findall(r'\bid="([^"]+)"', p['h']))
    broken, images = [], []
    for p in data['pages']:
        for href in re.findall(r'\bhref="#([^"]*)"', p['h']):
            t = unquote(href)
            if t and t not in page_ids and t not in ids:
                broken.append(f'{p["id"]} -> #{t}')
        tags = re.findall(r'<(?:img|source|video)\b[^>]*>', p['h'])
        for src in (s for tag in tags for s in re.findall(r'\s(?:data-)?src="([^"]+)"', tag)):
            if src.startswith(('data:', 'http://', 'https://')) or src in data['inline']:
                continue
            if not (SITE / src).is_file():
                images.append(f'{p["id"]} -> {src}')
    dups = sorted(i for i, n in ids.items() if n > 1)
    print(f'pages {len(page_ids)}  broken links {len(broken)}  duplicate ids {len(dups)}  missing images {len(images)}')
    for x in broken[:40] + [f'dup id {d}' for d in dups[:20]] + images[:40]:
        print('  ' + x)
    return 1 if broken or dups or images else 0


if __name__ == '__main__':
    sys.exit(main())
