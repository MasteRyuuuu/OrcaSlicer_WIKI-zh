# 插件开发

本页介绍如何为 OrcaSlicer 编写 Python 插件，以及如何在 C++ 中添加新的插件类型。Python 插件运行在内嵌的 CPython 解释器中，因此无需重新编译应用程序就能扩展 OrcaSlicer。

本页面向两类读者：

1. **插件作者**——编写新的 Python 插件、修改现有插件，并在开发过程中调试它。
2. **OrcaSlicer 贡献者**——在 C++ 中添加全新的*插件类型*（一种新的约定，Python 插件可以实现它，应用会在其工作流程中的某个位置调用它）。

相关的插件开发页面涵盖相邻的主题：

- [API 参考]({{L1}})——内嵌的 `orca` 模块、注册、宿主访问、UI 辅助工具，以及各个功能模块。
- [插件审计钩子]({{L2}})——CPython 审计钩子：在插件代码执行敏感的文件系统、网络或启动进程操作之前提示用户，并记住用户的答复。任何添加新 trampoline 方法的人都必须阅读它；每次 C++ 到 Python 的调用都会开启一个审计上下文。
- [插件系统概览]({{L3}})——系统中目录、加载器和云端订阅这一侧的内容（发现、安装、更新）。

> [!NOTE]
> 除非另有说明，下文中的所有文件路径都位于 `src/slic3r/plugin/` 之下。

## 第 1 部分：Python 插件开发

### 插件存放在哪里，如何被发现

插件从 OrcaSlicer 数据目录（`data_dir()`）下的两个根目录加载：

| 根目录 | 用途 |
|---|---|
| `data_dir()/orca_plugins/` | 本地安装 / 手动加载的插件 |
| `data_dir()/orca_plugins/_subscribed/<user_id>/` | 云端订阅的插件 |

每个插件位于**自己的子目录**中，其中恰好包含一个入口文件：要么是单个 `.py` 文件，要么是单个 `.whl`（wheel）。名称以 `.` 或 `__` 开头的子目录会被忽略。发现过程由 `PluginCatalog`（扫描）和 `PluginLoader`（加载）驱动；参见 `PluginCatalog.cpp` 和 `PluginLoader.cpp`（由 `PythonFileUtils.cpp` 中的 `find_installed_plugin_entry` 决定文件夹中哪个文件是入口点）。

> [!NOTE]
> **仓库中没有附带示例插件。** 本文档中的插件代码片段仅作说明。它们是按照下面真实的绑定编写的，但并不是从某个已发布、已验证的插件中复制来的。请把它们当作起点，并自行测试。

### 插件的结构

插件以**两种形式之一**打包，文件夹中的入口文件决定了是哪一种：

- **单个 `.py` 文件**——最简单的形式，下面首先介绍。元数据位于文件顶部的 PEP 723 注释块中。
- **wheel（`.whl`）**——普通的已构建 Python 包，适用于需要多个模块或编译代码的插件。元数据来自 wheel 自身的文件，而不是 PEP 723 注释块。参见下文的 [wheel（`.whl`）插件]({{L4}})。

**一个插件，多项功能。** 插件是一个*包*，注册一项或多项**功能**（capability）。每项功能都是一个有类型的功能单元：可以运行的脚本、G-code 后处理器、打印机代理，并有自己的显示名称。插件的*类型*由它注册的功能推导而来（它们是描述性的标签，而不是单一固定的角色），因此一个插件可以同时提供脚本功能和后处理功能。

**两种形式的注册方式相同**：OrcaSlicer 导入你的代码，实例化你用 `@orca.plugin` 标记的那一个**包类**，并调用它的 `register_capabilities()` 方法来收集它提供的功能。不同的只是打包方式和元数据来源。

单文件（`.py`）插件由三部分组成：

1. 一个 **PEP 723 内联元数据块**（一段特殊的注释头），声明身份信息和依赖。
2. 一个或多个**功能类**，每个都继承内嵌 `orca` 模块提供的某个有类型的基类（脚本、切片流水线或打印机代理功能），并实现 `get_name()` 以及它的入口方法。
3. 一个用 `@orca.plugin` 装饰的**包类**（继承 `orca.base`），它的 `register_capabilities()` 方法为每项功能调用一次 `orca.register_capability(...)`。

#### 1. 元数据块（PEP 723）

OrcaSlicer 从 PEP 723 *内联脚本元数据*块中读取身份信息和依赖元数据：这是一个以 `# /// script` 和 `# ///` 为界的注释块，每一行内容都以 `# ` 开头。身份字段位于 `[tool.orcaslicer.plugin]` 表中；依赖字段位于 TOML 根部。解析由 `PythonFileUtils.cpp::parse_pep723_toml` / `read_python_plugin_metadata` 实现。

{{C1}}

| 字段 | 位置 | 是否必需 | 说明 |
|---|---|---|---|
| `name` | `[tool.orcaslicer.plugin]` | 建议填写 | 插件对话框中的显示名称 |
| `description` | `[tool.orcaslicer.plugin]` | 建议填写 | 显示在插件的**描述**选项卡中 |
| `author` | `[tool.orcaslicer.plugin]` | 可选 | |
| `version` | `[tool.orcaslicer.plugin]` | 建议填写 | |
| `dependencies` | TOML 根部 | 可选 | pip 依赖项数组（参见[依赖]({{L5}})） |
| `requires-python` | TOML 根部 | 可选 | 目前**会被读取，但不会保存，也不会**针对捆绑的解释器强制检查 |

> [!NOTE]
> 元数据块不再声明 `type`。插件的类型由它注册的功能类推导而来（每项功能的 `get_type()`），所以无论插件提供一项还是多项功能，都使用同样的元数据块。PEP 723 解析器（`parse_pep723_toml`）只读取 `name`、`description`、`author`、`version`、`requires-python` 和 `dependencies`；其他任何键（包括误写的 `type = ...`）都会被忽略。`.whl` 插件也是如此：身份信息来自 wheel 的 `METADATA`，所提供的类型来自已注册的功能。

#### 2. 插件 API

详细的 API 参考分为[注册]({{L6}})、[宿主]({{L7}})、[宿主 UI]({{L8}})、[生命周期事件]({{L9}})、[脚本]({{L10}})、[页面]({{L11}})、[切片流水线]({{L12}})、[资源纹理]({{L13}})和[打印机代理]({{L14}})几部分。下面的摘要介绍编写插件时用到的主要符号。

解释器只提供一个名为 **`orca`** 的内嵌模块（`PythonPluginBridge.cpp` 中的 `PYBIND11_EMBEDDED_MODULE(orca, ...)`）。它提供功能基类、包基类和功能注册，还有 **`orca.host`** 子模块，用于只读访问实时的切片模型图、预设和网格几何（参见 [`orca.host` 模块]({{L15}})）。其中包含：

