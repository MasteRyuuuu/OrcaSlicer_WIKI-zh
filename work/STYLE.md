# 翻译约定（每次接续工作先读这里）

流程：`scripts/show.sh <页面相对路径>` 看术语提示和英文 → 写入 `zh/<同路径>.md` → `python3 -I scripts/check.py` 校验。

## 结构
- 占位符 `{{C1}} {{M1}} {{I1}} {{L1}} {{U1}} {{T1}}` 原样保留、每个恰好一次；单独成行的保持单独成行。
- `{{T1}}`（页内目录）、`{{M1}}`（模式/变量等元数据）由构建脚本生成中文，不要展开。
- 标题数量、级别、顺序必须与英文一致；标题只写中文（构建时自动附英文原名）。
- `> [!NOTE]` 等提示框标记、表格结构、列表缩进（4 空格）保持不变。
- mermaid 代码块里只翻译标签文字。公式 `$...$` 保留，`\text{}` 里的英文可译。

## 术语
- 设置项名称优先用提示里标 H 的官方中文界面译名；正文首次提到时可括注英文。
- 常用：wall/perimeter 墙；infill 填充；sparse infill 稀疏填充；solid infill 实心填充；top/bottom surface 顶面/底面；shell 外壳；seam 接缝；line width 线宽；flow ratio 流量比例；overhang 悬垂；bridge 桥接；support 支撑；raft 筏层；brim Brim；skirt 裙边；retraction 回抽；travel 空驶；wipe 擦拭；z hop Z 抬升；prime/wipe tower 擦拭塔；purge/flush 冲刷；ooze 渗料；stringing 拉丝；warping 翘边；first/initial layer 首层；bed/build plate 热床/打印板；nozzle 喷嘴；hotend 热端；extruder 挤出机；filament 耗材丝（预设类叫"耗材"）；preset 预设；profile 配置（文件）；slice 切片；pressure advance 压力提前（PA）；max volumetric speed 最大体积流量；input shaping 输入整形；ringing 振纹；jerk 抖动（Jerk）；junction deviation 结点偏差；acceleration 加速度；fuzzy skin 绒毛表面；ironing 熨烫；gyroid 螺旋体；spiral vase 旋转花瓶；feature/extrusion role 走线类型/挤出类型；modifier 修改器；toolhead 工具头；tool change 换工具头；ramming 尖端成型。
- 模式：Simple 简单，Advanced 高级，Expert 专家，Developer 开发者。
- OrcaSlicer、G-code、Klipper、Marlin、RepRapFirmware、Bambu、Prusa 等专有名词保留英文。

## 排版
- 中文句子用全角标点（，。：；（）？！），代码/数字/英文内部保持半角。
- 中英文、中文与数字之间加空格；单位保留（mm、mm/s、mm³/s、°C、%）。
- 语气：平实、准确的技术文档中文，不加译者评论；原文的强调（粗体/斜体）保留。

## 发布
- 站点：`python3 -I scripts/build.py` → docs/index.html + docs/img/（推送 zh-cn 后 GitHub Pages 自动发布公开网站）；artifact URL 见 work/ARTIFACT_URL.txt
- 再发布：Artifact publish url=<ARTIFACT_URL> file_path=<仓库>/docs/index.html，root=<仓库>/docs；新增/改动的图片才需要 files。新会话发布前先 Artifact read（path=index.html）一次。详见 UPDATE.md 第 6 步。
- 渲染检查：`node scripts/shots.js docs/index.html <outdir> <hash...>`

## 进度备忘
- 已完成：全部 164 页（用户文档 + 全部开发者参考 + 版本发布）均已翻译，v8 已发布到同一链接（work/ARTIFACT_URL.txt）。版本发布页为摘要模式（概述 + 各项标题，详情链接英文原文），流程见 scripts/rel_parse.py / rel_build.py。
- 最终检查：内部链接/锚点 0 失效、0 重复 id；桌面/暗色/手机三种模式无横向溢出、无缺图。GitHub 风格锚点（`--`）由 slug_gh 别名兼容。
- 英文 wiki 更新时按 UPDATE.md 走：`scripts/sync.py status → plan → 译 TODO → verify → finish → build → linkcheck`。上游源仓库是 OrcaSlicer/OrcaSlicer_WIKI（与 GitHub wiki 内容完全一致，提交说明更有用），当前对应提交见 upstream.json。
- build.py 已支持 mkdocs `!!! kind "标题"` 提示框，并会去掉中文段落内的软换行（避免多出空格）。
- 用语：Speed Dial 快捷面板；reference plane 基准面；Primitive 标准模型；offer menu 操作菜单；Section view 剖面视图。
- 纹理置换术语：Bake 烘焙、Midlevel 中间值、Resolution 分辨率、Budget 预算、layer 图层、island UV 岛、texture seam 切缝、Unwrap 展开、Frame 适配视图；Color Painting 页 = 涂色。
- Brim 类型 Mouse ears 用官方译名"圆盘"。大页面里大量格式化行可写小脚本批量转换（见 scripts/patterns_draft.py 的做法）。
