# 命令行其他选项

用于加载设置/耗材丝、选择对象、输出位置、日志和 3MF 元数据的选项。通用的标志语法请参见[命令行模式]({{L1}})。

{{T1}}

## 加载设置和耗材丝

这些选项加载的是各设置选项卡的"保存/导出"操作所生成的同一类单选项卡 JSON 文件——这些文件在图形界面中如何创建，请参见[导出预设包]({{L2}})。

| 标志 | 输入 | 说明 | 备注 |
| --- | --- | --- | --- |
| `--load-settings` | `"setting1.json;setting2.json"` | 从给定的文件（用分号分隔）加载工艺/机器设置。 | |
| `--load-filaments` | `"filament1.json;filament2.json;..."` | 从给定的文件（用分号分隔）加载耗材丝设置。 | |
| `--uptodate-settings` | `"setting1.json;setting2.json"` | 与 [`--uptodate`]({{L3}}) 一起使用时要加载的工艺/机器设置。 | |
| `--uptodate-filaments` | `"filament1.json;filament2.json;..."` | 与 [`--uptodate`]({{L4}}) 一起使用时要加载的耗材丝设置。 | |
| `--downward-check` | 布尔值 | 检查当前机器是否与 `--downward-settings` 中列出的机器向下兼容。 | |
| `--downward-settings` | `"machine1.json;machine2.json;..."` | 启用 `--downward-check` 时用于检查的机器设置列表。 | |
| `--load-custom-gcodes` | `custom_gcode_toolchange.json` | 从 JSON 文件加载自定义换工具头 G-code 定义。相关概念：[机器 G-code]({{L5}})。 | |

## 对象选择

| 标志 | 输入 | 说明 | 备注 |
| --- | --- | --- | --- |
| `--skip-objects` | `"3,5,10,77"` | 打印时跳过给定索引的对象。 | |
| `--clone-objects` | `"1,3,1,10"` | 加载列表中每个对象的克隆数量。 | 不能与 [`--assemble`]({{L6}}) 同时使用。 |
| `--load-assemble-list` | `assemble_list.json` | 从配置文件加载完整的装配对象列表（盘、对象及其参数），而不是直接加载模型。 | 不能与位置参数形式的输入模型文件或任何[变换]({{L7}})标志同时使用。 |
| `--load-filament-ids` | `"1,2,3,1"` | 为每个加载的对象分配的耗材丝 ID，每个输入文件一项。 | 列表长度必须与输入文件数量一致。 |

## 输出和日志

| 标志 | 输入 | 说明 | 备注 |
| --- | --- | --- | --- |
| `--datadir` | `dir` | 在给定目录中加载和存储设置，而不是使用默认的用户配置位置。便于维护多套独立的配置。相关概念：[便携式用户配置]({{L8}})。 | |
| `--outputdir` | `dir` | 导出文件的输出目录。 | 如果目录不存在会递归创建；创建失败时进程报错退出。 |
| `--export-statistics` | 布尔值 | 把每个已切片盘的统计信息写成 JSON，即输出目录中 G-code 旁边的 `plate_N.statistics.json`，以及 [`--export-3mf`]({{L9}}) 生成的 3MF 内部的同名文件：打印时间、耗材丝和走线类型的总计，以及按层、按对象的相同统计。 | 与[导出统计信息]({{L10}})偏好设置生成的文件相同。 |
| `--debug` | `level`（整数，0-5） | 调试日志级别：`0` fatal，`1` error，`2` warning，`3` info，`4` debug，`5` trace。 | 默认：`1`。 |
| `--logfile` | `file` | 把调试日志重定向到文件，而不是标准错误输出。 | |

## 摆放行为

这些选项对应图形界面中[自动摆放]({{L11}})面板里的选项。

| 标志 | 输入 | 说明 | 备注 |
| --- | --- | --- | --- |
| `--allow-multicolor-oneplate` | 布尔值 | 允许把多种材料/颜色摆放到同一个盘上。参见[自动摆放]({{L12}})中的"允许同一盘中包含多种材料"。 | 默认：开启。 |
| `--allow-rotations` | 布尔值 | 允许摆放时旋转对象以便放下。参见[自动摆放]({{L13}})中的"自动旋转以优化自动摆放效果"。 | 默认：开启。 |
| `--align-to-y-axis` | 布尔值 | 摆放之前把每个对象转到长边沿 Y 轴方向。参见[自动摆放]({{L14}})中的"对齐到 Y 轴"。 | 默认：i3 类打印机开启，其他打印机关闭。 |
| `--avoid-extrusion-cali-region` | 布尔值 | 摆放时避开盘上的挤出校准区域。 | 默认：关闭。 |

## 元数据

| 标志 | 输入 | 说明 | 备注 |
| --- | --- | --- | --- |
| `--makerlab-name` | `name` | 生成 3MF 时嵌入的 MakerLab 名称。 | |
| `--makerlab-version` | `version` | 生成 3MF 时嵌入的 MakerLab 版本。 | |
| `--metadata-name` | `"name1;name2;..."` | 要添加到 3MF 的自定义元数据字段名，用分号分隔。 | 按位置与 `--metadata-value` 配对。 |
| `--metadata-value` | `"value1;value2;..."` | 要添加到 3MF 的自定义元数据字段值，用分号分隔。 | 按位置与 `--metadata-name` 配对。 |

## 打印行为

| 标志 | 输入 | 说明 | 备注 |
| --- | --- | --- | --- |
| `--enable-timelapse` | 布尔值 | 把本次切片视为使用延时摄影。参见[延时摄影]({{L15}})。 | 默认：关闭。 |
| `--skip-modified-gcodes` | 布尔值 | 跳过加载的 3MF 中嵌入的（来自打印机/耗材丝预设的）修改过的 G-code。 | 默认：关闭。 |
| `--allow-newer-file` | 布尔值 | 允许切片由比当前运行版本更新的 OrcaSlicer 保存的 3MF。 | 默认：关闭。 |
| `--allow-mix-temp` | 布尔值 | 允许高温和低温需求不同的耗材丝一起打印。 | 内部使用；默认：关闭。 |
