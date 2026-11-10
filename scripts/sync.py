#!/usr/bin/env python3
"""Keep the Chinese wiki in step with the English upstream wiki repository (see upstream.json).

usage (paths are relative to the project root, the script can be run from anywhere):
  sync.py status   clone/fetch the upstream wiki into src/wiki and compare it with upstream.json
                   exit 0 = translation is current, exit 3 = upstream has new commits
  sync.py src      make sure src/wiki is checked out at the commit being built (needed by build.py)
  sync.py plan     move src/wiki to the newest upstream commit, re-prepare the English, carry every
                   unchanged Chinese block over (placeholders renumbered) and mark changed text with
                   TODO blocks; release-note pages get a list of untranslated keys. Writes work/sync/REPORT.md
  sync.py verify   list what still needs work; exit 0 only when every touched page is clean
  sync.py finish   (runs verify first) record the new upstream commit in upstream.json, clear work/sync/
"""
import difflib
import json
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import HEAD, PH  # noqa: E402
import rel_parse  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, PO_DIR = ROOT / 'src' / 'wiki', ROOT / 'src' / 'repo'
WORK, ZH, SYNC = ROOT / 'work', ROOT / 'zh', ROOT / 'work' / 'sync'
UPSTREAM, STATE = ROOT / 'upstream.json', ROOT / 'work' / 'sync' / 'state.json'
PY = [sys.executable, '-I']
SUMMARY_MARK = '<!-- summary -->'
TODO_OPEN = re.compile(r'^<<<TODO#(\d+)\s*$', re.M)
TODO_ANY = re.compile(r'<<<TODO#\d+|TODO#\d+>>>|^\[(?:EN-NEW|EN-OLD|ZH-OLD)\]\s*$', re.M)
STRAY = re.compile(r'\{\{\?[CMILUT]\d+\}\}')
META_KEY = {'C': 'code', 'M': 'meta', 'T': 'toc', 'I': 'img', 'L': 'link', 'U': 'url'}


# ---------------------------------------------------------------- small helpers
def sh(*cmd, cwd=None, check=True):
    r = subprocess.run([str(c) for c in cmd], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f'command failed: {" ".join(map(str, cmd))}\n{r.stderr.strip()}')
    return r.stdout.strip()


def read(p):
    return p.read_text(encoding='utf-8')


def load_json(p):
    return json.loads(read(p))


def describe(commit):
    return sh('git', '-C', SRC, 'log', '-1', '--format=%h %cs %s', commit)


def norm_url(u):
    u = u.strip().rstrip('/').lower()
    return u[:-4] if u.endswith('.git') else u


def ensure_src(up, fetch=True):
    """Clone (blobless) or fetch the upstream wiki; return the newest upstream commit."""
    if (SRC / '.git').exists():
        url = sh('git', '-C', SRC, 'remote', 'get-url', 'origin', check=False)
        if norm_url(url) != norm_url(up['repo']):
            shutil.rmtree(SRC)
    if not (SRC / '.git').exists():
        SRC.parent.mkdir(parents=True, exist_ok=True)
        sh('git', 'clone', '--quiet', '--filter=blob:none', '--no-checkout', up['repo'], SRC)
    if fetch:
        sh('git', '-C', SRC, 'fetch', '--quiet', 'origin', up['branch'])
        return sh('git', '-C', SRC, 'rev-parse', 'FETCH_HEAD')
    return None


def checkout(commit):
    # always run it: a --no-checkout clone already has HEAD at the commit but an empty work tree
    sh('git', '-C', SRC, 'checkout', '--quiet', '--force', '--detach', commit)


def ensure_po(up):
    """Shallow sparse checkout of the OrcaSlicer repo, only for the zh_CN UI translation (term hints)."""
    po = PO_DIR / up['po_path']
    try:
        if not (PO_DIR / '.git').exists():
            sh('git', 'clone', '--quiet', '--depth', '1', '--filter=blob:none', '--sparse', up['po_repo'], PO_DIR)
            sh('git', '-C', PO_DIR, 'sparse-checkout', 'set', str(pathlib.PurePosixPath(up['po_path']).parent))
        else:
            sh('git', '-C', PO_DIR, 'fetch', '--quiet', '--depth', '1', 'origin')
            sh('git', '-C', PO_DIR, 'reset', '--quiet', '--hard', 'FETCH_HEAD')
    except SystemExit as e:
        print(f'warning: could not update {up["po_repo"]}: {e}')
    return po if po.exists() else None


