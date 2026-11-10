# 插件系统概览

本页介绍 OrcaSlicer Python 插件系统的架构。Python 插件运行在内嵌的 CPython 解释器中，因此用户无需重新编译应用程序或修改 C++ 核心代码，就能扩展 OrcaSlicer。

其他插件开发页面介绍实现细节：

- [插件开发]({{L1}})——如何编写 Python 插件，以及如何在 C++ 中添加新的插件类型。
- [API 参考]({{L2}})——内嵌的 `orca` 模块、注册、宿主访问、UI 辅助工具，以及各个功能模块。
- [插件审计钩子]({{L3}})——CPython 审计钩子：在插件代码执行敏感的文件系统、网络或启动进程操作之前提示用户，并记住用户的答复。

> [!NOTE]
> 除非另有说明，下文中的所有路径都位于 `src/slic3r/plugin/` 之下。

## 系统提供的能力

- **无需重新编译即可扩展**——用户把插件放进一个文件夹（或从云端订阅），OrcaSlicer 就会加载它。
- **以功能为单位，而不是单一用途的插件**——一个插件是一个*包*，注册一项或多项**功能**（capability），每项功能都是一个有类型的功能单元（例如 `post-processing`、`script`、`printer-connection`）。每种功能类型都有固定的 C++ 入口点，并在应用中的特定位置被调用；插件的"类型"就是它所注册的功能类型的集合。
- **预设会记住所用的插件**——当预设引用了某个插件功能时，完整的引用会保存在预设中，并且可以在另一台机器上从 OrcaCloud 恢复（参见[预设中的插件引用]({{L4}})）。
- **单一而窄小的 API 接口**——插件只能看到内嵌的 `orca` 模块，看不到切片软件的内部实现。
- **权限边界，而不是沙箱**——插件代码执行的文件系统、网络、启动进程和创建线程操作会被分类，并由审计钩子把关：审计钩子提示用户，并按插件记住答复；插件也可以用 `orca.request_permissions(...)` 预先声明它需要的权限。当前的覆盖范围和不足之处请参见审计文档。
- **故障隔离**——行为异常的插件会报告错误并被卸载，而不会让整个应用崩溃；回溯信息会保存到日志文件中。

## 架构概览

{{C1}}

整体分为两层：

- **编排层（C++，不涉及 Python）：** `PluginManager`、`PluginCatalog`、`CloudPluginService`、`PluginLoader`、`PluginDescriptor`。它们把插件当作数据来发现、安装和管理。
- **执行层（C++ 到 Python 的桥接）：** `PythonInterpreter`、`PythonPluginBridge`、`PyPluginTrampoline`、`PluginAuditManager`，以及 `pluginTypes/` 下各类型的基类。它们把发现的插件变成应用可以调用的活动对象。

## 核心组件

| 组件 | 职责 |
|---|---|
| `PluginManager` | 顶层的**单例编排器**。拥有目录、加载器和云服务；提供 `initialize()`、`discover_plugins()`、安装/更新/删除以及 `shutdown()`。 |
| `PluginCatalog` | **仅基于清单的清册。** 扫描插件目录，把每个插件的元数据解析为 `PluginDescriptor`，并把结果分为有效和无效两类。不加载任何 Python。 |
| `CloudPluginService` | 对云代理的一层薄封装：获取已订阅/已拥有插件的清单、下载插件数据包、取消订阅/删除。 |
| `PluginLoader` | **加载/卸载的生命周期。** 安装依赖（使用捆绑的 `uv`）、导入模块、实例化包及其功能、标记它们的审计身份、运行 `on_load()`，并以 `PluginCapabilityIdentifier` 为键保存活动的功能实例。提供 `get_plugin_capabilities_by_type()` / `get_plugin_capability_by_name()`，以及加载/卸载和功能加载/卸载的回调。 |
| `PluginDescriptor` | 单个插件的规范记录：键、路径、功能类型/显示类型、版本、更新日志、依赖、云端覆盖信息，以及错误/有效性状态。 |
| `PythonInterpreter` | **内嵌 CPython 的单例 RAII 封装。** 负责初始化/终止、GIL 交接、`sys.path`、模块加载，以及安装审计钩子和 stderr 到日志的重定向。 |
| `PythonPluginBridge` | 定义内嵌的 **`orca` 模块**、`@orca.plugin` 装饰器、`orca.base` 包类和 `register_capability` 入口，并捕获、实例化包及其注册的功能类。 |
| `PyPluginTrampoline` | **C++ 到 Python 边界**上的 pybind11 覆盖基类：记录 Python 回溯，并为每次调用开启审计作用域。 |
| `pluginTypes/*` | 各类型的 C++ 功能基类和 trampoline（`SlicingPipelinePluginCapability`、`ScriptPluginCapability`、`PrinterAgentPluginCapability`），定义每种类型的入口方法和分派方式。 |
| `PluginAuditManager` | **单例 CPython 审计钩子**：对文件系统/网络/进程事件分类、提示用户，并按插件保存已授予的权限。参见审计文档。 |