| 符号 | 种类 | 成员 / 用途 |
|---|---|---|
| `orca.PluginType` | 枚举 | `PrinterConnection`、`Pages`、`Analysis`、`Importer`、`Exporter`、`Visualization`、`Script`、`SlicingPipeline`、`ResourceTexture`、`Unknown` |
| `orca.PluginResult` | 枚举 | `Success`、`Skipped`、`RecoverableError`、`FatalError` |
| `orca.PluginContext` | 类 | 基础上下文，字段 `orca_version: str` |
| `orca.ExecutionResult` | 类 | 字段 `status`、`message`、`data`；工厂方法见下文 |
| `orca.LifecycleEvent`、`orca.LifecycleEvtCode`、`orca.LifecycleEventContext` | 枚举 / 枚举 / 类 | 传给 `on_lifecycle_event` 的事件、结果代码和数据（[生命周期事件]({{L16}})） |
| `orca.PythonPluginBase` | 类 | 根**功能**基类；子类必须实现 `get_name()` |
| `orca.base` | 类 | **包**基类；继承它并重写 `register_capabilities()` |
| `orca.plugin` | 装饰器 | 标记文件中唯一的包类（每个文件恰好一个） |
| `orca.register_capability(cls)` | 函数 | 注册一个功能类；在 `register_capabilities()` 内部调用 |
| `orca.request_permissions(...)` | 函数 | 预先声明文件系统、网络、进程和线程权限；注册后合并为一次提示（[注册]({{L17}})） |
| `orca.pages` | 子模块 | [页面]({{L18}})：`PagesPluginCapabilityBase`，主窗口中的插件选项卡 |
| `orca.slicing` | 子模块 | [切片流水线]({{L19}})：`Step`、`SlicingPipelineContext`、`SlicingPipelineCapabilityBase` |
| `orca.script` | 子模块 | `ScriptPluginCapabilityBase` |
| `orca.resource_texture` | 子模块 | `ResourceTexturePluginCapabilityBase` 和 `get_texture_dir()` |
| `orca.printer_agent` | 子模块 | `PrinterAgentBase` 及其数据类型 |
| `orca.host` | 子模块 | 只读的宿主访问：实时 `Model` 图、预设/配置包，以及零拷贝的网格几何 |

`ExecutionResult` 是插件报告运行结果的方式：

{{C2}}

- `status`——一个 `orca.PluginResult`。
- `message`——供人阅读的文本；错误/结果对话框中显示的就是它。
- `data`——一个自由格式的字符串，其含义由插件/工作流程定义（框架不解释它）。

#### 功能配置

无论功能类型是什么，每项功能都有一份 JSON 配置。插件对话框中的**配置**选项卡使用宿主的 JSON 编辑器，除非该功能提供了自定义的 HTML 界面。全局配置保存在 `data_dir()/orca_plugins/config.json` 中，以完整的功能身份（插件键、功能类型和功能名称）为键。

配置方法位于 `orca.PythonPluginBase` 上：

| 方法 | 用途 |
|---|---|
| `has_config_ui() -> bool` | 返回 `True` 时，使用 `get_config_ui()` 返回的自定义界面，而不是 JSON 编辑器。 |
| `get_config_ui() -> str` | 返回一个自包含的 HTML 字符串。结果为空或出错时，退回到 JSON 编辑器。 |
| `get_default_config() -> str` | 重写该方法并返回一个 Python `dict`；OrcaSlicer 会把得到的 JSON 作为字符串提供，并在用户恢复全局默认值时使用它。不重写时，默认值为 `{}`。 |
| `get_config() -> str` | 以 JSON 字符串返回该功能实际生效的已保存配置。没有保存过配置时为 `{}`。 |
| `get_config_version() -> str` | 返回最后一次保存该配置的插件版本。可以用它检测并迁移旧的配置结构。 |
| `save_config(config: str) -> bool` | 为该功能持久保存一个 JSON 字符串。使用 `json.dumps(config_dict)`，并检查返回值。 |

示例：

{{C3}}

`save_config()` 会自动提供插件身份和当前版本；插件无法通过这个 API 写入其他功能的配置。针对预设的覆盖配置在预设的插件配置对话框中编辑，并保存在预设内部。存在覆盖配置时，`get_config()` 返回覆盖配置；否则返回全局配置。

要使用自定义界面，请从 `get_config_ui()` 返回一个完整的页面，并让 `has_config_ui()` 返回 `True`：

{{C4}}

该页面运行在沙箱化的框架中。它只能通过注入的 `window.orca.getConfig()` 和 `window.orca.saveConfig(value)` 桥接读写配置；请让页面保持自包含，不要假设可以同源访问宿主。

#### `orca.host` 模块：只读的宿主访问

`orca.host`（在 `src/slic3r/plugin/host/` 中绑定）让插件可以**只读**访问正在运行的切片软件。它面向分析、报告和导出类插件；这里没有任何东西会修改模型。**脚本插件在主线程/UI 线程上运行**，所以在一次 `execute()` 期间模型不会在你手下发生变化；**切片流水线插件在后台线程上运行**，同时 GUI 继续运行；**打印机代理的方法可能在 UI 线程上调用**（选择、发现、连接、注册回调），**也可能在任务线程上调用**（`start_*` 打印/发送任务）。无论哪种情况，都要把一切当作瞬时快照，不要跨运行保存引用。

**入口点**（如果在 GUI/模型就绪之前调用，每个入口点都会抛出 `RuntimeError`）：

{{C5}}

**模型图：** `Model.objects()` -> `ModelObject`；每个对象有 `volumes()`/`volume(i)`（-> `ModelVolume`）和 `instances()`/`instance(i)`（-> `ModelInstance`）。包围盒是值类型 `host.BoundingBox`（`min`/`max`/`size`/`center` 为以 mm 为单位的 `(x, y, z)` 元组，另有 `radius`/`defined`）。

**网格几何：** `ModelVolume.mesh()` -> `host.TriangleMesh`

| 成员 | 返回值 | 说明 |
|---|---|---|
| `vertex_count()` / `triangle_count()`（`facets_count()`）/ `is_empty()` | `int` / `bool` | 不需要 numpy |
| `vertex(i)` / `triangle(i)` | `(x, y, z)` / `(a, b, c)` 元组 | 不需要 numpy，带边界检查 |
| `vertices()` | `(N, 3)` float32 ndarray | **只读、零拷贝**，需要 numpy |
| `triangles()` | `(M, 3)` int32 ndarray | 顶点索引；**只读、零拷贝**，需要 numpy |
| `face_normals()` | `(M, 3)` float32 ndarray | 计算得到的副本，需要 numpy |
| `volume()` / `bounding_box()` / `is_manifold()` | `float` / `BoundingBox` / `bool` | 不需要 numpy |

