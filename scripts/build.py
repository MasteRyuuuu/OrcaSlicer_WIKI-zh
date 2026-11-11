#!/usr/bin/env python3
"""Build the Chinese OrcaSlicer wiki as one single-page site.

usage: build.py            -> docs/index.html + docs/img/...  (GitHub Pages publishes docs/ of the zh-cn branch)
Translated pages come from zh/<path>.md; anything not translated yet falls back to the
prepared English in work/en (release notes fall back to a short pointer page).
"""
import base64
import datetime
import hashlib
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.parse

import markdown
import yaml
from bs4 import BeautifulSoup, NavigableString

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import HEAD, PH, headings_of, plain, slug_gh, slug_v

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, WORK, ZH, OUT = ROOT / 'src' / 'wiki', ROOT / 'work', ROOT / 'zh', ROOT / 'docs'
TEMPLATE = ROOT / 'scripts' / 'template.html'
INLINE_MAX = 16_000

SEC_ZH = {
    'Guides': '指南', 'Calibration': '校准', 'General Settings': '通用设置', 'Design': '设计',
    'Print Prepare': '准备', 'User Profiles': '用户配置', 'Printer Settings': '打印机设置',
    'Basic Information': '基本信息', 'Machine G-Code': '机器 G-code', 'Multimaterial': '多材料',
    'Extruder': '挤出机', 'Motion Ability': '运动能力', 'Material Settings': '材料设置',
    'Filament': '耗材丝', 'Cooling': '冷却', 'Setting Overrides': '设置覆盖', 'Advanced': '高级',
    'Dependencies': '依赖关系', 'Print Settings': '工艺设置', 'Quality': '质量', 'Strength': '强度',
    'Speed': '速度', 'Support': '支撑', 'Others': '其他', 'Publishing 3MF': '发布 3MF',
    'Speed Dial': '快捷面板', 'Command Line Interface': '命令行', 'Plugins': '插件',
    'Releases': '版本发布', 'Developer Reference': '开发者参考', 'How to Build': '编译',
    'Plugin Development': '插件开发', 'API Reference': 'API 参考',
}
ALERT_ZH = {'note': '说明', 'tip': '提示', 'important': '重要', 'warning': '警告', 'caution': '当心'}
LABEL_ZH = {'Mode': '模式', 'Modes': '模式', 'Variable': '变量', 'Variables': '变量', 'Type': '类型',
            'Options': '可选值', 'CLI Example': '命令行'}
MODE_ZH = {'Simple': '简单', 'Advanced': '高级', 'Expert': '专家', 'Developer': '开发者'}
TYPE_ZH = [  # longest first
    ('Float or Percentage list', '浮点数或百分比列表'), ('Float or Percentage', '浮点数或百分比'),
    ('Point group list', '坐标点组列表'), ('Boolean list', '布尔值列表'), ('Integer list', '整数列表'),
    ('Float list', '浮点数列表'), ('Percentage list', '百分比列表'), ('Choice list', '选项列表'),
    ('Text list', '文本列表'), ('Point list', '坐标点列表'), ('Percentage', '百分比'), ('Boolean', '布尔值'),
    ('Integer', '整数'), ('Float', '浮点数'), ('Choice', '选项'), ('Text', '文本'), ('Point', '坐标点'),
]
META_SPECIAL = {
    '`Text` (shown as a dropdown of registered agents).': '`Text`（显示为已注册代理的下拉列表）',
    '`Float` — every variable above except `set_other_flow_ratios`, which is a [Boolean](option_type#boolean) '
    'enable toggle for all the others (`--set-other-flow-ratios=1`).':
        '`Float`：上面除 `set_other_flow_ratios` 之外的所有变量；`set_other_flow_ratios` 是控制其余各项的'
        '[布尔值](option_type#boolean)开关（`--set-other-flow-ratios=1`）',
}
GH_WIKI = 'https://github.com/OrcaSlicer/OrcaSlicer/wiki/'
MIME = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif',
        '.svg': 'image/svg+xml', '.webp': 'image/webp'}