# ---------------------------------------------------------------- block alignment
def blocks(text):
    text = text.strip('\n')
    return re.split(r'\n[ \t]*\n', text) if text else []


def ph_list(s):
    return [(m.group(1), int(m.group(2))) for m in PH.finditer(s)]


def ph_value(t, k, meta):
    arr = meta.get(META_KEY[t], [])
    if 1 <= k <= len(arr):
        v = arr[k - 1]
        return v if isinstance(v, str) else json.dumps(v, ensure_ascii=False, sort_keys=True)
    return f'?{t}{k}'


def resolve(s, meta):
    """Text with every placeholder replaced by what it stands for (for comparing old and new English)."""
    return PH.sub(lambda m: '\x00%s:%s\x00' % (m.group(1), ph_value(m.group(1), int(m.group(2)), meta)), s)


def no_prose(s):
    """True when a block has nothing to translate (placeholders, rules, table separators, html only)."""
    t = PH.sub(' ', s)
    t = re.sub(r'<[^>]+>', ' ', t)
    return not re.search(r'[A-Za-z]{2,}', t)


def kind(b):
    first = b.split('\n', 1)[0]
    m = HEAD.match(first)
    if m:
        return 'h%d' % len(m.group(1))
    s = first.lstrip()
    if s.startswith('|'):
        return 't'
    if s.startswith('>'):
        return 'q'
    if re.match(r'(?:[-*+]|\d+\.)\s', s):
        return 'l'
    return 'p'


def align_zh(ob, zb):
    """For every old English block, the Chinese text that translates it (None when unknown).
    Extra Chinese blocks (translator notes) stay attached to the block before them."""
    sig = lambda b: (kind(b), tuple(ph_list(b)))  # noqa: E731
    zo = [None] * len(zb)
    sm = difflib.SequenceMatcher(None, [sig(b) for b in ob], [sig(b) for b in zb], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for k in range(i2 - i1):
                zo[j1 + k] = i1 + k
    groups, pending, last = {}, [], None
    for j, b in enumerate(zb):
        i = zo[j]
        if i is None:
            (groups[last] if last is not None else pending).append(b)
        else:
            groups.setdefault(i, []).extend(pending + [b])
            pending, last = [], i
    return ['\n\n'.join(groups[i]) if i in groups else None for i in range(len(ob))]


def renumber(z, o, n):
    """Rewrite the placeholders of Chinese text z (made for English o) to the numbering of English n.
    o and n are equal once placeholders are resolved. Returns None when z does not fit o."""
    po, pn = ph_list(o), ph_list(n)
    mp = {}
    for t in META_KEY:
        a = [k for tt, k in po if tt == t]
        b = [k for tt, k in pn if tt == t]
        if len(a) != len(b):
            return None
        mp.update({(t, x): y for x, y in zip(a, b)})
    bad = []

    def rep(m):
        key = (m.group(1), int(m.group(2)))
        if key not in mp:
            bad.append(key)
            return m.group(0)
        return '{{%s%d}}' % (m.group(1), mp[key])
    out = PH.sub(rep, z)
    return None if bad else out


def content_map(olds, old_meta, news, new_meta):
    """Map old placeholder ids to new ids that stand for the same thing; unknown ones become {{?X1}}."""
    pool = {}
    for b in news:
        for t, k in ph_list(b):
            ids = pool.setdefault((t, ph_value(t, k, new_meta)), [])
            if k not in ids:
                ids.append(k)
    mp = {}
    for b in olds:
        for t, k in ph_list(b):
            if (t, k) not in mp:
                cands = pool.get((t, ph_value(t, k, old_meta)), [])
                mp[(t, k)] = '{{%s%d}}' % (t, cands.pop(0)) if cands else '{{?%s%d}}' % (t, k)
    return lambda s: PH.sub(lambda m: mp.get((m.group(1), int(m.group(2))),
                                             '{{?%s%s}}' % (m.group(1), m.group(2))), s)


class Drafter:
    def __init__(self):
        self.n = 0

    def todo(self, news, olds, zs, old_meta, new_meta, sep):
        self.n += 1
        parts = [f'<<<TODO#{self.n}', '[EN-NEW]', sep.join(news)]
        if olds:
            remap = content_map(olds, old_meta, news, new_meta)
            parts += ['[EN-OLD]', remap(sep.join(olds))]
            zt = sep.join(z for z in zs if z)
            if zt:
                parts += ['[ZH-OLD]', remap(zt)]
        parts.append(f'TODO#{self.n}>>>')
        return '\n'.join(parts)

    def units(self, ou, nu, zu, old_meta, new_meta, sep, fine):
        """Draft a sequence of units (blocks, or lines of one table/list block)."""
        out = []
        ores = [resolve(x, old_meta) for x in ou]
        nres = [resolve(x, new_meta) for x in nu]
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ores, nres, autojunk=False).get_opcodes():
            if tag == 'delete':
                continue
            if tag == 'equal':
                for k in range(i2 - i1):
                    o, n, z = ou[i1 + k], nu[j1 + k], zu[i1 + k]
                    c = renumber(z, o, n) if z is not None else None
                    if c is None and no_prose(n):
                        c = n
                    out.append(c if c is not None else
                               self.todo([n], [o] if z else [], [z] if z else [], old_meta, new_meta, sep))
                continue
            olds, news, zs = ou[i1:i2], nu[j1:j2], zu[i1:i2]
            if all(no_prose(n) for n in news):
                out.extend(news)
            elif (fine and tag == 'replace' and len(olds) == 1 and len(news) == 1 and zs[0] is not None
                  and kind(olds[0]) in 'tl' and kind(news[0]) == kind(olds[0])
                  and olds[0].count('\n') == zs[0].count('\n') > 0):
                # one table or list changed: carry unchanged rows/items over line by line
                out.append(self.units(olds[0].split('\n'), news[0].split('\n'), zs[0].split('\n'),
                                      old_meta, new_meta, '\n', False))
            else:
                out.append(self.todo(news, olds, zs, old_meta, new_meta, sep))
        return sep.join(out)

    def page(self, old_en, old_meta, new_en, new_meta, zh):
        ob, nb = blocks(old_en), blocks(new_en)
        zb = align_zh(ob, blocks(zh))
        return self.units(ob, nb, zb, old_meta, new_meta, '\n\n', True).rstrip() + '\n'