坐标是**局部**坐标（该体积自身的坐标系，单位为 mm）。`vertices()`/`triangles()` 数组是实时网格的零拷贝视图，并被标记为只读；向其写入会抛出 `ValueError`。它们的生命周期绑定在一个不可变的网格快照上，所以即使该体积的网格之后被替换，它们依然有效。

**完整示例**（在 PEP 723 块中声明 numpy，让捆绑的 `uv` 安装它）：

{{C6}}

> [!NOTE]
> 如果实例是镜像的（`instance.is_left_handed()` 为 `True`，即 `det(M) < 0`），在世界空间中计算朝外的法线时，要翻转三角面的绕序 / 对面法线取反。

**numpy 要求：** `vertices()`、`triangles()`、`face_normals()` 以及 `ModelVolume`/`ModelInstance` 上的 `matrix()` 访问器需要 numpy，如果没有安装会抛出明确的 `ImportError`（请声明 `dependencies = ["numpy"]`）。其他一切——计数、`vertex(i)`/`triangle(i)`、`volume()`、`bounding_box()`、`is_manifold()`，以及 `offset`/`rotation`/`scaling_factor`/`mirror` 元组访问器——都不需要 numpy。

#### `orca.host.ui` 模块：对话框和交互窗口

`orca.host.ui` 让插件可以显示由宿主管理的界面：原生消息框、原生进度对话框、模态 HTML 对话框、非模态交互窗口，以及停靠在 3D 视图旁的面板。**插件绝不能导入自己的 GUI 工具包**（PyQt/wxPython/tkinter）：`script` 插件与宿主共用 UI 线程，第二个工具包的事件循环会与 wxWidgets 冲突；而 `gcode`/`printer-agent` 插件可能在非主线程上运行，在那里调用工具包会导致崩溃。这些宿主调用会替你在主线程上运行，并阻塞调用代码直到返回。

{{C7}}

`message` 的参数：`buttons` 为 `"ok"|"ok_cancel"|"yes_no"|"yes_no_cancel"`；`icon` 为 `"info"|"warning"|"error"|"question"`。

**停靠面板：**

`create_dock_panel()` 把你的页面放进与侧边栏同一停靠区域中的一个窗格里，而不是单独的窗口。用户可以把它拖到另一侧边缘、让它浮动、调整大小或关闭它。再次打开时，它会回到上次保存窗口布局时的位置和大小——布局在新建项目时保存，而不是在退出时保存。`dock` 为 `"left"`、`"right"`、`"bottom"` 或 `"float"`；`width` 和 `height` 以 DIP 为单位。它属于"准备"和"预览"选项卡，用户切换到其他选项卡时会隐藏。

{{C8}}

页面与插件通信的方式与窗口完全相同，只有 `orca.submit()` 例外，它只适用于模态对话框。

**进度对话框：**

使用 `create_progress_dialog()` 显示由宿主管理的原生进度对话框。它返回一个 `ProgressDialog` 句柄，也可以作为上下文管理器使用，退出时会自动调用 `close()`。默认样式为 `PD_APP_MODAL | PD_AUTO_HIDE`；如果允许用户取消，请加上 `PD_CAN_ABORT`。`maximum` 默认为 `100`（`<= 0` 的值按 `100` 处理）。

对于脚本插件，请把对话框放在 `execute(self)` 内部，并在各段工作之间更新它。不要先创建对话框，然后执行一个长时间不间断的操作，例如单次 `time.sleep(...)` 或阻塞的网络调用；只有在你调用 `update()` 或 `pulse()` 时，对话框才有机会重绘和检查是否取消。

{{C9}}

对于无法确定进度的工作，请让对话框脉动，而不是设置数值：

{{C10}}

句柄方法：

| Python 调用 | 效果 |
|---|---|
| `progress.update(value, message="")` | 设置确定的进度值；如果已关闭/取消则返回 `False` |
| `progress.pulse(message="")` | 推进一步不确定进度；如果已关闭/取消则返回 `False` |
| `progress.start_pulse(interval_ms=100, message="")` | 在 UI 线程上启动由定时器驱动的脉动 |
| `progress.stop_pulse()` | 停止由定时器驱动的脉动 |
| `progress.close()` | 关闭对话框 |
| `progress.is_open()` | 返回宿主是否仍登记着该对话框 |

由于 `start_pulse()` 没有返回值，如果对话框包含 `PD_CAN_ABORT`，请在适合取消的位置显式调用 `update()` 或 `pulse()`。

`orca.host.ui` 提供的样式常量与 `wxProgressDialog` 对应：`PD_APP_MODAL`、`PD_AUTO_HIDE`、`PD_CAN_ABORT`、`PD_CAN_SKIP`、`PD_ELAPSED_TIME`、`PD_ESTIMATED_TIME` 和 `PD_REMAINING_TIME`。`PD_CAN_SKIP` 是为了保持样式一致而提供的，但当前的 Python 句柄并不提供单独的"跳过"状态。

**页面通过 `window.orca` 回传消息**（自动注入；页面提供原始的、自包含的 HTML/CSS/JS）：

| JS 调用 | 效果 |
|---|---|
| `orca.postMessage(obj)` | 把 `obj` 传给插件的 `on_message(obj)` |
| `orca.onMessage(cb)` | 每次 `win.post(data)`（以及模态推送）时运行 `cb(data)` |
| `orca.submit(obj)` | （模态）关闭并从 `show_dialog` 返回 `obj` |
| `orca.close()` | 关闭对话框 / 窗口 |

**主题（自动适配浅色/深色）：**

宿主会在你的页面渲染*之前*注入一份与 OrcaSlicer **当前主题**（当前的浅色/深色模式、字体、背景/前景色、强调色和边框颜色）相匹配的样式表。即使不写任何样式，页面看起来也已经很原生：`<body>`、标题、`button`、`input`/`select`/`textarea`、`table`、链接和滚动条都有合理的主题化默认样式；主题还以 CSS 变量的形式提供，方便你与界面的其他部分保持一致：

| 变量 | 含义 |
|---|---|
| `--orca-bg` | 窗口/背景颜色 |
| `--orca-fg` | 主要文字颜色 |
| `--orca-muted` | 次要 / 标签文字颜色 |
| `--orca-accent` | 强调色（按钮、链接、焦点） |
| `--orca-accent-fg` | 强调色上的文字颜色 |
| `--orca-border` | 细边框 / 分隔线 / 行悬停颜色 |
| `--orca-font` | 界面字体栈 |

注入的规则只使用低优先级的选择器，从不使用 `!important`，所以**页面自带的任何 CSS 都会覆盖它们**。请优先使用这些变量（例如 `border:1px solid var(--orca-border)`），而不是写死颜色，这样对话框就能自动适配浅色*和*深色模式。UI 示例 `host_ui_panel.py` 就依赖于此，没有使用任何固定颜色。

