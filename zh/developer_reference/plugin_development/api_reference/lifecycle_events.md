# 生命周期事件

任何功能都可以通过重写 `on_lifecycle_event()` 来观察应用程序的生命周期时刻（项目打开/保存、切片、盘和对象的编辑、预设更改、打印机和任务活动）。它定义在根基类 `orca.PythonPluginBase` 上，所以每种功能类型都可以使用，默认什么也不做。

事件数据有意设计得小而通用：它只标识*发生了什么*，而不包含完整的状态。要了解更多，请在处理函数中调用针对性的 API，例如在 `ObjectAdded` 事件之后调用 `orca.host.plater().model()`（参见[宿主]({{L1}})）。

{{C1}}

## 事件

`orca.LifecycleEvent` 的取值（也在模块层级导出，例如 `orca.SliceStarted`）：

| 分组 | 事件 |
|---|---|
| 项目（3MF） | `NewProject`、`ProjectOpened`、`ProjectBeforeSave`、`ProjectAfterSave`、`ProjectClosed`、`ProjectDirtyChanged` |
| 切片 | `SliceStarted`、`SliceGeometryFinished`、`GCodeExportStarted`、`GCodeExportFinished`、`SlicingJobComplete` |
| 盘 / 模型编辑 | `ObjectAdded`、`ObjectDeleted`、`ObjectTransformed`、`ObjectChanged`、`ObjectRenamed`、`PlateCreated`、`PlateDeleted`、`PlateSelected`、`PlateRenamed` |
| 预设 | `PresetSelected`、`PresetSaved` |
| 打印机 / 设备 | `PrintStateChanged`、`DeviceOnline`、`DeviceOffline`、`DeviceDiscovered`、`DeviceSelected`、`UploadStarted`、`UploadFinished` |
| 打印 / 发送任务 | `PrintJobStarted`、`PrintJobFinished`、`SendJobStarted`、`SendJobFinished` |

## 事件数据

`ctx` 是一个带有只读字段的 `orca.LifecycleEventContext`。事件没有用到的字段保持默认值（空字符串、`index = -1`、`dirty = False`）。

| 字段 | 含义 |
|---|---|
| `name` | 主要对象：项目/输出路径、模型、对象、盘或预设名称、设备 ID、上传的文件名。可能为空 |
| `code` | `orca.LifecycleEvtCode`：`Ok`、`Error` 或 `Warn`。对于开始事件和状态变化事件，`Ok` 只表示事件发生了 |
| `msg` | 可选的、供人阅读的详细信息；不保证可以稳定地解析 |
| `id` | 稳定的对象/模型标识符（如果来源有的话） |
| `previous_name` | 旧名称，用于重命名事件 |
| `device_id` | 设备，用于打印/发送任务事件 |
| `job_id` | 任务标识符（如果发起任务的队列提供的话） |
| `source` | 发起事件的子系统或操作，适合用来过滤 |
| `index` | 盘、对象或体积的索引（如果来源使用索引的话） |
| `dirty` | 项目整体的未保存状态，用于 `ProjectDirtyChanged` |

当前各来源填写的内容：

| 事件 | 事件数据 |
|---|---|
| `NewProject` | 没有主要对象；只有 `code` |
| `ProjectOpened`、`ProjectBeforeSave`、`ProjectAfterSave`、`ProjectClosed` | `name` = 项目文件 / 项目名称 |
| `ProjectDirtyChanged` | `dirty`、`source` |
| `SliceStarted`、`SliceGeometryFinished` | `id` = 模型 ID，`name` = 模型名称 |
| `GCodeExportStarted`、`GCodeExportFinished` | `id`、`name`，`msg` = 输出路径；失败时 `code = Error`，`msg` 中还会带有错误信息 |
| `SlicingJobComplete` | `id`、`name`；取消时 `code` 为 `Warn` 且 `msg = "cancelled"`，失败时为 `Error` 并带有错误文本 |
| `ObjectAdded`、`ObjectDeleted` | `name` = 对象名称 |
| `ObjectTransformed` | `msg` = `moved`、`rotated`、`scaled`、`arranged` 或 `auto_oriented`；交互式移动/旋转/缩放时带有 `name` |
| `ObjectChanged` | `name`、`id`、`source = "geometry"`（已知时还有 `index`） |
| `ObjectRenamed` | `name`、`previous_name`、`id`、`index`，`source` = `object` 或 `volume` |
| `PlateCreated`、`PlateDeleted`、`PlateSelected` | `name` = 盘名称，`index` = 盘索引 |
| `PlateRenamed` | `name`、`previous_name`、`index` |
| `PresetSelected` | `name` = 预设，`msg` = 预设类型（`print`、`filament`、`printer`……） |
| `PresetSaved` | `name` = 预设，`msg` = `new` 或 `overwrite` |
| `PrintStateChanged` | `name` = 设备 ID，`msg` = 新的打印状态 |
| `DeviceOnline`、`DeviceOffline`、`DeviceDiscovered`、`DeviceSelected` | `name` = 设备 ID |
| `UploadStarted`、`UploadFinished` | `name` = 上传的文件名；失败时 `code = Error`，`msg` = 错误信息 |
| `PrintJobStarted`、`PrintJobFinished`、`SendJobStarted`、`SendJobFinished` | `name` = 项目名称、`device_id`、`source`（`print_job`、`send_job` 或 `task_manager`），任务管理器的任务还有 `job_id`；结束的任务会报告 `Warn`/`cancelled` 或 `Error` |

请把这张表当作参考，而不是约定：以 `event` 和 `code` 为准，把缺失的字段视为"未提供"。

## 投递规则

- 每个插件中每项**已加载并启用**的功能都会收到每一个事件，与功能类型无关。被禁用的功能会被跳过。
- 事件**在触发它的线程上同步投递**：编辑、项目和预设事件通常在 UI 线程上，切片和 G-code 导出事件在切片工作线程上，任务和上传事件在任务/上传工作线程上。不要假设一定是 UI 线程，处理函数要简短，绝不能阻塞：切片软件会等待你的处理函数返回。同一个打印任务的 `PrintJobStarted` 和 `PrintJobFinished` 会在同一个工作线程上到达。
- 一旦切片被取消，该次切片的切片和 G-code 导出事件会在调用下一个功能之前停止分派。
- 处理函数抛出的异常会被记录到日志（连同事件和事件数据）并被吞掉；它不会影响 OrcaSlicer 或其他插件。
- 与其他任何插件调用一样，处理函数在审计上下文中运行，所以文件系统、网络和进程访问会提示用户。参见[插件审计钩子]({{L2}})。
- 插件关闭时，OrcaSlicer 停止接受新事件，并等待已经在运行的处理函数结束后，再卸载插件代码。

关于每项功能都会继承的其他成员，请参见[注册]({{L3}})。