## 插件打包与发现

插件是位于以下两个根目录之一中的一个文件夹，其中包含一个**入口文件**：

| 根目录 | 来源 |
|---|---|
| `data_dir()/orca_plugins/` | 本地安装 / 手动加载 |
| `data_dir()/orca_plugins/_subscribed/<user_id>/` | 云端订阅（按已登录用户区分） |

入口文件可以是单个 **`.py`** 文件（元数据写在 PEP 723 注释块中），也可以是 **`.whl`** wheel 包（元数据来自 wheel 的 `METADATA`）。插件注册的**功能**决定了哪些工作流程可以运行它；元数据中没有单独的 `type` 声明。元数据和打包的细节见[插件开发]({{L5}})。

**发现和加载是两个独立的阶段。** `PluginCatalog` *扫描*目录并生成 `PluginDescriptor`；它只解析清单，从不执行插件代码。*目录条目*只是数据；*已加载的插件*则是之后由 `PluginLoader` 创建的活动 Python 实例。用户登录后，云端清单会作为一层覆盖信息合并到目录中。

## 插件生命周期

{{C2}}

有几条加载时的不变条件值得了解：

- **`set_audit_plugin_key()` 才是启用强制检查的关键。** 没有它，实例的键为空，其调用不会经过审计。它在加载时标记，并在键迁移时重新标记（`update_loaded_plugin_key`）。参见审计文档。
- 一个模块必须且只能用 `@orca.plugin` 标记一个包类（`orca.base` 的子类），并且该类的 `register_capabilities()` 必须通过 `orca.register_capability(...)` 注册至少一项有效的功能，否则加载失败。每项功能都必须能解析出 `get_name()`，并且 `(type, name)` 在插件内必须唯一。
- **声明的权限在注册之后申请。** 如果 `register_capabilities()` 调用了 `orca.request_permissions(...)`，OrcaSlicer 会在该方法返回之后、实例化任何功能之前，显示一个合并的对话框。已经为该插件保存过的目标会被跳过；拒绝该对话框会中止加载。参见审计文档。

## 执行模型

功能是**按类型而不是按名称**访问的。不存在按类型实例化的注册表：功能的 Python 类继承一个有类型的 C++ 基类，包通过 `register_capability` 注册它，而每个工作流程的调用点用 `std::dynamic_pointer_cast<ConcreteType>` 把保存的功能实例（`PluginCapabilityInterface`）收窄到具体类型。转换成功，说明该功能存在并会被调用；转换失败（没有安装或启用该功能），这条路径就什么也不做。系统正是以此保证缺失或被禁用的功能绝不会改变现有行为。

| 功能类型 | 入口方法 | 调用者 |
|---|---|---|
| `slicing-pipeline` | `execute(ctx)` | 在配置的切片步骤由 `Print` 调用，在 G-code 导出期间的 `psGCodePostProcess` 由 `PostProcessor` 调用 |
| `script` | `execute()` | **插件对话框 -> 运行**操作 |
| `printer-connection` | 代理方法 | `NetworkAgentFactory`，通过在 `GUI_App` 中接好的加载器功能加载回调来注册 |
| `pages` | `get_ui()`、`on_message()` | `PluginPages`（`plugin/host/PluginPages.cpp`），它根据功能加载回调，为每项已启用的功能添加一个主窗口选项卡 |

