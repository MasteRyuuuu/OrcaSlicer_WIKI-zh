# 宿主

`orca.host`（在 `src/slic3r/plugin/host/` 中绑定）让插件可以**只读**访问正在运行的切片软件。它面向分析、报告和导出类插件；这里没有任何东西会修改模型。唯一会改变状态的例外是[本地配置包重新加载]({{L1}})，它从磁盘重新读取用户的本地预设包并刷新预设界面——它本身并不编辑或创建预设。

**脚本插件在主线程/UI 线程上运行**，所以在一次 `execute()` 期间模型不会在你手下发生变化。**切片流水线插件在后台线程上运行**，同时 GUI 继续运行；打印机代理的方法可能在 UI 线程上调用，也可能在任务线程上调用。无论哪种情况，都要把一切当作瞬时快照，不要跨运行保存引用。

## 入口点

如果在 GUI/模型就绪之前调用，每个入口点都会抛出 `RuntimeError`：

{{C1}}

`app_language()` 返回 OrcaSlicer 界面当前使用的语言，以便插件对自己的对话框进行本地化。请使用它，而不要去读取应用程序配置文件——审计钩子会阻止这种读取。

`plugin.storage()` 返回为调用它的插件保留的文件夹（必要时会创建），插件可以在其中跨运行、跨更新保存数据。本地插件的文件夹是 `orca_plugins/plugin_data/<plugin_key>`；云端插件的文件夹按登录用户区分（`orca_plugins/plugin_data/_subscribed/<user_id>/<plugin_key>`），所以在没有用户登录时会抛出 `RuntimeError`。它必须在插件回调（`execute()`、`on_load()`、消息处理函数……）中调用，而不能在导入时调用。

`plater()` 返回的 `Plater` 还提供 `model()`、`is_project_dirty()`、`is_presets_dirty()` 和 `inside_snapshot_capture()`。

## 模型图

`Model.objects()` 返回 `ModelObject` 值。每个对象有 `volumes()` / `volume(i)`（返回 `ModelVolume`）和 `instances()` / `instance(i)`（返回 `ModelInstance`）。包围盒是值类型 `host.BoundingBox`（`min` / `max` / `size` / `center` 为以 mm 为单位的 `(x, y, z)` 元组，另有 `radius` / `defined`）。

## 预设

`orca.host.preset_bundle()` 返回实时的 `PresetBundle`：GUI 正在编辑的各个预设集合，以及已选择和已编辑的预设。所有这些都是已加载预设的只读视图。

### 集合

`PresetBundle` 提供五个 `PresetCollection` 属性：

| 属性 | `PresetType` | 预设 |
|---|---|---|
| `bundle.prints` | `Print` | FDM 打印（工艺）预设 |
| `bundle.printers` | `Printer` | 打印机预设 |
| `bundle.filaments` | `Filament` | FDM 耗材丝预设 |
| `bundle.sla_prints` | `SlaPrint` | SLA 打印预设 |
| `bundle.sla_materials` | `SlaMaterial` | SLA 材料（树脂）预设 |

`PresetCollection` 提供对其中预设的只读访问：

| 调用 | 返回值 | 说明 |
|---|---|---|
| `size()` | `int` | 集合中预设的数量 |
| `selected_preset()` | `Preset` | 别名 `get_selected_preset()` |
| `selected_preset_name()` | `str` | 别名 `get_selected_preset_name()` |
| `edited_preset()` | `Preset` | 别名 `get_edited_preset()`；带有未保存修改的已选预设 |
| `preset(index)` | `Preset` | 按索引获取；超出范围时抛出 `IndexError` |
| `find_preset(name)` | `Preset` 或 `None` | 没有该名称的预设时为 `None` |
| `preset_names()` | `list[str]` | 集合中所有预设的名称 |

### Preset

`Preset` 提供只读的元数据及其自身的配置：

| 成员 | 返回值 | 说明 |
|---|---|---|
| `type` | `PresetType` | 预设的种类 |
| `name`、`alias`、`file`、`bundle_id` | `str` | `alias` / `file` 可能为空 |
| `is_default`、`is_external`、`is_system`、`is_visible`、`is_dirty`、`is_compatible`、`is_project_embedded` | `bool` | 只读标志 |
| `is_user()` | `bool` | 预设位于用户的预设文件夹中 |
| `is_from_bundle()` | `bool` | 预设来自某个配置包，而不是由用户创建 |
| `label(no_alias=False)` | `str` | 显示名称；`no_alias=True` 返回原始名称 |
| `config_keys()` | `list[str]` | 在该预设自身配置中设置了的键 |
| `config_value(key)` | 值或 `None` | 该预设中 `key` 的值；未设置时为 `None` |

### 当前预设和完整配置