**线程与生命周期：**

- 宿主 UI 调用在主线程上运行，并**阻塞调用代码**直到返回（`message`/`show_dialog` 在对话框关闭时返回；`create_window`/`create_progress_dialog` 在窗口/对话框显示出来后立即返回；进度更新在宿主应用之后返回）。在本来就在 UI 线程上的 `script` 插件中，它们直接内联运行；在后台线程插件（`gcode`/`printer-agent`）中，它们会先被调度到主线程。
- `on_message(data)` 在 **UI 线程**上运行；请保持简短，把繁重的工作交给 `threading.Thread`，再用 `win.post(...)` 把结果推送回来。
- **模态**对话框（`show_dialog`）适合一次性的 `execute()`。**常驻**面板（`create_window` 或 `create_dock_panel`）最好在 `on_load()` 中打开，使其在插件的整个生命周期内存在；插件被卸载/重新加载或应用退出时，宿主会自动关闭插件的窗口和面板，且不会调用 `on_close`。
- 内容以原始 HTML 形式加载；请尽量使用**自包含**的页面（内联 CSS/JS）。没有 CSP，开发者工具也被禁用。

`host_ui_panel.py` 是一个非模态交互面板的示例，可以浏览整个只读的 `orca.host` API。

**通知：** `orca.host.ui.push_notification(level, text, hyper_text="", on_click=None)` 在 3D 视图中显示一条通知，可以附带一个可单击的链接。参见[盘面通知]({{L20}})。

#### 3. 注册

注册分为两部分，都在**模块导入/加载时**完成。

**功能**——每项功能都是一个类，继承某个有类型的基类（参见[功能类型和入口点]({{L21}})），并实现 `get_name(self) -> str`。名称决定了功能在界面中如何显示、预设如何引用它，因此它必须**在插件内唯一**，并且**不能包含 `;`**。这个字符被保留为预设引用中的分隔符，功能名称中出现 `;` 会导致加载失败。

**包**——每个文件中恰好有一个类用 `@orca.plugin` 装饰并继承 `orca.base`。它的 `register_capabilities(self)` 方法为你想提供的每个功能类各调用一次 `orca.register_capability(Cls)`：

{{C11}}

OrcaSlicer 实例化包类（必须能以 `SamplePlugin()` 的形式无参数调用），调用 `register_capabilities()`，然后实例化每项已注册的功能。`orca.request_permissions(...)` 是可选的；调用它时，声明会在注册期间收集起来，并**在 `register_capabilities()` 返回之后、创建任何功能实例之前，显示为一个合并的"是/否"对话框**。已经授予该插件的目标不会再次询问，拒绝请求则会以错误中止加载。参数见[注册]({{L22}})，授权如何强制执行见[插件审计钩子]({{L23}})。

插件加载时强制执行的规则（大部分位于 `PythonPluginBridge.cpp`）：

- `@orca.plugin` 类**必须**继承 `orca.base`，并且每个文件中**恰好只能有一个**。出现第二个 `@orca.plugin` 会导致加载失败。
- 传给 `orca.register_capability` 的每个类都必须继承某个功能基类（最终都继承自 `orca.PythonPluginBase`）；否则会抛出 `value_error`。
- 每项功能都必须能解析出 `get_name()`（在桥接层检查）；如果得到的 `(type, name)` 组合在插件内不唯一，加载器（`PluginLoader.cpp`）还会拒绝该插件。
- 从未传给 `register_capability` 的功能类对 OrcaSlicer 来说是**不可见的**，即使它在文件中有定义。
- 如果插件调用了 `orca.request_permissions(...)`，用户必须接受注册之后出现的合并对话框；拒绝会导致加载失败。

#### wheel（`.whl`）插件

如果超出单个文件的范围，例如需要多个模块、打包的资源或编译扩展，请把标准的 Python **wheel** 作为插件文件夹的入口文件。插件*代码*与 `.py` 的情况完全相同：在可导入包的顶层代码中某处（通常是它的 `__init__.py`）定义功能类，以及注册它们的 `@orca.plugin` 包类。不同的是**元数据的来源**，以及 wheel 会在安装时接受验证（`PythonFileUtils.cpp` 中的 `read_wheel_plugin_metadata`）。

身份信息和依赖从 wheel 的 `*.dist-info/` 文件中读取，而不是从 PEP 723 块中读取：

| 插件字段 | wheel 中的来源 |
|---|---|
| `name` | `METADATA` -> `Name`（**必需**） |
| `version` | `METADATA` -> `Version`（**必需**） |
| `description` | `METADATA` -> `Summary` |
| `author` | `METADATA` -> `Author` |
| `dependencies` | `METADATA` -> `Requires-Dist` |

与 `.py` 插件一样，wheel **不**声明类型。插件所提供的类型来自其 `@orca.plugin` 包类在加载时注册的功能。

安装时还会强制执行以下 wheel 规则：

- wheel 中必须恰好包含**一个 `.dist-info` 目录**，并且其中有 `METADATA`、`WHEEL` 和 `RECORD`。
- 根据 `WHEEL` 文件中的 `Tag:` 行**检查平台/ABI 兼容性**。纯 Python wheel（`*-none-any`）在任何地方都可以接受；平台相关的 wheel 必须与当前解释器的 ABI 标签和操作系统相匹配（参见 `PythonInterpreter::python_abi_tag()`）。除非确实需要编译扩展，否则请发布纯 Python 的 wheel。
- 可导入的入口包按以下优先顺序选择：核心元数据中的 `Import-Name`，然后是 `top_level.txt`（如果其中只指定了一个包），最后是规范化后的 `Name`。

### 功能类型和入口点

每个有类型的基类都定义了 OrcaSlicer 将会调用的方法，以及 `get_type()` 返回的类型。每项功能都**必须**实现 `get_name(self) -> str`。生命周期钩子 `on_load()` / `on_unload()` 是可选的，每项功能都可以使用（默认什么也不做）。任何功能还可以重写 `on_lifecycle_event(event, ctx)` 来观察应用程序事件（项目打开/保存、切片、对象和盘的编辑、预设、打印机和任务活动）；参见[生命周期事件]({{L24}})。

API 参考把各模块的细节放在单独的页面中：[脚本]({{L25}})、[页面]({{L26}})、[切片流水线]({{L27}})、[资源纹理]({{L28}})和[打印机代理]({{L29}})。

