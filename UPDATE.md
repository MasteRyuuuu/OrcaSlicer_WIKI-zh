# 同步更新流程

英文 wiki（`upstream.json` 里的仓库，目前是 OrcaSlicer/OrcaSlicer_WIKI）有新提交时，按下面的步骤更新中文版。定时任务和手动更新都用这一套流程。

原则：只重译英文变了的部分，没变的中文原样保留；术语和排版遵守 `work/STYLE.md`。

所有命令都在仓库根目录运行，而且要在 `zh-cn` 分支上运行。`main` 分支是官方英文原稿，不要动它。克隆时用 `git clone -b zh-cn <仓库地址>`。

## 0. 环境（新会话先做一次）

```bash
pip install --break-system-packages -q -r requirements.txt
npm ci --prefix node --silent        # KaTeX，构建公式用
```

还需要 `mmdc`（Mermaid CLI，流程图有变化时才会用到）和 Playwright（截图检查用），云端环境里已经预装。

## 1. 检查有没有更新

```bash
python3 -I scripts/sync.py status
```

- 输出 `UP-TO-DATE`（退出码 0）时，说明没有新内容。**到此结束**：不提交，也不发布。
- 退出码 3 表示有新提交。命令会列出新提交和改动的文件。

## 2. 生成草稿

```bash
python3 -I scripts/sync.py plan
```

然后读 `work/sync/REPORT.md`。`plan` 会自动做下面这些事：

- 把 `work/en`、`work/meta` 换成新的英文预处理稿。
- 英文没变的段落沿用原来的中文。占位符编号变了的，会自动改成新编号。
- 只有链接、代码或元数据变化的页面会自动处理。页面改名和删除也会自动处理。
- 英文有改动或新增的段落，会在 `zh/` 对应页面里标成 **TODO 块**。
- 表格只改了几行时，只有改动的行会标成 TODO。
- 版本发布页（摘要模式）会生成 `work/rel/<key>.todo.tsv`。
- 刷新术语提示 `work/hints/`。

## 3. 翻译

先读 `work/STYLE.md`。

### 3a. TODO 块

格式如下：

```
<<<TODO#3
[EN-NEW]
新的英文（要翻译的内容）
[EN-OLD]
旧的英文（参考）
[ZH-OLD]
旧的中文（参考；占位符已换成新编号，对应不上的写成 {{?L3}}）
TODO#3>>>
```

把从 `<<<TODO#n` 到 `TODO#n>>>` 的**整个块**换成 `[EN-NEW]` 的中文译文。要求：

- 只翻译 `[EN-NEW]` 的内容。行和空行的结构要和 `[EN-NEW]` 一致，表格仍然一行一行写。
- 占位符（`{{C1}} {{L2}} {{I1}} {{U1}} {{M1}} {{T1}}`）使用 `[EN-NEW]` 里的编号，每个恰好出现一次。单独成行的占位符仍然单独成行。
- 旧中文里还能用的说法尽量沿用，只改英文变了的部分。
- 术语提示在 `work/hints/<页面路径>.txt`。标 H 的是软件官方中文界面的译名，要优先使用。
- 翻译对照表页（`developer_reference/localization_glossary.md`）的中文表格只保留"英文 / 说明 / zh_CN / zh_TW"四列。改动的行也按这个格式写。

### 3b. 新页面

```bash
scripts/show.sh <页面路径>      # 例如 scripts/show.sh calibration/flow_ratio_calib
```

这个命令会显示术语提示和英文。整页翻译后，写到 `zh/<同路径>.md`。标题的数量、级别和顺序必须和英文一致。

### 3c. 版本发布页（只译概述和每项标题）

1. `work/rel/<key>.todo.tsv` 每行的格式是 `键<TAB>英文`。
2. 把译文按 `键<TAB>中文` 追加到 `work/rel/<key>.zh.tsv`。多行内容写 `\n`。
3. 删除 todo 文件。
4. 运行 `python3 -I scripts/rel_build.py <key>`，输出里应该有 `missing 0`。

新版本页可以运行 `python3 -I scripts/rel_parse.py <key>` 看编号大纲，写法参照已有的 `work/rel/*.zh.tsv`。

### 3d. 导航新分组

`REPORT.md` 里列出的新分组，要在 `scripts/build.py` 的 `SEC_ZH` 里加上中文名。

## 4. 校验和构建

```bash
python3 -I scripts/sync.py verify     # 必须输出 OK
python3 -I scripts/sync.py finish     # 把新的上游提交记进 upstream.json
python3 -I scripts/build.py
python3 -I scripts/linkcheck.py       # broken links / duplicate ids / missing images 都必须是 0
```

- `verify` 输出的 `english-looking` 只是警告。命令、代码、专有名词可以保留英文，其他的要翻译。
- 截图检查是可选的：`node scripts/shots.js site/index.html shots <页面id> ...`（页面 id 是文件名里的 `_` 换成 `-`）。

## 5. 提交并推送

```bash
git add -A
git commit -m "同步上游 <旧提交>→<新提交>：<一句话说明改了什么>"
git push origin zh-cn
```

如果没能全部完成（`verify` 或 `linkcheck` 过不了），**不要推送到 `zh-cn`**。把进度推到 `zh-cn-wip` 分支，并在汇报里说明还剩什么。

## 6. 更新中文 wiki 的网页链接（Claude artifact）

网址在 `work/ARTIFACT_URL.txt`。

1. 先用 Artifact 的 `read` 读一次：`url=<网址>`，`path="index.html"`。新会话发布前必须先读；这个文件很大，读取时只会存成本地文件。
2. 再用 `publish` 发布：
   - `url=<网址>`
   - `file_path=<仓库绝对路径>/site/index.html`
   - `root=<仓库绝对路径>/site`
   - `files`：本次新增或改动的图片，路径相对于 `site/`。可以用 `git diff --name-only --diff-filter=AM HEAD~1 -- site/img | sed 's#^site/##'` 列出来。
   - 不传 `icon`。

## 7. 汇报

用中文写几句：上游改了什么，中文版更新了哪些页面，有没有遗留问题。没有更新时不需要汇报。
