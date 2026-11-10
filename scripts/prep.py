#!/usr/bin/env python3
"""Turn each English wiki page into a translation-ready file.

Non-translatable spans (code blocks, images, link targets, bare URLs, generated option
metadata lines, in-page tables of contents) become short placeholders such as {{L3}}.
The originals are stored in work/meta/<page>.json so build.py can restore them.

usage: prep.py <wiki_src_dir> <work_dir>
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import (SKIP_DIRS, SKIP_FILES, META, TOCLINE, LISTLINE, iter_fenced,
                    headings_of, assign_slugs)

SRC = pathlib.Path(sys.argv[1]).resolve()
WORK = pathlib.Path(sys.argv[2]).resolve()

IMG_MD = re.compile(r'!\[[^\]]*\]\(\s*<?[^)\s>]*>?(?:\s+"[^"]*")?\s*\)')
IMG_HTML = re.compile(r'<img\b[^>]*>', re.I)
LINK_T = re.compile(r'\]\(\s*(<[^>]*>|[^()\s]*(?:\([^()\s]*\)[^()\s]*)*)(\s+"[^"]*")?\s*\)')
ATTR_URL = re.compile(r'\b(href|src)\s*=\s*"([^"]*)"', re.I)
BARE = re.compile(r'(?<![\w/"\'(<=\]])(https?://[^\s<>()\[\]"\'`]+)')
CODESPAN = re.compile(r'(`+)(.+?)\1')


def prep(text):
    text = text.lstrip('﻿').replace('\r\n', '\n').replace('\r', '\n')
    heads = assign_slugs(headings_of(text))
    lines = text.split('\n')

    # 1. fenced code -> {{Cn}} (mermaid kept visible so its labels can be translated)
    codes, out, keep = [], [], []
    blocks = {s: (e, ind, info) for s, e, ind, info in iter_fenced(lines)}
    i = 0
    while i < len(lines):
        if i in blocks:
            e, ind, info = blocks[i]
            blk = lines[i:e + 1]
            if info.lower().startswith('mermaid'):
                keep.append(len(out))
                out.extend(blk)
                keep.append(len(out) - 1)
            else:
                codes.append(blk)
                out.append(f'{ind}{{{{C{len(codes)}}}}}')
            i = e + 1
        else:
            out.append(lines[i])
            i += 1
    text = '\n'.join(out)

    # 2. drop HTML comments
    text = re.sub(r'<!--[\s\S]*?-->\n?', '', text)
    lines = text.split('\n')

    # 3. option metadata runs -> {{Mn}};  in-page TOC lists -> {{Tn}}
    metas, tocs, out = [], [], []
    i = 0
    while i < len(lines):
        m = META.match(lines[i])
        if m:
            run = []
            while i < len(lines) and META.match(lines[i]):
                mm = META.match(lines[i])
                run.append({'label': mm.group(2), 'target': mm.group(3), 'value': mm.group(4)})
                i += 1
            metas.append(run)
            out.append(f'{m.group(1)}{{{{M{len(metas)}}}}}')
            continue
        if LISTLINE.match(lines[i]) and (i == 0 or not lines[i - 1].strip() or not LISTLINE.match(lines[i - 1])):
            j = i
            while j < len(lines) and lines[j].strip() and LISTLINE.match(lines[j]):
                j += 1
            run = lines[i:j]
            if len(run) >= 2 and all(TOCLINE.match(x) for x in run):
                items = []
                for x in run:
                    tm = TOCLINE.match(x)
                    items.append({'indent': len(tm.group(1).expandtabs(4)), 'anchor': tm.group(3), 'en': tm.group(2)})
                tocs.append(items)
                out.append(f'{{{{T{len(tocs)}}}}}')
                i = j
                continue
        out.append(lines[i])
        i += 1
    lines = out

    # 4. inline spans outside mermaid blocks
    imgs, links, urls = [], [], []

    def sub_inline(seg):
        spans = []
        seg = CODESPAN.sub(lambda m: (spans.append(m.group(0)), f'\x01{len(spans) - 1}\x01')[1], seg)

        def img(m):
            imgs.append(m.group(0))
            return f'{{{{I{len(imgs)}}}}}'
        seg = IMG_HTML.sub(img, seg)
        seg = IMG_MD.sub(img, seg)

        def lnk(m):
            t = m.group(1).strip()
            if t.startswith('<') and t.endswith('>'):
                t = t[1:-1]
            links.append(t)
            return f']({{{{L{len(links)}}}}})'
        seg = LINK_T.sub(lnk, seg)

        def attr(m):
            links.append(m.group(2))
            return f'{m.group(1)}="{{{{L{len(links)}}}}}"'
        seg = ATTR_URL.sub(attr, seg)

        def bare(m):
            u = m.group(1)
            tail = ''
            while u and u[-1] in '.,;:!?*':
                tail = u[-1] + tail
                u = u[:-1]
            urls.append(u)
            return f'{{{{U{len(urls)}}}}}{tail}'
        seg = BARE.sub(bare, seg)
        return re.sub('\x01(\\d+)\x01', lambda m: spans[int(m.group(1))], seg)

    # mermaid regions are pairs of (start, end) indexes in `keep` (pre-step-3 numbering may shift,
    # so re-detect them here)
    res, i = [], 0
    while i < len(lines):
        if re.match(r'^\s*(`{3,}|~{3,})\s*mermaid', lines[i], re.I):
            j = i + 1
            while j < len(lines) and not re.match(r'^\s*(`{3,}|~{3,})\s*$', lines[j]):
                j += 1
            res.extend(lines[i:j + 1])
            i = j + 1
            continue
        res.append(lines[i])
        i += 1
    # process non-mermaid text in paragraph-sized chunks so code spans never cross blocks
    final, buf, inmer = [], [], False
    for line in res:
        if re.match(r'^\s*(`{3,}|~{3,})\s*mermaid', line, re.I):
            final.append(sub_inline('\n'.join(buf))) if buf else None
            buf, inmer = [], True
            final.append(line)
            continue
        if inmer:
            final.append(line)
            if re.match(r'^\s*(`{3,}|~{3,})\s*$', line):
                inmer = False
            continue
        buf.append(line)
    if buf:
        final.append(sub_inline('\n'.join(buf)))
    text = '\n'.join(final)
    text = re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'

    meta = {'code': codes, 'meta': metas, 'toc': tocs, 'img': imgs, 'link': links,
            'url': urls, 'headings': heads}
    return text, meta


def main():
    pages = []
    for f in sorted(SRC.rglob('*.md')):
        rel = f.relative_to(SRC)
        if rel.parts[0] in SKIP_DIRS or (len(rel.parts) == 1 and rel.name in SKIP_FILES):
            continue
        text, meta = prep(f.read_text(encoding='utf-8'))
        meta['src'] = str(rel)
        for sub, data in (('en', text), ('meta', json.dumps(meta, ensure_ascii=False, indent=0))):
            p = WORK / sub / (rel.with_suffix('.json') if sub == 'meta' else rel)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(data, encoding='utf-8')
        pages.append((str(rel), len(text), len(meta['headings'])))
    print(f'{len(pages)} pages prepared')
    tot = sum(p[1] for p in pages)
    print(f'prepared chars total: {tot}')


if __name__ == '__main__':
    main()