# ---------------------------------------------------------------- navigation
class _Loader(yaml.SafeLoader):
    pass


_Loader.add_multi_constructor('tag:yaml.org,2002:python/', lambda l, s, n: None)
CFG = yaml.load((SRC / 'mkdocs.yml').read_text(encoding='utf-8'), Loader=_Loader)

PAGES = {}   # key -> info
ORDER = []


def walk(items, trail):
    out = []
    for item in items:
        (title, val), = item.items()
        if isinstance(val, list):
            out.append({'t': SEC_ZH.get(title, title), 'c': walk(val, trail + [SEC_ZH.get(title, title)])})
        else:
            rel = 'home.md' if val == 'index.md' else val
            key = pathlib.Path(rel).stem
            PAGES[key] = {'key': key, 'rel': rel, 'nav_en': title, 'trail': trail}
            ORDER.append(key)
            out.append({'p': hid(key)})
    return out


def hid(key, anchor=None):
    h = key.replace('_', '-')
    if anchor:
        a = re.sub(r'[^A-Za-z0-9-]', '-', anchor.strip().lower().replace('_', '-'))
        h += '--' + re.sub(r'-{3,}', '--', a).strip('-')
    return h


NAV = walk(CFG['nav'], [])


# ---------------------------------------------------------------- images
INLINE, FILES = {}, {}


def svg_clean(data):
    """Drop DOCTYPE/ENTITY machinery (expanding any internal entities) so SVGs publish cleanly."""
    t = data.decode('utf-8', 'replace')
    m = re.search(r'<!DOCTYPE[^\[>]*(\[(.*?)\])?\s*>', t, re.S)
    if m:
        ents = dict(re.findall(r'<!ENTITY\s+(\w+)\s+"([^"]*)"\s*>', m.group(2) or ''))
        t = t[:m.start()] + t[m.end():]
        for k, v in ents.items():
            t = t.replace(f'&{k};', v)
    t = re.sub(r'<!ENTITY[^>]*>', '', t)
    return t.encode('utf-8')


def img_bytes(path):
    data = path.read_bytes()
    return svg_clean(data) if path.suffix.lower() == '.svg' else data


def map_image(src):
    s = urllib.parse.unquote(src.split('?')[0])
    m = re.match(r'https?://(?:github\.com/OrcaSlicer/OrcaSlicer_WIKI/(?:blob|raw)/main|'
                 r'raw\.githubusercontent\.com/OrcaSlicer/OrcaSlicer_WIKI/main)/(images/.+)$', s)
    path = None
    if m:
        path, cls = SRC / m.group(1), 'shot'
        key = 'img/' + m.group(1)[len('images/'):]
    else:
        m = re.match(r'https?://(?:github\.com/OrcaSlicer/OrcaSlicer/(?:blob|raw)/main|'
                     r'raw\.githubusercontent\.com/OrcaSlicer/OrcaSlicer/main)/resources/images/(.+)$', s)
        if m:
            path, cls = WORK / 'res' / pathlib.Path(m.group(1)).name, 'icon'
            key = 'img/res/' + pathlib.Path(m.group(1)).name
    if not path or not path.exists():
        return None
    if path.stat().st_size <= INLINE_MAX:
        if key not in INLINE:
            INLINE[key] = f'data:{MIME.get(path.suffix.lower(), "application/octet-stream")};base64,' + \
                base64.b64encode(img_bytes(path)).decode()
    else:
        FILES[key] = path
    return key, cls


def img_html(orig):
    if orig.lstrip().startswith('<'):
        attrs = {k.lower(): v for k, v in re.findall(r'([\w-]+)\s*=\s*"([^"]*)"', orig)}
    else:
        m = re.match(r'!\[([^\]]*)\]\(\s*<?([^)\s>]*)>?', orig)
        attrs = {'alt': m.group(1), 'src': m.group(2)}
    src, alt = attrs.get('src', ''), attrs.get('alt', '')
    got = map_image(src)
    if got is None:
        if 'youtube.com' in src or 'youtu.be' in src:
            return '<span class="video-thumb">▶ 观看视频</span>'
        if 'shields.io' in src or 'ko-fi.com' in src:
            return f'<span class="badge">{html.escape(alt or "badge")}</span>'
        return f'<span class="ext-img">[图片：{html.escape(alt or src)}]</span>'
    key, cls = got
    size = ''.join(f' {k}="{html.escape(attrs[k])}"' for k in ('width', 'height') if k in attrs)
    return f'<img data-src="{key}" class="{cls}" alt="{html.escape(alt)}" loading="lazy"{size}>'