与类型无关，每项已加载并启用的功能都会通过 `on_lifecycle_event(event, ctx)` 收到应用程序的**生命周期事件**。libslic3r 和 GUI 中的调用点用 `Slic3r::fire_lifecycle_event()`（`libslic3r/LifecycleEvents.hpp`）触发这些事件；`plugin_hooks` 安装分派器，分派器在触发事件的线程上同步转发给 `PluginManager::dispatch_lifecycle_event()`，一旦切片被取消就跳过其余功能，并记录、吞掉处理函数抛出的异常。关闭时，先卸载这个钩子，并等待正在进行的分派结束。参见[生命周期事件]({{L6}})。

加载/卸载**回调**（`PluginLoader::subscribe_on_load_callback` / `subscribe_on_unload_callback`）及其按功能的变体（`subscribe_on_capability_load_callback` / `subscribe_on_capability_unload_callback`），是各子系统对插件和功能的出现或消失做出响应的方式。例如，打印机代理层为每项 `PrinterConnection` 功能注册/注销一个代理，插件对话框则会刷新。添加新类型和接入调用点的方法见[插件开发]({{L7}})。

## 线程与 GIL

- **解释器在主线程上初始化。** CPython 通过 `PythonInterpreter`（单例）启动一次。在非主线程上初始化可能导致堆损坏，所以 `PluginManager::initialize()` 会立即同步完成初始化。
- **初始化后会释放 GIL**（`PyEval_SaveThread`），并在关闭时重新获取，这样其他线程就可以获取它。
- **插件加载在工作线程上运行**，由一个静态互斥锁串行化，避免模块导入相互竞争。发现过程也可以在后台线程上运行（`discover_plugins(async=true)`），不过启动时的发现是同步的。
- **在非主线程上每次接触 Python 都要获取 GIL**，通过 RAII 守卫 `PythonGILState`（`PyGILState_Ensure` / `Release`）实现——加载、执行以及实例析构（`on_unload` + `Py_DECREF`）都包裹在其中。

## 云端订阅

`CloudPluginService` 封装了云代理（`OrcaCloudServiceAgent`），并且需要登录才能使用。它获取已订阅/已拥有插件的清单，把它们作为覆盖信息合并到目录中，并把插件的数据包下载到临时文件（通过嗅探文件内容区分 `.whl` 和 `.py`）。`PluginManager` 设置加载器的云端用户 ID，`PluginLoader` 把下载的数据包安装到 `orca_plugins/_subscribed/<user_id>/` 下。注销登录会卸载云端插件。云端认证令牌（`orca_refresh_token.sec`）归云代理所有，而不属于插件层。

## 预设中的插件引用

当某个设置指向插件功能时（例如 `post_process_plugin`），该设置保存的值只是功能的**名称**。为了让引用在复制到可能没有安装该插件的另一台机器时依然有效，每个预设还带有一个 `plugins` 数组，记录它所用每项功能的**完整引用**。

每个条目是一个字符串，包含三个用 `;` 分隔的字段：

{{C3}}

{{C4}}

- 从 OrcaCloud 订阅的插件带有 **`cloud_uuid`**，仅限本地的插件则为**空**（注意相邻的 `;;`）。正是它让 OrcaSlicer 能够主动提出自动恢复缺失的插件。
- 由于 `;` 是字段分隔符，**功能名称中不能包含 `;`**（加载器会拒绝这样的插件），插件显示名称中的 `;` 都会被替换为 `_`（`sanitize_plugin_name`）。
- `plugins` 数组是内部清单（`coStrings`，`comDevelop` 模式），不是供用户编辑的字段。保存功能名称的字段标有 `support_plugin`；保存时，数组会被**修剪**为仍被这类字段使用的引用，所以过时的条目会被去掉。
- 解析/序列化位于 `Config.cpp`（`parse_capability_ref` -> `PluginCapabilityRef{ name, capability_name, uuid }`）；`plugins` 选项在 `PrintConfig.cpp` 中定义，并在**工艺、打印机和耗材丝**预设上跟踪。参见 `tests/libslic3r/test_config.cpp` 和 `tests/slic3rutils/test_plugin_capability_identifier.cpp`。