# ---------------------------------------------------------------- release-note summaries
def read_tsv(p):
    tr = {}
    if p.exists():
        for line in read(p).split('\n'):
            if line.strip() and '\t' in line:
                k, v = line.split('\t', 1)
                tr[k.strip()] = v.strip()
    return tr


def rel_remap(old_secs, new_secs, tr, old_meta, new_meta):
    """Carry translated keys (S<i>, P<i>.<j>, item numbers) over by matching the English text
    (placeholders compared by what they stand for, then renumbered)."""
    old = {}
    n = 0
    for si, s in enumerate(old_secs):
        old.setdefault(('S', s['level'], resolve(s['title'], old_meta)), (f'S{si}', s['title']))
        for pj, p in enumerate(s['prose']):
            old.setdefault(('P', resolve(p, old_meta)), (f'P{si}.{pj}', p))
        for it in s['items']:
            n += 1
            old.setdefault(('I', resolve(it['title'], old_meta)), (str(n), it['title']))
    new_tr, todo, n = {}, [], 0

    def take(key, look, en):
        old_key, old_en = old.get(look, (None, None))
        v = renumber(tr[old_key], old_en, en) if old_key in tr else None
        if v is None:
            todo.append((key, en))
        else:
            new_tr[key] = v
    for si, s in enumerate(new_secs):
        take(f'S{si}', ('S', s['level'], resolve(s['title'], new_meta)), s['title'])
        if 'Support OrcaSlicer' not in s['title']:
            for pj, p in enumerate(s['prose']):
                if not p.startswith('<'):
                    take(f'P{si}.{pj}', ('P', resolve(p, new_meta)), p)
        for it in s['items']:
            n += 1
            take(str(n), ('I', resolve(it['title'], new_meta)), it['title'])
    return new_tr, todo