| 调用 | 返回值 | 说明 |
|---|---|---|
| `current_process_preset()` | `Preset` | 正在编辑的**打印**预设 |
| `current_print_preset()` | `Preset` | 与 `current_process_preset()` 相同的正在编辑的打印预设 |
| `current_printer_preset()` | `Preset` | 正在编辑的打印机预设 |
| `current_filament_preset_names()` | `list[str]` | 当前所选耗材丝的名称 |
| `current_filament_presets()` | `list[Preset or None]` | 所选的耗材丝预设；名称无法解析时对应项为 `None` |
| `full_config_keys()` | `list[str]` | 配置包完整（展平后）配置中的键 |
| `full_config_value(key)` | 值或 `None` | 完整配置中 `key` 的值 |

`current_process_preset()` 和 `current_print_preset()` 是同一个正在编辑的打印预设的两个名称，`current_printer_preset()` 是正在编辑的打印机预设。没有单独的"当前耗材丝"调用：多挤出机配置可以选择多种耗材丝，所以请遍历 `current_filament_presets()`（或其名称）。`config_value()` 读取的是预设自身设置的键值，而 `full_config_value()` 读取的是在整个配置包范围内解析后的值。

### PresetType

`orca.host.PresetType` 标识预设的种类：`Invalid`、`Print`、`SlaPrint`、`Filament`、`SlaMaterial`、`Printer`、`PhysicalPrinter`、`Plate` 和 `Model`。只有 `Print`、`Printer`、`Filament`、`SlaPrint` 和 `SlaMaterial` 在上面有对应的 `PresetCollection` 属性。

### 本地配置包重新加载

`orca.host.preset.bundles` 是 `orca.host` 中唯一**会改变状态**的部分：它从磁盘重新读取用户的本地预设包，并刷新预设界面。它不会编辑、创建、导入或导出预设——插件 API 不提供这类调用。

{{C2}}

| 调用 | 效果 |
|---|---|
| `list_ids()` | 当前用户 `_local` 目录中 `reload_local()` 可以接受的本地配置包 ID，包括启动后才添加的配置包 |
| `reload_local(bundle_id)` | 从当前用户的 `_local` 目录重新读取该配置包，并刷新预设界面（侧边预设列表、选项卡配置、预设下拉框） |

两者都只作用于本地配置包，并会调度到 UI 线程执行，所以可以安全地从后台线程插件中调用。如果应用正在关闭，或者预设包或主窗口不可用，两者都会抛出 `RuntimeError`；配置包无法重新加载时（ID 未知或解析错误），`reload_local()` 也会抛出该异常。

> [!NOTE]
> 请用 `list_ids()` 重新获取列表，而不要缓存它：它包括启动后才添加的配置包。

## 网格几何

`ModelVolume.mesh()` 返回 `host.TriangleMesh`。

| 成员 | 返回值 | 说明 |
|---|---|---|
| `vertex_count()` / `triangle_count()`（`facets_count()`）/ `is_empty()` | `int` / `bool` | 不需要 numpy |
| `vertex(i)` / `triangle(i)` | `(x, y, z)` / `(a, b, c)` 元组 | 不需要 numpy，带边界检查 |
| `vertices()` | `(N, 3)` float32 ndarray | **只读、零拷贝**，需要 numpy |
| `triangles()` | `(M, 3)` int32 ndarray | 顶点索引；**只读、零拷贝**，需要 numpy |
| `face_normals()` | `(M, 3)` float32 ndarray | 计算得到的副本，需要 numpy |
| `volume()` / `bounding_box()` / `is_manifold()` | `float` / `BoundingBox` / `bool` | 不需要 numpy |

坐标是**局部**坐标（该体积自身的坐标系，单位为 mm）。`vertices()` / `triangles()` 数组是实时网格的零拷贝视图，并被标记为只读；向其写入会抛出 `ValueError`。它们的生命周期绑定在一个不可变的网格快照上，所以即使该体积的网格之后被替换，它们依然有效。

## 完整示例

在 PEP 723 块中声明 numpy，让捆绑的 `uv` 安装它：

{{C3}}

> [!NOTE]
> 如果实例是镜像的（`instance.is_left_handed()` 为 `True`，即 `det(M) < 0`），在世界空间中计算朝外的法线时，要翻转三角面的绕序 / 对面法线取反。

## numpy 要求

`vertices()`、`triangles()`、`face_normals()` 以及 `ModelVolume` / `ModelInstance` 上的 `matrix()` 访问器需要 numpy，如果没有安装会抛出明确的 `ImportError`（请声明 `dependencies = ["numpy"]`）。其他一切——计数、`vertex(i)` / `triangle(i)`、`volume()`、`bounding_box()`、`is_manifold()`，以及 `offset` / `rotation` / `scaling_factor` / `mirror` 元组访问器——都不需要 numpy。