# ---------------------------------------------------------------- links
def map_link(t, page):
    if not t:
        return t
    if t.startswith('#'):
        return '#' + hid(page, t[1:])
    m = re.match(r'^https?://github\.com/(?:OrcaSlicer|SoftFever)/OrcaSlicer/wiki/([^#?/]+)/?(?:#(.*))?$', t)
    if m and m.group(1) in PAGES:
        return '#' + hid(m.group(1), m.group(2))
    m = re.match(r'^https?://(?:www\.)?orcaslicer\.com/wiki/(?:[^#?]*/)?([a-z0-9_]+)(?:\.html)?/?(?:#(.*))?$', t)
    if m and m.group(1) in PAGES:
        return '#' + hid(m.group(1), m.group(2))
    if re.match(r'^[a-z]+:', t):
        return t
    m = re.match(r'^(?:\.?/)?([A-Za-z0-9_\-]+)(?:\.md)?/?(?:#(.*))?$', t)
    if m and m.group(1) in PAGES:
        return '#' + hid(m.group(1), m.group(2))
    return GH_WIKI + t


# ---------------------------------------------------------------- option metadata chips
def md_inline(s, page):
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: f'[{m.group(1)}]({map_link(m.group(2), page)})', s)
    out = markdown.markdown(s)
    return re.sub(r'^<p>|</p>$', '', out.strip())


def render_meta(run, page):
    chips = []
    for d in run:
        label, target, value = d['label'], d['target'], d['value'].strip()
        value = META_SPECIAL.get(value, value)
        value = re.sub(r'\.\s*$', '', value)
        cls = 'chip'
        if label in ('Mode', 'Modes'):
            words = re.findall(r'`([^`]+)`', value) or [value]
            value = ' / '.join(MODE_ZH.get(w, w) for w in words)
            cls += ' mode-' + (words[0].lower() if words else 'x')
            vhtml = html.escape(value)
        elif label == 'Type':
            v = value
            for en, zh in TYPE_ZH:
                v = re.sub(r'(?<=\()' + re.escape(en) + r'(?=[):])', zh, v)
                v = re.sub(r'^`' + re.escape(en) + r'`$', zh, v)
            v = v.replace('(Choice:', '(选项：')
            v = re.sub(r'\(([^()`]*)\)', r'（\1）', v)
            vhtml = md_inline(v, page)
        elif label == 'Options':
            opts = [o.strip() for o in re.sub(r'^`|`$', '', value).split(',') if o.strip()]
            vhtml = ' '.join(f'<code>{html.escape(o)}</code>' for o in opts)
        else:
            vhtml = md_inline(value, page)
        href = map_link(target, page)
        chips.append(f'<span class="{cls}"><a class="chip-k" href="{href}">{LABEL_ZH.get(label, label)}</a>'
                     f'<span class="chip-v">{vhtml}</span></span>')
    return '<div class="opt-meta">' + ''.join(chips) + '</div>'


# ---------------------------------------------------------------- placeholder restore
FENCE_ANY = re.compile(r'^\s*(?:>\s*)*(`{3,}|~{3,})')