## 恢复缺失的插件

当你准备切片时，OrcaSlicer 会把当前工艺、打印机和耗材丝预设的 `plugins` 数组与已加载的目录进行比对（`Plater::refresh_missing_plugin_block`）。任何无法满足的引用都会以**无法关闭的通知**显示出来；只要还有未解决的引用，**切片按钮就一直被阻止**。没有"仍然切片"的途径；你必须解决引用（或修改引入它的设置）。引用分为四类：

- **缺失的 OrcaCloud 插件**（引用带有 UUID）——通知中的操作为**安装插件**，它会订阅、安装、加载并启用每个插件，使其立即可用。
- **缺失的本地插件**（没有 UUID）——无法自动获取；操作**在 OrcaCloud 上查找**只是在浏览器中打开 OrcaCloud 插件页面的搜索。它仅仅是一个建议：既不会关闭通知，也不会解除切片阻止。
- **未激活的插件**——包已在本地安装，但被引用的功能未处于活动状态（插件未加载，或功能被禁用）。操作**立即激活**会在本地加载/启用它，无需下载。
- **失效的引用**——插件已安装并加载，但不再提供被引用的功能（被重命名、删除或已过时）。激活无法解决这个问题，所以它只是提示信息，并提供**在 OrcaCloud 上查找**来寻找更新。

分类逻辑位于 `PluginResolver`（`get_missing_cloud_plugins`、`get_missing_local_plugins`、`get_inactive_plugins`、`get_broken_plugins`）；通知和切片阻止由 `Plater.cpp`（`refresh_missing_plugin_block`）驱动。

## 插件对话框

插件对话框（`PluginsDialog.cpp` + `resources/web/dialog/PluginsDialog/`）把每个已安装的插件显示为可展开的一行（激活 · 名称 · 版本 · 状态）。展开插件会显示**功能树**：每项已注册的功能一行，带有自己的启用复选框、类型标签，以及（对于可运行的脚本功能）一个**运行**按钮。详细信息窗格分为几个选项卡：

| 选项卡 | 显示内容 |
|---|---|
| **插件信息** | 缩略图、来源、类型、作者、版本（带有更新标记） |
| **描述** | 插件自己的描述，取自其 Python/wheel 元数据 |
| **配置** | 所选插件功能的 JSON 配置或自定义配置 |
| **更新日志** | 版本 / 日期 / 更改内容表格 |
| **诊断** | 加载状态和错误状态 |

安装通过分体式下拉按钮**浏览插件**进行，它打开 OrcaCloud 插件中心；其中还有**安装本地插件**选项，用于直接手动加载 `.py` 或 `.whl`。每个插件和每项功能的启用状态保存在每个插件各自的 `.install_state.json` 附属文件中（由 `PluginManager` 写入）。

状态列由 `resolve_plugin_status()`（`GUI/PluginStatus.hpp`）得出：加载进行中时为**载入中**；插件有错误且未加载（加载时失败）时为**错误**；有错误但仍已加载时为 **RuntimeError**（例如加载后某项功能被拒绝，比如某个打印机代理的 ID 已被其他功能或内置代理注册）；已加载时为**已激活**；其他情况为**未激活**。激活复选框跟随插件是否已加载，所以处于 RuntimeError 状态的插件仍保持勾选，而禁用插件会清除它的错误。

不再订阅或 OrcaCloud 不再返回的云端插件，会在下一次云端刷新时被标记为**孤立**：它的本地包仍然保持安装并可以使用，但无法再从云端重新安装或更新，只提供**删除**和**在文件夹中显示**。如果刷新时发现某些已安装插件的文件已从磁盘上消失，对话框会提供移除它们的选项（`get_missing_plugin_descriptors` / `remove_missing_plugins`）。

每次成功安装（本地安装、重新安装或云端更新）都会撤销之前授予该插件键的权限，所以新代码必须重新请求；参见[插件审计钩子]({{L8}})。

## 安全性与可观测性