| 基类 | `get_type()` 返回 | 必需的方法 | 调用者 |
|---|---|---|---|
| `orca.script.ScriptPluginCapabilityBase` | `Script` | `get_name()`、`execute(self) -> ExecutionResult` | **插件对话框 -> 运行**操作 |
| `orca.pages.PagesPluginCapabilityBase` | `Pages` | `get_name()`、`get_ui(self) -> str` | 功能启用期间添加的一个**主窗口选项卡** |
| `orca.slicing.SlicingPipelineCapabilityBase` | `SlicingPipeline` | `get_name()`、`execute(self, ctx) -> ExecutionResult` | 配置的切片步骤，以及 **G-code 导出 / 后处理** |
| `orca.printer_agent.PrinterAgentBase` | `PrinterConnection` | `get_name()` + 约 30 个代理方法（`get_agent_info`、`connect_printer`……） | 加载时的**网络 / 打印机代理**层；只有在启用**偏好设置 > 开发者 > 实验性功能 > 使用打印机代理替代打印主机**（默认关闭）时，它才会收到打印任务，并由打印机预设的 `printer_agent` 字段选择代理 ID |
| `orca.resource_texture.ResourceTexturePluginCapabilityBase` | `ResourceTexture` | `get_name()`、`get_texture_dir(self) -> str` | 功能被具体化时由 OrcaSlicer 调用 |

> [!NOTE]
> `get_name()` 是必需的；`get_type()` 通常不是。每项功能都必须实现 `get_name()`。它在根基类上是纯虚函数，缺少重写会导致加载失败。有类型的 C++ 基类已经实现了 `get_type()`（例如 `ScriptPluginCapability::get_type()` 返回 `Script`），所以继承*有类型*基类的子类**不需要**重写它。只有直接继承**根**基类 `orca.PythonPluginBase` 的功能，才必须自己设置 `get_type()`。

> [!IMPORTANT]
> `ScriptPluginCapabilityBase.execute()` 在**主线程/UI 线程**上运行：在整个调用期间都可以安全地读取实时的宿主句柄，`orca.host.ui` 对话框也会内联打开，但运行缓慢的 `execute()` 会**冻结界面**。请保持简短；把繁重的工作交给你自己的 `threading.Thread`（它不能接触模型），并通过 `create_window` 面板呈现结果。`SlicingPipelineCapabilityBase` 在后台切片线程上运行。`PrinterAgentBase` 的方法在 UI 线程上（选择 / 发现 / 连接 / 注册回调）或任务线程上（`start_*`）调用；宿主会把代理的回调调度回 UI 线程。

切片上下文（`orca.slicing.SlicingPipelineContext`）会传给 `execute`，并在几何处理步骤中提供实时的切片图。在 `Step.psGCodePostProcess` 时，图字段为 `None`，上下文改为提供工作中的 G-code 文件：

| 字段 | 含义 |
|---|---|
| `orca_version` | OrcaSlicer 版本字符串（继承自 `PluginContext`） |
| `step` | 当前正在执行的流水线步骤 |
| `print` | 实时的打印图，在 `psGCodePostProcess` 时为 `None` |
| `object` | 对象级步骤中的当前打印对象，否则为 `None` |
| `gcode_path` | 工作中的 G-code 路径，在 `psGCodePostProcess` 时设置 |
| `host` | 导出到网络打印机时的目标主机 |
| `output_name` | 输出文件名 |
| `config_value(key)` | 解析后的打印配置值，不存在时为 `None` |
| `cancelled()` | 当前打印是否已被取消 |

> [!IMPORTANT]
> 文件系统、网络、进程和创建线程的访问都会受到审计。`execute()` 运行期间，敏感操作（读取/写入/创建/删除文件、HTTP/套接字连接、启动进程或启动线程）会用一个写明目标的"是/否"对话框提示用户；选择"是"之后会为该插件记住，同一目标不会再次提示。创建线程的权限按插件授予一次：之后在新线程中执行的工作**不会**受到审计。在预先确定的允许文件夹中进行的操作——`data_dir()`、只读的 `resources_dir()`，或（在 `psGCodePostProcess` 时）当前 G-code 文件所在的文件夹——完全不需要提示；类似 `secrets`/`cert`/`conf` 的路径则直接被阻止，同样不会提示。为了避免首次使用时的提示，请在 `register_capabilities()` 中用 `orca.request_permissions(...)` 声明你需要的权限。参见[插件审计钩子]({{L30}})。

### 完整示例

**最小的脚本插件：** 一项功能，从插件对话框运行，没有上下文。

{{C12}}

**多功能插件：** 一个包同时提供切片流水线功能*和*脚本功能。

{{C13}}

> [!NOTE]
> 当某项功能被选为某个设置的值时（例如后处理功能），预设中保存的是它的 `get_name()`。与之一起保存的完整引用是 `<plugin_name>;<cloud_uuid>;<capability_name>`，这正是功能名称不能包含 `;` 的原因。关于如何利用它来恢复缺失的插件，请参见[预设中的插件引用]({{L31}})。

### 依赖

在 PEP 723 根部的 `dependencies` 数组中列出第三方依赖。安装时，OrcaSlicer 用捆绑的 `uv` 把它们解析安装到插件的环境中（`PluginLoader.cpp`）：

{{C14}}

尽量减少依赖。每个依赖都是在与你的插件相同的审计策略下运行的代码，并且必须在安装时下载。

### 修改现有插件

1. 在 `data_dir()/orca_plugins/<plugin>/` 下找到它的文件夹（对于已订阅的插件，则在 `.../_subscribed/<user_id>/` 下）。
2. 编辑 `.py` 入口文件。如果修改了元数据块，请提升 `version`，让改动在插件对话框中可见。
3. 重新加载（参见下面的迭代工作流程）。注意，插件实例在加载时就已捕获；正在运行的 OrcaSlicer 不会察觉源代码的修改，直到插件被重新加载或应用重启。

> [!NOTE]
> 不支持直接修改 `.whl` 插件。请重新构建并重新安装 wheel。

### 错误如何呈现

错误有**三种不同的呈现方式**。知道你看到的是哪一种，就能知道发生了哪类故障。

**1. 消息框：** 显式运行时发生的*运行时*故障。在以下情况下会出现：

- 你的 `execute()` **抛出了异常**——它在 C++ 到 Python 的 trampoline 边界处被捕获，完整的回溯会被记录到日志中，然后异常被重新抛出并显示出来；或者
- 你的 `execute()` **返回了失败**（`ExecutionResult.failure(...)`，即状态为 `RecoverableError` / `FatalError`）。

对于**脚本**插件，对话框标题为 *"Script Plugin Failed"*（返回失败/成功时为 *"Script Plugin"*），正文是异常消息或你的 `ExecutionResult.message`。对于**切片流水线**插件，故障会作为切片错误抛出（`"Post-processing plugin <name> failed/raised..."`），并通过普通的切片错误途径呈现。源代码：`PluginsDialog.cpp`（`run_script_plugin`、`complete_with_error`）和 `PostProcessor.cpp`。