def restore(text, meta, page, translated):
    heads = meta['headings']
    own = headings_of(text)
    head_text = {}
    for h, (_, raw) in zip(heads, own):
        head_text[h['id']] = plain(PH.sub('', raw))
        head_text[h['alt']] = head_text[h['id']]

    def inline(line, raw):
        def rep(m):
            kind, n = m.group(1), int(m.group(2)) - 1
            if kind == 'I':
                return meta['img'][n] if raw else img_html(meta['img'][n])
            if kind == 'L':
                t = meta['link'][n]
                return t if raw else map_link(t, page)
            if kind == 'U':
                u = meta['url'][n]
                before = line[:m.start()]
                if raw or before.endswith('<'):
                    return u
                return f'<{u}>'
            return m.group(0)
        return PH.sub(rep, line)

    out, in_fence, hidx = [], False, 0
    for line in text.split('\n'):
        if FENCE_ANY.match(line):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(inline(line, True))
            continue
        m = re.match(r'^(\s*)\{\{([CMT])(\d+)\}\}\s*$', line)
        if m:
            ind, kind, n = m.group(1), m.group(2), int(m.group(3)) - 1
            if kind == 'C':
                out.extend(meta['code'][n])
            elif kind == 'M':
                out += ['', ind + render_meta(meta['meta'][n], page), '']
            else:
                for it in meta['toc'][n]:
                    label = head_text.get(it['anchor']) or plain(it['en'])
                    out.append(' ' * it['indent'] + f'- [{label}](#{hid(page, it["anchor"])})')
            continue
        if HEAD.match(line) and hidx < len(heads):
            line = re.sub(r'\s+#+\s*$', '', line.rstrip()) + f' {{#h-{hidx}}}'
            hidx += 1
        out.append(inline(line, False))
    return '\n'.join(out)


# ---------------------------------------------------------------- markdown -> html
MD_EXT = ['tables', 'attr_list', 'md_in_html', 'sane_lists', 'pymdownx.superfences', 'pymdownx.highlight',
          'pymdownx.arithmatex', 'pymdownx.inlinehilite', 'pymdownx.tilde']


ALERT_RE = re.compile(r'^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$')


CJK = r'⺀-⿿　-〿぀-ヿ㐀-䶿一-鿿豈-﫿＀-￯—…“”'
CJK_PUNCT = r'　-〿！-／：-＠［-｀｛-･—…“”'
CJK_NL_A = re.compile(rf'(?<=[{CJK}])[ \t]*\n[ \t]*(?=[{CJK}])')          # CJK \n CJK -> joined
CJK_NL_B = re.compile(rf'(?<=[{CJK_PUNCT}])[ \t]*\n[ \t]*|[ \t]*\n[ \t]*(?=[{CJK_PUNCT}])')  # around full-width punct
ADMON_RE = re.compile(r'^!!!\s+(\w+)(?:\s+"(.*)")?\s*$')
ADMON_KIND = {'info': 'note', 'note': 'note', 'abstract': 'note', 'question': 'note', 'example': 'note',
              'quote': 'note', 'tip': 'tip', 'hint': 'tip', 'success': 'tip', 'important': 'important',
              'warning': 'warning', 'caution': 'caution', 'danger': 'caution', 'failure': 'caution',
              'bug': 'caution'}


def convert_alerts(md):
    """Top-level GitHub alerts -> md_in_html divs (Python-Markdown would merge adjacent blockquotes).
    Also handles mkdocs `!!! kind "Title"` admonitions (body indented by 4 spaces)."""
    lines, out, i = md.split('\n'), [], 0
    while i < len(lines):
        a = ADMON_RE.match(lines[i])
        if a:
            kind, title, body = ADMON_KIND.get(a.group(1).lower(), 'note'), a.group(2), []
            i += 1
            while i < len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
                body.append(lines[i][4:])
                i += 1
            while body and not body[-1].strip():
                body.pop()
            head = [f'<p class="callout-title">{html.escape(title)}</p>', ''] if title else []
            out += ['', f'<div class="callout {kind}" markdown="1">', ''] + head + body + ['', '</div>', '']
            continue
        m = ALERT_RE.match(lines[i])
        if m:
            body = [m.group(2)] if m.group(2) else []
            i += 1
            while i < len(lines) and lines[i].startswith('>'):
                body.append(re.sub(r'^>\s?', '', lines[i]))
                i += 1
            out += ['', f'<div class="callout {m.group(1).lower()}" markdown="1">', ''] + body + ['', '</div>', '']
            continue
        out.append(lines[i])
        i += 1
    return '\n'.join(out)


