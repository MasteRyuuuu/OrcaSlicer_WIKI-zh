# OrcaSlicer Wiki 中文版（非官方）

这是 OrcaSlicer 官方 wiki 的简体中文翻译，英文源仓库是 [OrcaSlicer/OrcaSlicer_WIKI](https://github.com/OrcaSlicer/OrcaSlicer_WIKI)。

> 本仓库是官方 wiki 仓库的 fork：
> - `main` 分支：官方英文原稿；
> - `zh-cn` 分支（本分支）：中文版。

译文生成为一个单页网站，下载仓库后用浏览器打开 `site/index.html` 就能浏览，不需要联网。

- 界面术语以 OrcaSlicer 官方简体中文版（zh_CN）为准，标题旁附英文原名。
- 每页都有"英文原文"链接。
- 版本发布说明只翻译了概述和每项更新的标题，细节请看英文原文。
- 支持搜索、浅色/深色模式和手机浏览。

当前译文对应的英文版本记录在 `upstream.json`（提交号、日期、提交说明）。

## 自动更新

定时任务每周运行一次 `scripts/sync.py`。英文 wiki 有新提交时，它会：

1. 只重译改动的段落，没变的中文保留不动；
2. 重新生成网站；
3. 推送到本仓库。

完整流程见 [UPDATE.md](UPDATE.md)。

## 目录

| 路径 | 内容 |
| --- | --- |
| `zh/` | 中文译稿（Markdown）。代码、链接、图片等用 `{{C1}}` `{{L1}}` `{{I1}}` 这类占位符代替，构建时还原 |
| `work/en/`、`work/meta/` | 与译稿对应的英文预处理稿，以及占位符代表的原文 |
| `work/STYLE.md` | 翻译约定与术语表 |
| `work/rel/` | 版本发布页的摘要翻译（TSV） |
| `work/hints/`、`work/terms.json` | 每页的术语提示（来自软件官方中文界面和 wiki 术语表） |
| `scripts/` | 预处理、校验、构建、同步脚本 |
| `site/` | 生成的网站 |

## 本地构建

```bash
pip install -r requirements.txt
npm ci --prefix node
python3 scripts/sync.py src      # 拉取对应版本的英文 wiki（图片和导航来自这里）
python3 scripts/build.py         # 生成 site/
python3 scripts/linkcheck.py     # 检查链接和图片
```

## 版权

wiki 内容版权归 OrcaSlicer wiki 的原作者所有。本仓库只是非官方的中文翻译，以英文原文为准。