**2. 插件详细信息 / 描述区域：** 保存在插件描述符上的*持续*错误状态，而不是某一次运行的结果。当插件加载失败或元数据无效时，描述符会记录一个错误（`PluginDescriptor.hpp` 中的 `set_error` / `normalized_error`）；对于元数据无效的插件，**错误文本会取代**对话框中显示的描述（`PluginsDialog.cpp`）。它反映的是*状态*（"这个插件目前已损坏"），而不是某一次执行的结果。

**3. Python 日志文件：** 完整的回溯。`sys.stderr` 会同时写入：

{{C15}}

（`PythonInterpreter.cpp` 中的 `install_python_stderr_redirect`。）这是插件创建的后台线程中的错误**唯一**会出现的地方；这些错误永远不会传回 C++，也永远不会产生对话框。C++ 端的上下文（加载/发现消息）则通过 Boost 写入主会话日志。

**分别如何处理：**

- **消息框** -> 阅读消息内容，然后打开 `python_*.log` 查看回溯中的文件和行号。对话框只显示消息，不显示调用栈。
- **详细信息区域 / 诊断中的错误** -> 插件没有加载；通常是注册问题（功能没有继承有类型的基类、缺少 `get_name()`、功能名称重复，或者没有 `@orca.plugin` 包类）、导入错误，或者 `orca.request_permissions(...)` 对话框被拒绝。修复后重新加载。
- **任何被 `PermissionError` 阻止的操作** -> 用户对审计钩子针对该操作的提示回答了"否"（或被自动拒绝）。参见[插件审计钩子]({{L32}})中的*调试*一节，以及日志中的 `[AUDIT BLOCKED]` 行。

对于可以预料到的失败，**优先返回结果而不是抛出异常**：`ExecutionResult.failure(orca.PluginResult.RecoverableError, "clear user-facing reason")` 会给用户一条清晰的消息。真正的程序错误才抛出异常；这样日志中会有完整的回溯供你调试。

### 开发期间的测试与迭代

一个实用的循环：

1. **编辑**插件所在 `orca_plugins/<plugin>/` 文件夹中的源代码。
2. **重新加载**——重新打开插件对话框 / 重新触发发现过程；拿不准时就重启 OrcaSlicer（实例在加载时捕获）。
3. **运行**——脚本插件使用插件对话框中的**运行**操作；切片流水线插件则执行一次切片/导出，让流水线调用它。
4. **查看日志**——让 `data_dir()/log/python_*.log` 保持打开（例如用 `tail -f`）。回溯、`print()` 输出和审计阻止记录都会写到这里。
5. **迭代。** 对预期中的结果使用 `ExecutionResult` 消息；调用栈则依靠日志。

提示：

- 确认插件在插件对话框中显示了正确的名称和版本，并且**你注册的每项功能**都出现在其可展开的功能列表中（类型也符合预期）。从未传给 `orca.register_capability` 的功能不会出现。
- 使用小而快的输入进行开发；对于切片流水线插件，准备一个很小的测试模型，让每次导出循环都很快。
- 记住，文件系统/网络/进程/线程操作在每个插件首次使用时都会提示：意外出现的 `PermissionError` 通常意味着之前某次提示被回答了"否"——或者对于路径中带有 `secret`/`cert`/`conf` 的情况，它被直接拒绝，根本没有提示过。在非主线程上，提示会被异步发出，而本次尝试会被拒绝；接受提示后，之后的尝试才会放行。参见[插件审计钩子]({{L33}})。

## 第 2 部分：在 C++ 中添加新的插件类型

这一部分面向用新约定扩展插件*框架*的 OrcaSlicer 贡献者，例如添加一种"导入器"功能类型。系统中没有按类型*实例化*的注册表或分支：功能的 Python 类继承一个有类型的基类，包的 `register_capabilities()` 通过 `register_capability` 注册它，应用的其余部分在调用点用 `std::dynamic_pointer_cast<ConcreteType>` 访问已加载的功能实例。所以添加一种类型意味着：定义基类 + 上下文 + 结果，添加一个通过审计宏转发到 Python 的 trampoline，注册 pybind11 绑定，接入一个调用点，并把文件加入构建。

可以参考 `src/slic3r/plugin/pluginTypes/` 下现有的 `slicingPipeline`、`script` 和 `printerAgent` 类型。`script` 最简单；`slicingPipeline` 展示了实时图上下文以及每次调用的 `audit_setup` 回调；`printerAgent` 展示了一个包含大量方法的接口。

### 第 1 步：定义插件约定

创建 `pluginTypes/<type>/<Type>PluginCapability.hpp`。继承 `PluginCapabilityInterface`，把 `get_type()` 固定为你的 `PluginCapabilityType`，声明纯虚的入口方法和上下文结构体，并声明一个静态的 `RegisterBindings`。当前的切片流水线基类（`pluginTypes/slicingPipeline/SlicingPipelinePluginCapability.hpp`）是上下文的标准范例：

{{C16}}

共享的构件来自 `PythonPluginInterface.hpp`：

- `PluginCapabilityInterface`——`virtual std::string get_name() const = 0`（功能名称，由 Python 提供）、`virtual PluginCapabilityType get_type() const`（默认为 `Unknown`；有类型的基类会重写它）、虚函数 `on_load()` / `on_unload()`，以及仅限 C++ 的审计身份（`set_audit_plugin_key`）。
- `struct PluginContext { std::string orca_version; }`——你的上下文应从它派生。
- `struct ExecutionResult { PluginResult status; std::string message, data; }`，带有静态的 `success` / `skipped` / `failure`。
- `enum class PluginCapabilityType { ... }`，以及 `plugin_capability_type_to_string` / `plugin_capability_type_from_string` / `plugin_capability_type_display_name` 三个映射。

如果你的类型需要新的 `PluginCapabilityType` 值，**请把它添加到 `PythonPluginInterface.hpp` 中的枚举以及全部三个映射中**，并选定映射所转换的字符串。如果现有的值（例如 `Analysis`）合适，就复用它。

### 第 2 步：确定 API 接口

精确地确定插件必须接收和返回什么，并且**只公开这些**：

- **输入**放在上下文结构体中（仿照 `SlicingPipelineContext`）。只包含插件确实需要的数据。
- **输出**应当是一个 `ExecutionResult`（状态 + 消息 + `data` 字符串），除非你的类型确实需要更丰富的返回数据。那种情况下，定义并绑定一个小的结果结构体。
- **保持最小且稳定。** 绑定是插件所依赖的 API 接口；删除或重命名已绑定的字段/方法会破坏现有插件。宁可新增字段，也不要改变现有字段的用途，并优先选择能完成工作的最小接口。
- **避免公开切片软件/GUI 的内部类型。** 当前的 API 有意只公开普通数据（字符串、枚举）。把原始的引擎对象传给插件，会同时扩大兼容性和安全性方面的暴露面。