def sync_release(key, old_meta, new_meta):
    rel_dir = WORK / 'rel'
    rel_dir.mkdir(exist_ok=True)
    jp, tp, dp = rel_dir / f'{key}.json', rel_dir / f'{key}.zh.tsv', rel_dir / f'{key}.todo.tsv'
    old_secs = load_json(jp) if jp.exists() else []
    new_secs = rel_parse.parse(read(WORK / 'en' / 'releases' / f'{key}.md'))
    new_tr, todo = rel_remap(old_secs, new_secs, read_tsv(tp), old_meta or {}, new_meta)
    jp.write_text(json.dumps(new_secs, ensure_ascii=False, indent=1), encoding='utf-8')
    tp.write_text(''.join(f'{k}\t{v}\n' for k, v in new_tr.items()), encoding='utf-8')
    if todo:
        dp.write_text(''.join(f'{k}\t{v}\n' for k, v in todo), encoding='utf-8')
    elif dp.exists():
        dp.unlink()
    if not todo:
        sh(*PY, ROOT / 'scripts' / 'rel_build.py', key)
    return len(todo)


# ---------------------------------------------------------------- commands
def status():
    up = load_json(UPSTREAM)
    new = ensure_src(up)
    old = up['commit']
    print(f'upstream    {up["repo"]} ({up["branch"]})')
    print(f'translated  {describe(old)}')
    if new == old:
        print('UP-TO-DATE')
        return 0
    print(f'latest      {describe(new)}')
    log = sh('git', '-C', SRC, 'log', '--format=%h %cs %s', f'{old}..{new}').splitlines()
    print(f'{len(log)} new commit(s):\n' + '\n'.join('  ' + x for x in log))
    diff = sh('git', '-C', SRC, 'diff', '--name-status', '--no-renames', old, new)
    print('changed files:\n' + '\n'.join('  ' + x for x in diff.splitlines()))
    return 3


def src():
    up = load_json(UPSTREAM)
    target = load_json(STATE)['to'] if STATE.exists() else up['commit']
    ensure_src(up, fetch=False)
    if sh('git', '-C', SRC, 'cat-file', '-t', target, check=False) != 'commit':
        sh('git', '-C', SRC, 'fetch', '--quiet', 'origin', up['branch'])
    checkout(target)
    print(f'src/wiki at {describe(target)}')
    return 0


def sec_zh_missing():
    import yaml
    text = read(ROOT / 'scripts' / 'build.py')
    block = text[text.index('SEC_ZH = {'):]
    block = block[:block.index('\n}')]
    known = set(re.findall(r"'([^']+)':", block))
    loader = type('L', (yaml.SafeLoader,), {})
    loader.add_multi_constructor('tag:yaml.org,2002:python/', lambda ld, s, n: None)
    cfg = yaml.load(read(SRC / 'mkdocs.yml'), Loader=loader)

    def walk(items):
        for item in items or []:
            if isinstance(item, dict):
                for title, val in item.items():
                    if isinstance(val, list):
                        yield title
                        yield from walk(val)
    return sorted({t for t in walk(cfg.get('nav')) if t not in known})


