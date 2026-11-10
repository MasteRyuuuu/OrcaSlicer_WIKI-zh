# 注册

内嵌的插件 API 通过一个名为 `orca` 的 Python 模块提供（`PythonPluginBridge.cpp` 中的 `PYBIND11_EMBEDDED_MODULE(orca, ...)`）。它提供功能基类、包基类、结果类型和功能注册。

| 符号 | 种类 | 成员 / 用途 |
|---|---|---|
| `orca.PluginType` | 枚举 | `PrinterConnection`、`Pages`、`Analysis`、`Importer`、`Exporter`、`Visualization`、`Script`、`SlicingPipeline`、`ResourceTexture`、`Unknown` |
| `orca.PluginResult` | 枚举 | `Success`、`Skipped`、`RecoverableError`、`FatalError` |
| `orca.PluginContext` | 类 | 基础上下文，字段 `orca_version: str` |
| `orca.ExecutionResult` | 类 | 字段 `status`、`message`、`data`；工厂方法见下文 |
| `orca.LifecycleEvent` | 枚举 | [生命周期事件]({{L1}})：传给 `on_lifecycle_event` 的应用程序时刻 |
| `orca.LifecycleEvtCode` | 枚举 | `Ok`、`Error`、`Warn`——生命周期事件携带的结果 |
| `orca.LifecycleEventContext` | 类 | 生命周期事件的只读数据 |
| `orca.PythonPluginBase` | 类 | 根**功能**基类；子类必须实现 `get_name()` |
| `orca.base` | 类 | **包**基类；继承它并重写 `register_capabilities()` |
| `orca.plugin` | 装饰器 | 标记文件中唯一的包类（每个文件恰好一个） |
| `orca.register_capability(cls)` | 函数 | 注册一个功能类；在 `register_capabilities()` 内部调用 |
| `orca.request_permissions(...)` | 函数 | 预先声明文件系统、网络、进程和线程权限；在 `register_capabilities()` 内部调用（参见[权限]({{L2}})） |
| `orca.slicing` | 子模块 | [切片流水线]({{L3}})：`Step`、`SlicingPipelineContext`、`SlicingPipelineCapabilityBase` |
| `orca.script` | 子模块 | [脚本]({{L4}})：`ScriptPluginCapabilityBase` |
| `orca.pages` | 子模块 | [页面]({{L5}})：`PagesPluginCapabilityBase`，主窗口中的插件选项卡 |
| `orca.resource_texture` | 子模块 | [资源纹理]({{L6}})：`ResourceTexturePluginCapabilityBase` |
| `orca.printer_agent` | 子模块 | [打印机代理]({{L7}})：`PrinterAgentBase` 及其数据类型 |
| `orca.host` | 子模块 | [宿主]({{L8}})：只读访问实时模型、预设和网格几何 |
| `orca.host.ui` | 子模块 | [宿主 UI]({{L9}})：对话框、进度对话框、交互窗口、停靠面板和通知 |

每项功能都从 `orca.PythonPluginBase` 继承可选的钩子 `on_load()`、`on_unload()` 和 `on_lifecycle_event(event, ctx)`（参见[生命周期事件]({{L10}})），以及以下配置方法：

| 方法 | 用途 |
|---|---|
| `has_config_ui()` | 选择自定义 HTML 编辑器，而不是宿主的 JSON 编辑器。 |
| `get_config_ui()` | 返回自定义 HTML 编辑器页面。 |
| `get_default_config()` | 返回**恢复默认**时使用的 Python dict；从 Python 调用时返回其 JSON 字符串。 |
| `get_config()` | 以 JSON 字符串返回实际生效的配置。 |
| `get_config_version()` | 返回最后一次保存该配置的版本。 |
| `save_config(config)` | 为该功能持久保存一个 JSON 字符串；JSON 无效或写入失败时返回 `False`。 |

在这一边界上请使用 `json.loads()` 和 `json.dumps()`。关于存储层次和自定义界面的消息传递，请参见[功能配置]({{L11}})。

## 执行结果

`ExecutionResult` 是插件报告运行结果的方式：

{{C1}}

- `status`——一个 `orca.PluginResult`。
- `message`——供人阅读的文本；错误/结果对话框中显示的就是它。
- `data`——一个自由格式的字符串，其含义由插件/工作流程定义（框架不解释它）。

## 注册

注册分为两部分，都在**模块导入/加载时**完成。

**功能**——每项功能都是一个类，继承某个有类型的基类，并实现 `get_name(self) -> str`。名称决定了功能在界面中如何显示、预设如何引用它，因此它必须**在插件内唯一**，并且**不能包含 `;`**。这个字符被保留为预设引用中的分隔符，功能名称中出现 `;` 会导致加载失败。

**包**——每个文件中恰好有一个类用 `@orca.plugin` 装饰并继承 `orca.base`。它的 `register_capabilities(self)` 方法为你想提供的每个功能类各调用一次 `orca.register_capability(Cls)`：

{{C2}}

OrcaSlicer 实例化包类（必须能以 `SamplePlugin()` 的形式无参数调用），调用 `register_capabilities()`，然后实例化每项已注册的功能。

插件加载时强制执行的规则（大部分位于 `PythonPluginBridge.cpp`）：

- `@orca.plugin` 类**必须**继承 `orca.base`，并且每个文件中**恰好只能有一个**。出现第二个 `@orca.plugin` 会导致加载失败。
- 传给 `orca.register_capability` 的每个类都必须继承某个功能基类（最终都继承自 `orca.PythonPluginBase`）；否则会抛出 `value_error`。
- 每项功能都必须能解析出 `get_name()`（在桥接层检查）；如果得到的 `(type, name)` 组合在插件内不唯一，加载器（`PluginLoader.cpp`）还会拒绝该插件。
- 从未传给 `orca.register_capability` 的功能类对 OrcaSlicer 来说是**不可见的**，即使它在文件中有定义。
- 如果插件调用了 `orca.request_permissions(...)`，用户必须接受注册之后出现的合并对话框；拒绝会导致加载失败。

## 权限

`orca.request_permissions(...)` 在 `register_capabilities()` 中声明插件预期需要的文件系统、网络、进程和线程访问。所有参数都是可选的：

{{C3}}

- 每个列表接受相应审计事件所报告的目标字符串：文件系统类别为路径，`network_http` 为 URL，`network_socket` 为地址字符串（例如 `"('example.com', 443)"`），`process` 为命令。
- `threading=True` 申请创建一个线程的权限；创建线程的权限按插件授予一次，新线程自身的工作不会受到审计。
- OrcaSlicer 在 `register_capabilities()` 运行期间收集这些声明，并在它返回之后、创建任何功能实例之前，显示**一个合并的"是/否"对话框**。已经授予该插件的目标会被跳过，所以再次声明它们不会产生提示。
- 拒绝该对话框会中止插件加载。任何列表中出现空字符串，或者在插件发现过程之外调用该函数，都会抛出 `ValueError`。
- 声明只会预先批准所列出的确切目标字符串；其他任何访问在首次使用时仍会提示。关于审计类别、持久化以及非主线程上的提示行为，请参见[插件审计钩子]({{L12}})。

## 功能名称和类型

`get_name()` 是必需的；`get_type()` 通常不是。每项功能都必须实现 `get_name()`。它在根基类上是纯虚函数，缺少重写会导致加载失败。有类型的 C++ 基类已经实现了 `get_type()`（例如 `ScriptPluginCapability::get_type()` 返回 `Script`），所以继承*有类型*基类的子类不需要重写它。只有直接继承**根**基类 `orca.PythonPluginBase` 的功能，才必须自己设置 `get_type()`。