### 第 3 步：添加 trampoline

创建 `pluginTypes/<type>/<Type>PluginCapabilityTrampoline.hpp`。继承 `PyPluginCommonTrampoline<YourBase>`（它已经提供了 `get_name` 和 `on_load`/`on_unload` 的 trampoline），并通过 `ORCA_PY_OVERRIDE_AUDITED` 把每个虚函数转发到 Python。切片流水线的 trampoline（`pluginTypes/slicingPipeline/SlicingPipelinePluginCapabilityTrampoline.hpp`）遵循这种模式：

{{C17}}

这些宏（`PyPluginTrampoline.hpp`）在这个唯一的边界上完成两项工作：记录并重新抛出 Python 回溯，以及开启审计上下文。

{{C18}}

| 参数 | 含义 |
|---|---|
| `audit_setup` | 在审计上下文开启*之后*运行的 lambda；如果你的调用需要，可以用它执行 `add_scoped_allowed_root(...)`。不需要时传入 `[] {}` |
| `override_macro` | pybind11 自身的 `PYBIND11_OVERRIDE`（有 C++ 后备实现）或 `PYBIND11_OVERRIDE_PURE`（纯虚，没有后备实现） |
| `ret, base, name, ...` | 标准的 pybind11 重写参数 |

> [!IMPORTANT]
> 每个新的 trampoline 方法都必须经过 `ORCA_PY_OVERRIDE_AUDITED`（如果需要手动解包 Python 返回值，则直接调用 `ORCA_PY_AUDIT_SCOPE()`）。这里没有模式可选——请阅读[插件审计钩子]({{L34}})，了解你的新类型的 Python 接口可能触发的事件中，哪些会提示用户、哪些会被持久保存。

### 第 4 步：注册 Python 绑定

在 `pluginTypes/<type>/<Type>PluginCapability.cpp` 中实现 `RegisterBindings`：创建一个子模块，绑定上下文/结果结构体，并把基类与其 trampoline 一起绑定。切片流水线的实现（`pluginTypes/slicingPipeline/SlicingPipelinePluginCapability.cpp`）是这样的结构：

{{C19}}

基类以 `SlicingPipelineCapabilityBase` 的名称绑定（这是插件作者要继承的名称），并从根基类 `PythonPluginBase` 继承 `get_name`，所以这里只需绑定该类型特有的方法。然后**在 `PythonPluginBridge.cpp` 的 `bind_python_api` 中调用你的 `RegisterBindings`**，放在现有调用的旁边（找到 `// Make sure you register your bindings here` 注释）：

{{C20}}

共享的 `PluginCapabilityType` / `PluginResult` / `PluginContext` / `ExecutionResult` / `PythonPluginBase` 绑定、包基类（`orca.base`），以及 `@orca.plugin` / `orca.register_capability` 入口点，都已经在同一个函数中定义过一次。你只需要添加自己类型特有的子模块。

### 第 5 步：添加审计钩子

审计不是可选的。你在第 3 步中编写的每个 trampoline 方法都已经通过 `ORCA_PY_OVERRIDE_AUDITED` 开启了审计上下文，所以你的类型的 Python 接口执行的任何文件系统/网络/进程操作都会被自动分类、提示用户，并（对大多数类别）按插件持久保存——类别表参见[插件审计钩子]({{L35}})。如果你的类型执行了当前事件映射没有覆盖的敏感操作，请把相应的 CPython 事件添加到 `PluginAuditManager.cpp` 中的 `audit_event_categories`，而不是另外发明一套平行的检查。在最终确定 trampoline 之前，请先阅读审计文档。

### 第 6 步：把类型接入 OrcaSlicer 的工作流程

在应用的某个部分调用它之前，你的插件不会运行。选择与你的类型相符的调用模式，并仿照现有的类型来实现：

| 类型 | 调用位置 | 模式 |
|---|---|---|
| `slicingPipeline` | `Print.cpp` 和 `PostProcessor.cpp` | 解析预设中的功能引用，转换为 `SlicingPipelinePluginCapability`，构建 `SlicingPipelineContext`，并在持有 GIL 的情况下调用 `execute(ctx)` |
| `script` | `PluginsDialog.cpp`（运行操作） | `get_plugin_capability_by_name(...)`，`dynamic_pointer_cast<ScriptPluginCapability>(cap->instance)`，调用 `execute()` |
| `printerAgent` | `NetworkAgentFactory.cpp`，在 `GUI_App.cpp` 中接入 | 通过 `subscribe_on_capability_load_callback` / `subscribe_on_capability_unload_callback` 注册；回调按 `capability.type == PluginCapabilityType::PrinterConnection` 过滤，然后注册/注销一个代理 |
| `resourceTexture` | `GUI_App.cpp`（`init_plugin_gui_wiring`） | 通过功能加载/卸载回调注册；回调按 `capability.type == PluginCapabilityType::ResourceTexture` 过滤，并更新 `PluginResourceTextures`，使用方从中读取资源包的缓存目录 |

对于你的新类型，添加一个调用点（或一个功能加载回调），它应当：

1. 获取一个已加载的功能（通过 `PluginLoader::get_plugin_capabilities_by_type(...)` 或 `get_plugin_capability_by_name(...)`），并执行 `std::dynamic_pointer_cast<YourTypeCapability>(cap->instance)`；
2. 转换成功后，构建上下文，并在持有 GIL 的情况下调用你的入口方法；
3. 如果你的类型在卸载时需要清理，请在 `PluginLoader.cpp` 中按 `PluginCapabilityType` 分支的功能销毁 switch 中添加一个分支。

> [!IMPORTANT]
> 被禁用或缺失的插件绝不能改变现有行为。每条现有路径都以 `dynamic_pointer_cast` 成功（或 `type ==` 检查）为前提，并且只遍历已安装/已选择的插件，所以当没有安装你的类型的插件时，循环或回调只是什么也找不到、什么也不做。请遵循同样的模式：绝不要为一个不存在的插件类型无条件地执行任何工作。

### 第 7 步：把文件加入构建

在 `src/slic3r/CMakeLists.txt` 中，把新的 `.hpp` / `.cpp` 文件列在现有插件类型源文件的旁边（搜索 `plugin/pluginTypes/slicingPipeline/SlicingPipelinePluginCapability.cpp`；该代码块大约在第 615-623 行）：

{{C21}}

### 步骤速览

