#!/usr/bin/env python3
"""Two-step helper for the very formulaic patterns page.

draft: patterns_draft.py draft <en.md> <out.md> <prose.txt>
    converts rating lines / headings by dictionary, replaces every remaining prose line with @@Pn@@
    (keeping indentation, list markers, quote markers and trailing double spaces) and lists the
    English prose lines in prose.txt.
merge: patterns_draft.py merge <out.md> <zh_prose.txt> <final.md>
    zh_prose.txt has lines "Pn: 中文"; fills them in.
"""
import re
import sys

RATING = {'Ultra-Low': '极低', 'Extra-Low': '很低', 'Normal-Low': '中低', 'Normal-High': '中高', 'Extra-High': '很高',
          'Ultra-High': '极高', 'Low': '低', 'Normal': '中等', 'High': '高'}
VAR = {'None': '无', 'Unnoticeable': '不明显', 'Possibly Noticeable': '可能明显', 'Likely Noticeable': '很可能明显'}
HEAD = {
    'Patterns': '图案', 'Analysis parameters': '分析参数', 'Strength': '强度', 'Material Usage': '材料用量',
    'Print Time': '打印时间', 'Layer Time Variability': '层时间波动', 'Slicing Time': '切片时间',
    'G-code Size': 'G-code 大小', 'Multiline': '多线', 'Monotonic': '单调', 'Monotonic line': '单调线',
    'Rectilinear': '直线', 'Aligned Rectilinear': '直线排列', 'Zig Zag': '之字形', 'Cross Zag': '交叉之字',
    'Locked Zag': '限定之字', 'Line': '线', 'Grid': '网格', 'Triangles': '三角形', 'Tri-hexagon': '内六边形',
    'Cubic': '立方体', 'Adaptive Cubic': '自适应立方体', 'Quarter Cubic': '四分之一立方体',
    'Support Cubic': '支撑立方体', 'Lightning': '闪电', 'Honeycomb': '蜂窝', '3D Honeycomb': '3D 蜂窝',
    'Lateral Honeycomb': '侧向蜂窝', 'Lateral Lattice': '侧向晶格', 'Cross Hatch': '交叉层叠',
    'TPMS-D': 'TPMS-D', 'TPMS-FK': 'TPMS-FK', 'Adaptive TPMS': '自适应 TPMS', 'Gyroid': '螺旋体',
    'Concentric': '同心', 'Spiral Inset': '螺旋内缩', 'Hilbert Curve': '希尔伯特曲线',
    'Archimedean Chords': '阿基米德和弦', 'Octagram Spiral': '八角螺旋', 'Overhang Angle': '悬垂角度',
    'Prune Angle': '修剪角度', 'Straightening Angle': '拉直角度', 'Fill pattern tops': '填充图案顶部',
    'Adaptive Density': '自适应密度', 'Interior Density': '内部密度', 'Adaptive Gradient': '自适应梯度',
    'Gyroid Optimized': '螺旋体优化',
}
LINKWORD = {'Multiline': '多线', 'Symmetric infill Y axis': '对称填充 Y 轴', 'Smooth Factor': '平滑系数',
            'Adaptive Density': '自适应密度', 'Sparse Infill': '稀疏填充', 'Solid Infill': '实心填充',
            'Surface': '表面', 'Ironing': '熨烫', 'Support Base': '支撑主体', 'Support Interface': '支撑面',
            'Classic': '经典', 'Non-Crossing': '不交叉', 'Cubic': '立方体', 'Concentric': '同心',
            'Zig Zag': '之字形'}
VAL = {'N/A': '不适用', 'No': '否', 'Yes': '是'}


def rating(s):
    s = s.strip()
    return RATING.get(s, s)


def link(m):
    return f'[{LINKWORD.get(m.group(1), m.group(1))}]({m.group(2)})'