def md_to_html(text):
    from pymdownx.superfences import fence_code_format
    text = convert_alerts(text)
    return markdown.markdown(text, extensions=MD_EXT, extension_configs={
        'pymdownx.superfences': {'custom_fences': [{'name': 'mermaid', 'class': 'mermaid',
                                                   'format': fence_code_format}]},
        'pymdownx.highlight': {'use_pygments': True, 'guess_lang': False, 'css_class': 'highlight'},
        'pymdownx.arithmatex': {'generic': True},
    })


MATH_JOBS, MERMAID_JOBS = [], []


def postprocess(htm, page, meta, translated):
    soup = BeautifulSoup(htm, 'html.parser')
    heads = meta['headings']
    toc = []
    for el in soup.find_all(re.compile(r'^h[1-6]$')):
        m = re.match(r'h-(\d+)$', el.get('id', ''))
        if not m:
            continue
        h = heads[int(m.group(1))]
        el['id'] = hid(page, h['id'])
        zh_txt = el.get_text(' ', strip=True)
        if hid(page, h['alt']) != el['id']:
            alias = soup.new_tag('span', attrs={'id': hid(page, h['alt']), 'class': 'alias'})
            el.insert(0, alias)
        gh = slug_gh(plain(h['en'])) if h['en'] else ''
        if gh and hid(page, gh) not in (el['id'], hid(page, h['alt'])) and not soup.find(id=hid(page, gh)):
            el.insert(0, soup.new_tag('span', attrs={'id': hid(page, gh), 'class': 'alias'}))
        if translated and h['en'] and re.sub(r'\W', '', zh_txt.lower()) != re.sub(r'\W', '', h['en'].lower()):
            en = soup.new_tag('span', attrs={'class': 'h-en', 'lang': 'en'})
            en.string = h['en']
            el.append(en)
        link = soup.new_tag('a', attrs={'class': 'h-link', 'href': '#' + el['id'], 'aria-label': '本节链接'})
        link.string = '#'
        el.append(link)
        toc.append([int(el.name[1]), el['id'], zh_txt, h['en']])
    # GitHub style alerts
    for bq in soup.find_all('blockquote'):
        first = bq.find('p', recursive=False)
        if not first:
            continue
        mm = re.match(r'\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]', first.get_text())
        if not mm:
            continue
        kind = mm.group(1).lower()
        for node in list(first.descendants):
            if isinstance(node, NavigableString) and '[!' in node:
                node.replace_with(re.sub(r'^\s*\[!\w+\]\s*', '', str(node), count=1))
                break
        while first.contents and (getattr(first.contents[0], 'name', None) == 'br' or
                                  (isinstance(first.contents[0], NavigableString) and not first.contents[0].strip())):
            first.contents[0].extract()
        if not first.get_text(strip=True) and not first.find(['img', 'code', 'a']):
            first.decompose()
        bq.name = 'div'
        bq['class'] = ['callout', kind]
        title = soup.new_tag('p', attrs={'class': 'callout-title'})
        title.string = ALERT_ZH[kind]
        bq.insert(0, title)
    for div in soup.find_all('div', class_='callout'):
        if div.find('p', class_='callout-title', recursive=False):
            continue
        kind = next((c for c in div['class'] if c in ALERT_ZH), 'note')
        title = soup.new_tag('p', attrs={'class': 'callout-title'})
        title.string = ALERT_ZH[kind]
        div.insert(0, title)
    # tables scroll inside their own box
    for t in soup.find_all('table'):
        t.wrap(soup.new_tag('div', attrs={'class': 'table-wrap'}))
    # external links open in a new tab
    for a in soup.find_all('a', href=True):
        if re.match(r'^https?:', a['href']):
            a['target'] = '_blank'
            a['rel'] = 'noopener'
    # math -> MathML (rendered later in one batch)
    for el in soup.find_all(class_='arithmatex'):
        tex = el.get_text()
        disp = el.name == 'div'
        tex = re.sub(r'^\s*\\[\[(]|\\[\])]\s*$', '', tex.strip())
        MATH_JOBS.append({'tex': tex, 'display': disp})
        el.clear()
        el.append(f'@@MATH{len(MATH_JOBS) - 1}@@')
        el['class'] = ['math', 'math-block' if disp else 'math-inline']
    # mermaid -> pre-rendered svg pair
    for el in soup.find_all(class_='mermaid'):
        src = el.get_text()
        MERMAID_JOBS.append(src)
        n = len(MERMAID_JOBS) - 1
        fig = soup.new_tag('figure', attrs={'class': 'diagram'})
        fig.append(f'@@MERMAID{n}@@')
        el.replace_with(fig)
    # code copy hook
    for d in soup.find_all('div', class_='highlight'):
        d['data-copy'] = '1'
    # soft line breaks inside Chinese prose would render as stray spaces
    if translated:
        for s in list(soup.find_all(string=True)):
            if '\n' not in s or s.find_parent(['pre', 'code', 'script', 'style']):
                continue
            t = CJK_NL_A.sub('', str(s))
            t = CJK_NL_B.sub('', t)
            if t != str(s):
                s.replace_with(NavigableString(t))
    text = soup.get_text(' ', strip=True)
    return str(soup), toc, re.sub(r'\s+', ' ', text)


