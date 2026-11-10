# 脚本

`orca.script` 模块为从插件对话框运行的插件提供 `ScriptPluginCapabilityBase`。

| 基类 | `get_type()` 返回 | 必需的方法 | 调用者 |
|---|---|---|---|
| `orca.script.ScriptPluginCapabilityBase` | `Script` | `get_name()`、`execute(self) -> ExecutionResult` | **插件对话框 -> 运行**操作 |

生命周期钩子 `on_load()` / `on_unload()` 是可选的，每项功能都可以使用（默认什么也不做）。`on_lifecycle_event(event, ctx)` 也是如此，它用于观察项目保存或切片等应用程序事件；参见[生命周期事件]({{L1}})。

> [!IMPORTANT]
> `ScriptPluginCapabilityBase.execute()` 在**主线程/UI 线程**上运行：在整个调用期间都可以安全地读取实时的宿主句柄，`orca.host.ui` 对话框也会内联打开，但运行缓慢的 `execute()` 会**冻结界面**。请保持简短；把繁重的工作交给你自己的 `threading.Thread`（它不能接触模型），并通过 `create_window` 面板呈现结果。

## 最小结构

{{C1}}

关于 `ExecutionResult`、包的注册以及功能名称的规则，请参见[注册]({{L2}})。