def conv(line):
    """Return converted line, or None if it is prose to translate by hand."""
    ind = re.match(r'^(\s*)', line).group(1)
    s = line.strip()
    if not s or re.fullmatch(r'(\{\{I\d+\}\}\s*)+', s) or s.startswith('{{M') or s.startswith('{{T') or s.startswith('{{C'):
        return line
    m = re.match(r'^(#+)\s+(.*)$', s)
    if m:
        return f'{m.group(1)} {HEAD.get(m.group(2), m.group(2))}' if m.group(2) in HEAD else None
    if s == '- **Strength**':
        return ind + '- **强度**'
    if s == '- **Extra:**':
        return ind + '- **其他：**'
    if s == '- **Applies to:**':
        return ind + '- **适用于：**'
    m = re.match(r'^- \*\*(Horizontal \(X-Y\)|Vertical \(Z\)|Material Usage|Print Time|Material/Time \(Higher better\)|Slicing Time|G-code Size):\*\* (\S+)( .*)?$', s)
    if m:
        lab = {'Horizontal (X-Y)': '水平（X-Y）', 'Vertical (Z)': '竖直（Z）', 'Material Usage': '材料用量',
               'Print Time': '打印时间', 'Material/Time (Higher better)': '材料/时间（越高越好）',
               'Slicing Time': '切片时间', 'G-code Size': 'G-code 大小'}[m.group(1)]
        return f'{ind}- **{lab}：** {rating(m.group(2))}{m.group(3) or ""}'
    m = re.match(r'^- \*\*Layer time Variability:\*\* (.*)$', s)
    if m and m.group(1) in VAR:
        return f'{ind}- **层时间波动：** {VAR[m.group(1)]}'
    m = re.match(r'^- \*\*Density Calculation:\*\*\s+% of\s+total infill volume$', s)
    if m:
        return f'{ind}- **密度计算：** 填充总体积的 %'
    if s == '- **Density Calculation:** % of layer before top shell layers':
        return f'{ind}- **密度计算：** 顶部外壳层之前那一层的 %'
    if s == '- **Density Calculation:** Unknown':
        return f'{ind}- **密度计算：** 未知'
    m = re.match(r'^- \*\*([23]) lines:\*\* Print Time (\S+) (\{\{I\d+\}\}) \((\d+)% (Faster|Slower) over single line\)$', s)
    if m:
        fs = '快' if m.group(5) == 'Faster' else '慢'
        return f'{ind}- **{m.group(1)} 线：** 打印时间 {rating(m.group(2))} {m.group(3)}（比单线{fs} {m.group(4)}%）'
    m = re.match(r'^- \*\*\[([^\]]+)\]\((\{\{L\d+\}\})\):\*\* (.*)$', s)
    if m and m.group(1) in LINKWORD:
        v = m.group(3)
        v = VAL.get(v, v)
        v = re.sub(r'\[([^\]]+)\]\((\{\{L\d+\}\})\)', link, v)
        v = v.replace(') only', ')').replace('] only', ']')
        if 'only' in m.group(3):
            v = '仅' + v
        return f'{ind}- **[{LINKWORD[m.group(1)]}]({m.group(2)})：** {v}'
    m = re.match(r'^- \*\*\[([^\]]+)\]\((\{\{L\d+\}\})\)\*\*$', s)
    if m and m.group(1) in LINKWORD:
        return f'{ind}- **[{LINKWORD[m.group(1)]}]({m.group(2)})**'
    return None


def draft(en, out, prose):
    res, plist = [], []
    for line in open(en, encoding='utf-8').read().split('\n'):
        c = conv(line)
        if c is not None:
            res.append(c)
            continue
        m = re.match(r'^(\s*(?:>\s?)?(?:[-*+]\s+|\d+\.\s+)?)(.*?)(\s*)$', line)
        pre, body, post = m.group(1), m.group(2), m.group(3)
        if line.lstrip().startswith('|'):
            pre, body, post = '', line, ''
        if not re.search(r'[A-Za-z]{2,}', body):
            res.append(line)
            continue
        plist.append(body)
        res.append(f'{pre}@@P{len(plist)}@@{post}')
    open(out, 'w', encoding='utf-8').write('\n'.join(res))
    open(prose, 'w', encoding='utf-8').write('\n'.join(f'P{i + 1}: {p}' for i, p in enumerate(plist)) + '\n')
    print(len(plist), 'prose lines')


def merge(out, zh, final):
    tr = {}
    for line in open(zh, encoding='utf-8').read().split('\n'):
        m = re.match(r'^P(\d+):\s?(.*)$', line)
        if m:
            tr[int(m.group(1))] = m.group(2)
    text = open(out, encoding='utf-8').read()
    missing = [n for n in map(int, re.findall(r'@@P(\d+)@@', text)) if n not in tr]
    text = re.sub(r'@@P(\d+)@@', lambda m: tr.get(int(m.group(1)), m.group(0)), text)
    open(final, 'w', encoding='utf-8').write(text)
    print('missing', missing)


if __name__ == '__main__':
    {'draft': draft, 'merge': merge}[sys.argv[1]](*sys.argv[2:])