def render_math():
    if not MATH_JOBS:
        return []
    js = ("const k=require('katex');let d='';process.stdin.on('data',c=>d+=c).on('end',()=>{"
          "const jobs=JSON.parse(d);console.log(JSON.stringify(jobs.map(j=>{try{return k.renderToString(j.tex,"
          "{displayMode:j.display,output:'mathml',throwOnError:false,strict:'ignore'})}catch(e){return j.tex}})))});")
    r = subprocess.run(['node', '-e', js], input=json.dumps(MATH_JOBS), capture_output=True, text=True,
                       cwd=ROOT / 'node', check=True)
    return json.loads(r.stdout)


def render_mermaid():
    outdir = OUT / 'img' / 'mermaid'
    outdir.mkdir(parents=True, exist_ok=True)
    cache = WORK / 'mermaid'
    cache.mkdir(exist_ok=True)
    cfg = cache / 'cfg.json'
    cfg.write_text(json.dumps({'fontFamily': '"PingFang SC","Noto Sans CJK SC","Microsoft YaHei",sans-serif'}))
    res = []
    for src in MERMAID_JOBS:
        h = hashlib.sha1(src.encode()).hexdigest()[:10]
        pair = {}
        for theme in ('default', 'dark'):
            f = cache / f'{h}-{theme}.svg'
            if not f.exists():
                inp = cache / f'{h}.mmd'
                inp.write_text(src, encoding='utf-8')
                subprocess.run(['mmdc', '-q', '-i', str(inp), '-o', str(f), '-t', theme, '-b', 'transparent',
                                '-c', str(cfg)], check=True, capture_output=True)
            name = f'img/mermaid/{h}-{theme}.svg'
            FILES[name] = f
            pair[theme] = name
        res.append(f'<img class="mm-light" src="{pair["default"]}" alt="流程图" loading="lazy">'
                   f'<img class="mm-dark" src="{pair["dark"]}" alt="流程图" loading="lazy">')
    return res


# ---------------------------------------------------------------- pages
SUMMARY_MARK = '<!-- summary -->'
SUMMARY_EN = re.compile(r'\s*\[\[en:(.+?)\]\]\s*$')


def summary_page(text, meta):
    """Free-structure page (release-note summaries): headings are taken from the Chinese text itself.
    A heading may end with [[en:English title]] to show the English original as its subtitle."""
    heads, out, used = [], [], set()
    in_fence = False
    for line in text.split('\n'):
        if FENCE_ANY.match(line):
            in_fence = not in_fence
        m = None if in_fence else HEAD.match(line)
        if m:
            en_m = SUMMARY_EN.search(line)
            en = re.sub(r'^[^A-Za-z0-9`*\[]+', '', en_m.group(1)).strip() if en_m else ''
            if en_m:
                line = line[:en_m.start()]
            base = slug_v(plain(en)) if en else ''
            base = base or f's{len(heads)}'
            sid, k = base, 1
            while sid in used:
                sid, k = f'{base}-{k}', k + 1
            used.add(sid)
            heads.append({'level': len(m.group(1)), 'en': en, 'id': sid, 'alt': sid})
        out.append(line)
    return '\n'.join(out), dict(meta, headings=heads, toc=[])