def plan(force=False):
    up = load_json(UPSTREAM)
    if STATE.exists() and not force:
        sys.exit('an update is already in progress (work/sync/state.json): finish it, or rerun plan with --force')
    dirty = sh('git', '-C', ROOT, 'status', '--porcelain', '--', 'zh', 'work/en', 'work/meta', 'work/rel',
               check=False)
    if dirty and not force:
        sys.exit('zh/ or work/ has uncommitted changes; commit them first (or rerun with --force)\n' + dirty)
    new = ensure_src(up)
    old = up['commit']
    if new == old:
        print('UP-TO-DATE')
        return 0
    commits = sh('git', '-C', SRC, 'log', '--format=%h %cs %s', f'{old}..{new}').splitlines()
    checkout(new)

    tmp = SYNC / 'new'
    if tmp.exists():
        shutil.rmtree(tmp)
    sh(*PY, ROOT / 'scripts' / 'prep.py', SRC, tmp)
    en_old, en_new = WORK / 'en', tmp / 'en'
    old_pages = {str(p.relative_to(en_old)) for p in en_old.rglob('*.md')}
    new_pages = {str(p.relative_to(en_new)) for p in en_new.rglob('*.md')}
    o_txt = {r: read(en_old / r) for r in old_pages}
    n_txt = {r: read(en_new / r) for r in new_pages}
    o_meta = {r: load_json((WORK / 'meta' / r).with_suffix('.json')) for r in old_pages}
    n_meta = {r: load_json((tmp / 'meta' / r).with_suffix('.json')) for r in new_pages}

    # pages that moved: an added page whose English is close to a removed one
    removed, added = sorted(old_pages - new_pages), sorted(new_pages - old_pages)
    renamed = {}
    for a in added:
        best = max(((difflib.SequenceMatcher(None, o_txt[r], n_txt[a], autojunk=False).ratio(), r)
                    for r in removed if r not in renamed.values()), default=(0, None))
        if best[0] >= 0.6:
            renamed[a] = best[1]
    removed = [r for r in removed if r not in renamed.values()]

    res = {'todo': {}, 'new': [], 'release': {}, 'meta_only': [], 'removed': removed, 'renamed': renamed}
    drafts = {}
    for rel in sorted(new_pages):
        prev = rel if rel in old_pages else renamed.get(rel)
        zh_prev = ZH / prev if prev else None
        key = pathlib.PurePosixPath(rel).stem
        is_release = rel.startswith('releases/') and key.startswith('release_')
        if prev and o_txt[prev] == n_txt[rel]:
            if o_meta[prev] != n_meta[rel] or prev != rel:
                res['meta_only'].append(rel)
            if prev != rel and zh_prev.exists():
                drafts[rel] = read(zh_prev)
            continue
        zh_text = read(zh_prev) if zh_prev and zh_prev.exists() else None
        if is_release and (zh_text is None or zh_text.startswith(SUMMARY_MARK)):
            res['release'][rel] = key
            continue
        if zh_text is None:
            res['new'].append(rel)
            continue
        d = Drafter()
        drafts[rel] = d.page(o_txt[prev], o_meta[prev], n_txt[rel], n_meta[rel], zh_text)
        res['todo'][rel] = d.n

    # switch work/en + work/meta to the new English; write drafts; drop removed / moved pages
    for sub in ('en', 'meta'):
        shutil.rmtree(WORK / sub)
        shutil.move(str(tmp / sub), str(WORK / sub))
    shutil.rmtree(tmp)
    stem = lambda r: pathlib.PurePosixPath(r).stem  # noqa: E731
    for a, r in renamed.items():   # release-note data follows a moved page
        for ext in ('json', 'zh.tsv'):
            f = WORK / 'rel' / f'{stem(r)}.{ext}'
            if f.exists():
                shutil.move(str(f), str(WORK / 'rel' / f'{stem(a)}.{ext}'))
    for r in removed + list(renamed.values()):
        if (ZH / r).exists():
            (ZH / r).unlink()
    for r in removed:
        for f in (WORK / 'rel').glob(f'{stem(r)}.*'):
            f.unlink()
    for rel, text in drafts.items():
        (ZH / rel).parent.mkdir(parents=True, exist_ok=True)
        (ZH / rel).write_text(text, encoding='utf-8')
    for rel, key in list(res['release'].items()):
        prev = rel if rel in old_pages else renamed.get(rel)
        res['release'][rel] = {'key': key, 'todo': sync_release(key, o_meta.get(prev), n_meta[rel])}

    po = ensure_po(up)
    if po:
        sh(*PY, ROOT / 'scripts' / 'hints.py', SRC, po, WORK)
    missing_sec = sec_zh_missing()

    state = {'from': old, 'to': new, 'commits': commits, **res, 'sections': missing_sec}
    SYNC.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding='utf-8')
    report = render_report(state, up)
    (SYNC / 'REPORT.md').write_text(report, encoding='utf-8')
    print(report)
    return 0