- **安全性**——所有 C++ 到 Python 的调用都会经过一个 trampoline，它为每次调用开启审计上下文；随后 `PluginAuditManager` 审计钩子对敏感的文件系统、网络、启动进程和创建线程事件进行分类，用一个写明目标的"是/否"对话框提示用户，并按插件保存大多数类别的授权。插件可以用 `orca.request_permissions(...)` 声明它预期的目标，这会在加载期间产生一个合并的提示。这是一套权限系统，而不是加固的沙箱；究竟哪些会被强制检查、哪些不会，请阅读[插件审计钩子]({{L9}})（创建线程会被把关，但新线程中执行的工作不会）。
- **可观测性**——Python 的 `sys.stderr`（插件回溯，包括插件创建的线程中的回溯）会同时写入 `data_dir()/log/python_*.log`；C++ 端的加载/发现消息写入主会话日志。错误在界面中如何呈现（消息框还是插件详细信息区域）见[插件开发]({{L10}})。

## 相关文档

- [插件开发]({{L11}})——编写 Python 插件；添加新的 C++ 插件类型；测试与调试。
- [API 参考]({{L12}})——内嵌的 `orca` 模块、注册、宿主访问、UI 辅助工具，以及各个功能模块。
- [插件审计钩子]({{L13}})——审计钩子：类别、提示、持久化，以及扩展策略。

## 关键文件

| 文件 | 作用 |
|---|---|
| `src/slic3r/plugin/PluginManager.{hpp,cpp}` | 顶层编排器；启动时的 `initialize()` / `discover_plugins()` / `shutdown()` |
| `src/slic3r/plugin/PluginCatalog.{hpp,cpp}` | 目录扫描 -> `PluginDescriptor` 清册 |
| `src/slic3r/plugin/PluginLoader.{hpp,cpp}` | 多线程加载/卸载、依赖安装、功能注册表、审计键标记 |
| `src/slic3r/plugin/PluginDescriptor.hpp` | 每个插件的记录（类型、更新日志、`sanitize_plugin_name`） |
| `src/slic3r/plugin/CloudPluginService.{hpp,cpp}` | 云端获取 / 下载 / 订阅 / 取消订阅 |
| `src/slic3r/plugin/PythonInterpreter.{hpp,cpp}` | 内嵌 CPython、GIL 交接、审计钩子和日志的安装 |
| `src/slic3r/plugin/PythonPluginBridge.{hpp,cpp}` | `orca` 模块，`@orca.plugin` / `register_capability` / `request_permissions`，包和功能的捕获 |
| `src/slic3r/plugin/PluginFsUtils.hpp` | `PluginPermissions` / `PluginInstallState`：`.install_state.json` 附属文件及其权限分组 |
| `src/slic3r/plugin/PyPluginPackage.hpp` | 包基类（`orca.base`）+ `register_capabilities` |
| `src/slic3r/plugin/PyPluginTrampoline.hpp` | C++ 到 Python 边界的宏（回溯日志 + 审计作用域） |
| `src/slic3r/plugin/pluginTypes/*` | 各类型的功能基类 + trampoline |
| `src/slic3r/plugin/PluginAuditManager.{hpp,cpp}` | CPython 审计钩子及其策略 |
| `src/libslic3r/Config.cpp` | `parse_capability_ref`，`plugins` 数组的序列化/反序列化 |
| `src/libslic3r/PrintConfig.cpp` | `plugins` / `post_process_plugin` 选项的定义 |
| `src/slic3r/GUI/PostProcessor.cpp` | 解析预设中的插件引用，并运行 `psGCodePostProcess` 切片流水线步骤 |
| `src/slic3r/GUI/PluginPickerDialog.{hpp,cpp}` | 选择一项功能作为设置值 |
| `src/slic3r/GUI/Plater.cpp` | 切片时（`reslice`）的缺失插件解决对话框 |
| `src/slic3r/GUI/GUI_App.cpp` | 启动时的接线（初始化、发现、加载/功能加载回调）以及关闭 |
| `src/slic3r/GUI/PluginsDialog.cpp` | 插件对话框（功能树、选项卡、运行、浏览插件） |
| `src/slic3r/plugin/PluginConfig.{hpp,cpp}` | 全局功能配置、预设覆盖，以及 JSON/自定义 UI 响应 |