def release_stub(key, meta):
    title = meta['headings'][0]['en'] if meta['headings'] else key
    return (f'# {title}\n\n本版本的发布说明是一份很长的英文更新列表（PR 列表），中文站暂未翻译全文。'
            f'\n\n请查看英文原文：[{title}]({GH_WIKI}{key})\n')


def build():
    commit = subprocess.run(['git', '-C', str(SRC), 'log', '-1', '--format=%h|%cs'], capture_output=True,
                            text=True).stdout.strip().split('|')
    pages = []
    for key in ORDER:
        info = PAGES[key]
        rel = pathlib.Path(info['rel'])
        meta = json.loads((WORK / 'meta' / rel.with_suffix('.json')).read_text(encoding='utf-8'))
        zh_file = ZH / rel
        translated = zh_file.exists()
        stub = False
        if translated:
            text = zh_file.read_text(encoding='utf-8')
            if text.startswith(SUMMARY_MARK):
                text, meta = summary_page(text[len(SUMMARY_MARK):].lstrip('\n'), meta)
        elif key.startswith('release_'):
            text, stub = release_stub(key, meta), True
            meta = dict(meta, headings=[{'level': 1, 'en': meta['headings'][0]['en'], 'id': 'top', 'alt': 'top'}])
        else:
            text = (WORK / 'en' / rel).read_text(encoding='utf-8')
        md = restore(text, meta, key, translated)
        htm, toc, plain_text = postprocess(md_to_html(md), key, meta, translated)
        h1 = next((t for t in toc if t[0] == 1), None)
        title = h1[2] if h1 else (toc[0][2] if translated and toc else info['nav_en'])
        title_en = meta['headings'][0]['en'] if meta['headings'] else info['nav_en']
        if h1:
            toc.remove(h1)
        pages.append({'id': hid(key), 'key': key, 't': title, 'te': title_en, 'sec': info['trail'],
                      'zh': 1 if translated or stub else 0, 'src': info['rel'], 'h': htm, 'toc': toc,
                      'x': plain_text})
    math = render_math()
    mer = render_mermaid()
    for p in pages:
        p['h'] = re.sub(r'@@MATH(\d+)@@', lambda m: math[int(m.group(1))], p['h'])
        p['h'] = re.sub(r'@@MERMAID(\d+)@@', lambda m: mer[int(m.group(1))], p['h'])
    done = sum(1 for k in ORDER if (ZH / PAGES[k]['rel']).exists())
    data = {'pages': pages, 'nav': NAV, 'inline': INLINE, 'commit': commit[0], 'date': commit[1],
            'built': datetime.date.today().isoformat(), 'done': done, 'total': len(ORDER)}
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    page = TEMPLATE.read_text(encoding='utf-8').replace('/*__DATA__*/', blob)
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'img').mkdir(parents=True)
    (OUT / 'index.html').write_text(page, encoding='utf-8')
    (OUT / '.nojekyll').write_text('', encoding='utf-8')   # GitHub Pages: serve files as they are
    for name, path in FILES.items():
        dst = OUT / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(img_bytes(path))
    missing = sorted(set(p.stem for p in (WORK / 'en').rglob('*.md')) - set(PAGES))
    print(f'pages {len(pages)}  translated {done}  inline imgs {len(INLINE)}  files {len(FILES)}  '
          f'math {len(MATH_JOBS)}  mermaid {len(MERMAID_JOBS)}  html {len(page) / 1e6:.2f} MB')
    if missing:
        print('not in nav:', missing)


if __name__ == '__main__':
    build()
