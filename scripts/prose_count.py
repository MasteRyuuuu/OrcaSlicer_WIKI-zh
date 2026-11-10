import re, sys, pathlib, collections
root = pathlib.Path(sys.argv[1])
tot = collections.Counter(); pages = collections.Counter()
for f in sorted(root.rglob('*.md')):
    rel = f.relative_to(root)
    if rel.parts[0] in ('images','overrides','web_extras') or rel.name in ('AGENTS.md','CLAUDE.md','README.md'): continue
    t = f.read_text(encoding='utf-8')
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)          # code blocks
    t = re.sub(r'<[^>]+>', ' ', t)                        # html tags
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', t)           # images
    t = re.sub(r'\]\([^)]*\)', ']', t)                    # link targets
    t = re.sub(r'https?://\S+', ' ', t)
    t = re.sub(r'`[^`]*`', ' x ', t)
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", t)
    sec = rel.parts[0] if len(rel.parts) > 1 else '(top)'
    tot[sec] += len(words); pages[sec] += 1
for k, v in sorted(tot.items(), key=lambda x: -x[1]):
    print(f"{k:22s} {pages[k]:3d} pages {v:7d} prose words")
print('TOTAL', sum(tot.values()))