1. **枚举/映射**（如果是新类型）：在 `PythonPluginInterface.hpp` 中添加一个 `PluginCapabilityType` 值以及三个字符串映射。
2. **约定**：`pluginTypes/<type>/<Type>PluginCapability.hpp`——基类 + 上下文 + 结果 + 静态的 `RegisterBindings`。
3. **trampoline**：`pluginTypes/<type>/<Type>PluginCapabilityTrampoline.hpp`——通过 `ORCA_PY_OVERRIDE_AUDITED` 转发每个虚函数。
4. **绑定**：`pluginTypes/<type>/<Type>PluginCapability.cpp` 中的 `RegisterBindings`，然后在 `PythonPluginBridge.cpp` 的 `bind_python_api` 中调用它。
5. **审计**：按照[插件审计钩子]({{L36}})确认你的类型的 Python 接口可能触发的事件都被正确分类。
6. **工作流程**：添加执行转换并调用的调用点 / 加载回调；加上判断，使类型不存在时什么也不做。
7. **构建**：把文件加入 `src/slic3r/CMakeLists.txt`。

## 第 3 部分：测试与验证

**目前没有专门针对 Python 插件系统的自动化测试套件。** 验证主要靠手动进行，对于纯 C++ 的逻辑则有针对性的 Catch2 测试。

### 手动测试

- **加载**——把插件安装/手动加载到 `data_dir()/orca_plugins/<name>/` 中，打开插件对话框，确认它以正确的名称和版本出现，并且列出了每项已注册的功能（类型也符合预期）。加载失败的插件会在诊断选项卡中显示错误（参见[错误如何呈现]({{L37}})）。
- **执行**——脚本插件：使用对话框中的**运行**操作。切片流水线插件：执行一次切片/导出，并确认插件确实运行了（例如它对 G-code 的影响，以及日志输出）。打印机代理插件：确认代理在加载时注册、在卸载时注销。
- **错误处理**——故意让插件（a）抛出异常和（b）返回 `ExecutionResult.failure(...)`；确认消息框中的文字，以及完整的回溯出现在 `data_dir()/log/python_*.log` 中。确认元数据无效的插件会在详细信息区域显示错误，而不会导致崩溃。
- **审计**——触发一次文件系统/网络/进程/线程操作，确认"是/否"对话框写明了正确的目标；回答**否**时，操作被 `PermissionError` 阻止，并在日志中出现 `[AUDIT BLOCKED]` 行；回答**是**时，操作被放行，并且授权被持久保存，重复同一操作时不会再次提示。
- **声明的权限**——在 `register_capabilities()` 中调用 `orca.request_permissions(...)`，然后重新加载：确认注册之后出现一个合并的对话框；下次加载时已授予的目标会被跳过；回答**否**会中止加载（诊断中显示错误，并且没有任何功能出现）。

### 适当的自动化测试

为不需要运行解释器或 GUI 的纯 C++ 部分添加**有针对性的 Catch2 测试**（位于 `tests/` 下）。例如：

- PEP 723 元数据解析（`PythonFileUtils.cpp` 中的 `parse_pep723_toml` / `read_python_plugin_metadata`）：有效的块、缺失的字段、格式错误的数组。
- 功能引用的解析/序列化（`Config.cpp` 中的 `parse_capability_ref`）——关于本地引用与云端引用以及格式错误的输入，参见 `tests/libslic3r/test_config.cpp` 和 `tests/slic3rutils/test_plugin_capability_identifier.cpp`。
- 允许根目录/禁止路径的逻辑（`PluginAuditManager::check_open`、`is_inside_allowed_root`、`is_denied_path_keyword`），`tests/slic3rutils/test_plugin_audit.cpp` 已经覆盖了这些：根目录内外、只读根目录、`..` 路径穿越、读与写、被禁止的文件名和关键字。参见[插件审计钩子]({{L38}})。
- 类型字符串的往返转换（`plugin_capability_type_from_string` / `plugin_capability_type_to_string`）。

凡是需要内嵌解释器、文件安装或 GUI 对话框的内容，目前最好通过上述手动步骤来覆盖。

### 跨平台与回归检查

- **跨平台**——插件代码必须能在 Windows、macOS 和 Linux 上编译和运行。注意路径处理（审计目标提取会通过 `PyOS_FSPath` 规范化路径；请继续使用 `std::filesystem` / 现有的辅助函数），以及 PEP 723 解析器中的换行符（它已经会去掉 `\r`）。
- **不得引入回归**——当没有安装某种类型的插件时，对框架的修改不能改变行为（第 6 步）。修改 trampoline/审计头文件时请注意，`PyPluginTrampoline.hpp` 和 `PluginAuditManager.hpp` 被许多编译单元包含；仅修改头文件的改动可能需要对受影响的目标进行干净的重新编译才能生效（参见审计文档的*调试*一节）。
- **向后兼容**——不要重命名或删除现有插件或已安装配置文件可能依赖的已绑定字段/方法或 `PluginCapabilityType` 值；宁可新增，也不要改变用途。

## 关键文件

| 文件 | 职责 |
|---|---|
| `src/slic3r/plugin/PythonPluginInterface.hpp` | `PluginCapabilityType`、`PluginContext`、`PluginResult`、`ExecutionResult`、`PluginCapabilityInterface`、类型字符串映射 |
| `src/slic3r/plugin/PythonPluginBridge.{hpp,cpp}` | `orca` 模块（`bind_python_api`），`@orca.plugin` / `register_capability` / `request_permissions`，包和功能的捕获/实例化 |
| `src/slic3r/plugin/PyPluginPackage.hpp` | 包基类（`orca.base`）及其 `register_capabilities` |
| `src/slic3r/plugin/PyPluginTrampoline.hpp` | `ORCA_PY_*` trampoline 宏（回溯日志 + 审计作用域）以及通用 trampoline |
| `src/slic3r/plugin/pluginTypes/<type>/` | 各类型的功能基类（`*PluginCapability.hpp/.cpp`）和 trampoline（`*PluginCapabilityTrampoline.hpp`） |
| `src/slic3r/plugin/PluginDescriptor.hpp` | 每个插件的元数据 + 错误状态（`set_error`、`normalized_error`、`is_metadata_valid`） |
| `src/slic3r/plugin/PythonFileUtils.cpp` | PEP 723 / wheel 元数据解析，入口文件发现 |
| `src/slic3r/plugin/PluginCatalog.cpp`、`PluginLoader.cpp` | 发现、安装、加载生命周期、依赖安装 |
| `src/slic3r/plugin/PythonInterpreter.cpp` | 解释器初始化、审计钩子安装、回溯格式化、`stderr` -> 日志文件 |
| `src/slic3r/GUI/PluginsDialog.cpp` | 插件对话框：详细信息/错误区域、脚本**运行**、错误对话框 |
| `src/slic3r/GUI/PostProcessor.cpp` | 解析预设中的插件引用，并在导出期间调用后处理（G-code）功能 |
| `src/slic3r/CMakeLists.txt`（约第 609-623 行） | 插件源文件的构建列表 |
| [插件审计钩子]({{L39}}) | 审计钩子：类别、提示/持久化，以及如何扩展它 |
