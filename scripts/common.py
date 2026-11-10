"""Shared helpers for the OrcaSlicer wiki translation pipeline."""
import re
import unicodedata

SKIP_DIRS = {'images', 'overrides', 'web_extras', '.github'}
SKIP_FILES = {'AGENTS.md', 'CLAUDE.md', 'README.md'}

FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})(.*)$')
HEAD = re.compile(r'^\s{0,3}(#{1,6})\s+(.*)$')
META = re.compile(r'^(\s*)\[(Mode|Modes|Variable|Variables|Type|Options|CLI Example)\]\(([^)]*)\):\s*(.*?)\s*$')
TOCLINE = re.compile(r'^(\s*)[-*+]\s+\[(.+)\]\(#([^)\s]+)\)\s*$')
LISTLINE = re.compile(r'^\s*(?:[-*+]|\d+\.)\s+')
PH = re.compile(r'\{\{([CMILUT])(\d+)\}\}')


def slug_v(v):
    """Slug as computed by the wiki's own link validator (GitHub-style, underscores dropped)."""
    v = unicodedata.normalize('NFKD', v)
    v = re.sub(r'[̀-ͯ]', '', v).strip().lower()
    v = re.sub(r'[^a-z0-9\s-]', '', v)
    v = re.sub(r'\s+', '-', v)
    v = re.sub(r'-+', '-', v)
    return v


def slug_gh(v):
    """GitHub's own heading slug: like slug_v but every space becomes a hyphen (runs are kept)."""
    v = unicodedata.normalize('NFKD', v)
    v = re.sub(r'[̀-ͯ]', '', v).strip().lower()
    v = re.sub(r'[^a-z0-9 _-]', '', v)
    return v.replace(' ', '-')


def slug_r(v):
    """Slug as Python-Markdown / mkdocs computes it (keeps underscores)."""
    v = unicodedata.normalize('NFKD', v)
    v = re.sub(r'[̀-ͯ]', '', v)
    v = re.sub(r'[^\w\s-]', '', v).strip().lower()
    return re.sub(r'[-\s]+', '-', v)


def plain(md):
    """Inline markdown -> plain text."""
    t = re.sub(r'!\[([^\]]*)\]\([^)]*\)', '', md)
    t = re.sub(r'\{\{I\d+\}\}', '', t)
    t = re.sub(r'<img[^>]*>', '', t)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'<[^>]+>', '', t)
    t = t.replace('`', '').replace('**', '').replace('__', '')
    t = re.sub(r'(?<![\w*])\*(\S[^*]*?)\*(?![\w*])', r'\1', t)
    t = t.replace('\\', '')
    return re.sub(r'\s+', ' ', t).strip()


def iter_fenced(lines):
    """Yield (start, end_inclusive, indent, info) for each fenced block."""
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            indent, fence, info = m.groups()
            close = re.compile(r'^\s*' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$')
            j = i + 1
            while j < len(lines) and not close.match(lines[j]):
                j += 1
            yield i, min(j, len(lines) - 1), indent, info.strip()
            i = j + 1
        else:
            i += 1


def headings_of(text):
    """Return heading list (level, raw text) skipping fenced code and mermaid blocks."""
    lines = text.split('\n')
    skip = set()
    for s, e, _, _ in iter_fenced(lines):
        skip.update(range(s, e + 1))
    out = []
    for n, line in enumerate(lines):
        if n in skip:
            continue
        m = HEAD.match(line)
        if m:
            t = re.sub(r'\s+#+\s*$', '', m.group(2)).strip()
            if t:
                out.append((len(m.group(1)), t))
    return out


def assign_slugs(heads):
    """heads: list of (level, raw english text) -> list of dicts with both slug flavours."""
    cv, cr, res = {}, {}, []
    for level, raw in heads:
        sv = slug_v(raw) or 'section'
        n = cv.get(sv, 0)
        cv[sv] = n + 1
        if n:
            sv = f'{sv}-{n}'
        sr = slug_r(plain(raw)) or 'section'
        n = cr.get(sr, 0)
        cr[sr] = n + 1
        if n:
            sr = f'{sr}_{n}'
        res.append({'level': level, 'en': plain(raw), 'raw': raw, 'id': sv, 'alt': sr})
    return res