def render_report(st, up):
    L = [f'# 同步报告：{st["from"][:7]} → {st["to"][:7]}', '', f'上游：{up["repo"]}', '',
         f'## 上游新提交（{len(st["commits"])}）', ''] + [f'- {c}' for c in st['commits']] + ['']
    todo_total = sum(st['todo'].values())
    L += ['## 需要翻译', '']
    if st['todo']:
        L += [f'### 已生成草稿、含 TODO 块的页面（共 {todo_total} 处）', '']
        L += [f'- `zh/{r}`：{n} 处（术语提示 `work/hints/{r[:-3]}.txt`）' if n else
              f'- `zh/{r}`：0 处（只是占位符编号或无需翻译的内容变了，已自动处理）'
              for r, n in st['todo'].items()] + ['']
    if st['new']:
        L += ['### 新页面（整页翻译，写到 zh/ 下同路径）', ''] + [f'- `{r}`' for r in st['new']] + ['']
    if st['release']:
        L += ['### 版本发布页（摘要模式）', '']
        L += [f'- `{v["key"]}`：{v["todo"]} 条待译（`work/rel/{v["key"]}.todo.tsv`）' if v['todo'] else
              f'- `{v["key"]}`：已自动更新，无新条目' for v in st['release'].values()] + ['']
    if st['sections']:
        L += ['### 导航里没有中文名的分组（在 scripts/build.py 的 SEC_ZH 里补上）', '']
        L += [f'- {s}' for s in st['sections']] + ['']
    if not (todo_total or st['new'] or any(v['todo'] for v in st['release'].values()) or st['sections']):
        L += ['无。', '']
    L += ['## 已自动处理', '']
    if st['meta_only']:
        L += ['- 只有链接/代码/元数据变化，中文无需改动：' + '、'.join(f'`{r}`' for r in st['meta_only'])]
    if st['renamed']:
        L += ['- 改名/移动：' + '、'.join(f'`{a}` ← `{b}`' for a, b in st['renamed'].items())]
    if st['removed']:
        L += ['- 上游已删除（中文页一并删除）：' + '、'.join(f'`{r}`' for r in st['removed'])]
    if not (st['meta_only'] or st['renamed'] or st['removed']):
        L += ['- 无']
    return '\n'.join(L) + '\n'


def touched(st):
    return sorted(set(st['todo']) | set(st['new']) | set(st['renamed']))


def verify(quiet=False):
    if not STATE.exists():
        print('no update in progress')
        return 0
    import check
    st = load_json(STATE)
    errors, warnings = [], []
    for rel in touched(st):
        p = ZH / rel
        if not p.exists():
            errors.append(f'{rel}: 还没有中文页')
            continue
        t = read(p)
        n = len(TODO_OPEN.findall(t))
        if n or TODO_ANY.search(t):
            errors.append(f'{rel}: 还有 {n} 个 TODO 块（或残留的 [EN-NEW]/[EN-OLD]/[ZH-OLD] 标记）')
        if STRAY.search(t):
            errors.append(f'{rel}: 残留 {{{{?…}}}} 占位符：' + ' '.join(sorted(set(STRAY.findall(t)))[:8]))
        probs, _ = check.check(rel)
        for pr in probs:
            (warnings if 'english-looking' in pr else errors).append(f'{rel}: {pr}')
    for rel, v in st['release'].items():
        key = v['key']
        if (WORK / 'rel' / f'{key}.todo.tsv').exists():
            errors.append(f'{key}: work/rel/{key}.todo.tsv 还在（译完并入 {key}.zh.tsv 后删除它）')
            continue
        out = sh(*PY, ROOT / 'scripts' / 'rel_build.py', key)
        if 'missing 0' not in out:
            errors.append(f'{key}: {out}')
        else:
            probs, _ = check.check(rel)
            errors += [f'{rel}: {pr}' for pr in probs if 'english-looking' not in pr]
    for s in sec_zh_missing() if (SRC / 'mkdocs.yml').exists() else []:
        errors.append(f'导航分组 "{s}" 在 scripts/build.py 的 SEC_ZH 里没有中文名')
    if not quiet or errors:
        for w in warnings:
            print('warning:', w)
        for e in errors:
            print('TODO:', e)
        print('OK — ready to build' if not errors else f'{len(errors)} problem(s) left')
    return 1 if errors else 0


def finish():
    if not STATE.exists():
        print('no update in progress')
        return 0
    if verify(quiet=True):
        return 1
    st = load_json(STATE)
    up = load_json(UPSTREAM)
    h, date, subject = sh('git', '-C', SRC, 'log', '-1', '--format=%H%x09%cs%x09%s', st['to']).split('\t', 2)
    up.update({'commit': h, 'date': date, 'subject': subject})
    UPSTREAM.write_text(json.dumps(up, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    shutil.rmtree(SYNC)
    print(f'upstream.json now at {h[:7]} {date} {subject}')
    return 0


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    force = '--force' in sys.argv
    fn = {'status': status, 'src': src, 'plan': lambda: plan(force), 'verify': verify, 'finish': finish}.get(cmd)
    if not fn:
        sys.exit(__doc__)
    sys.exit(fn())
