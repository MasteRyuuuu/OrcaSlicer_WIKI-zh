#!/usr/bin/env python3
"""Assemble a Chinese release-notes summary page from work/rel/<key>.json + work/rel/<key>.zh.tsv.
TSV keys: S<i> heading, P<i>.<j> prose paragraph, <n> item title. Writes zh/releases/<key>.md"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
GH = 'https://github.com/OrcaSlicer/OrcaSlicer/wiki/'
key = sys.argv[1]
secs = json.loads((ROOT / 'work/rel' / f'{key}.json').read_text(encoding='utf-8'))
tr = {}
for line in (ROOT / 'work/rel' / f'{key}.zh.tsv').read_text(encoding='utf-8').split('\n'):
    if line.strip():
        k, v = line.split('\t', 1)
        tr[k.strip()] = v.strip().replace('\\n', '\n')
en_text = (ROOT / 'work/en/releases' / f'{key}.md').read_text(encoding='utf-8')
support_html = [l for l in en_text.split('\n') if re.match(r'^\s*(<p\b|</p>|<a\b)', l)]
SUPPORT = ('> **OrcaSlicer 是、并将一直是免费的开源软件。**\n>\n'
           '> 每一次发布背后都有大量幕后工作：开发功能、修复错误、验证配置，并在真实的机器上测试。\n>\n'
           '> 如果 OrcaSlicer 帮助你把想法变成现实，请考虑支持这个项目。捐款用于支持帮助构建和维护 OrcaSlicer 的开源贡献者，'
           '以及支付服务器、开发工具、测试机器、耗材丝、打印机零件和其他基础设施等项目开支。\n>\n'
           '> 你的支持帮助我们为所有人持续改进 OrcaSlicer，同时让这个项目保持免费、开放、由社区驱动。\n>\n'
           '> **感谢你参与 OrcaSlicer 的旅程。** 🙏')
out = ['<!-- summary -->']
n = 0
missing = []
for si, s in enumerate(secs):
    title = tr.get(f'S{si}')
    if title is None:
        missing.append(f'S{si}')
        title = s['title']
    if si == 0:
        out += [f'# {title}', '',
                '> [!NOTE]',
                f'> 中文版翻译了版本概述和每一项更新的标题。每项更新的详细说明、贡献者和截图，请查看[英文原文]({GH}{key})。',
                '']
    else:
        lv = min(s['level'] + 1, 6)
        out += [f'{"#" * lv} {title} [[en:{s["title"]}]]', '']
    if 'Support OrcaSlicer' in s['title']:
        out += [SUPPORT, ''] + support_html + ['']
        continue
    for pj, p in enumerate(s['prose']):
        k = f'P{si}.{pj}'
        if p.startswith('<'):
            out += [p, '']
            continue
        if k not in tr:
            missing.append(k)
        out += [tr.get(k, p), '']
    if s['items']:
        for it in s['items']:
            n += 1
            t = tr.get(str(n))
            if t is None:
                missing.append(str(n))
                t = it['title']
            links = '、'.join(f'[{a}]({b})' for a, b in it['links'])
            out.append(f'- **{t}**' + (f'（{links}）' if links else ''))
        out.append('')
text = '\n'.join(out).rstrip() + '\n'
dst = ROOT / 'zh/releases' / f'{key}.md'
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(text, encoding='utf-8')
print(f'{key}: {n} items, missing {len(missing)}', missing[:20])
