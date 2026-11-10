# 占位符与表达式

OrcaSlicer 在展开自定义 G-code 和文件名模板时会填入占位符。

把占位符写在花括号中，例如 `{layer_num}`。每个工艺、耗材丝和打印机设置都是一个占位符，名称就是它的配置键。本页列出的是其余的占位符，它们由 OrcaSlicer 在切片过程中设置。

{{T1}}

> [!TIP]
> 要查找某个设置的键名，可以在 OrcaSlicer 中把鼠标悬停在它的标签上，或者查看该设置 wiki 页面中的*变量*一行。
>
> {{I1}}

## 各 G-code 字段可用的占位符

每个自定义 G-code 字段都可以使用所有设置，以及[耗材丝、挤出机和喷嘴]({{L1}})、[温度]({{L2}})、[尺寸]({{L3}})、[打印统计]({{L4}})、[对象]({{L5}})、[盘]({{L6}})、[预设]({{L7}})、[时间戳]({{L8}})、[环境]({{L9}})和[工具头位置]({{L10}})中的占位符。有些字段还有下表列出的额外占位符。

| 字段 | 键 | 额外占位符 |
| --- | --- | --- |
| 文件头 G-code | `file_start_gcode` | 无 |
| 起始 G-code（打印机） | `machine_start_gcode` | 无 |
| 起始 G-code（耗材丝） | `filament_start_gcode` | [层占位符]({{L11}})和[耗材丝起始和结束 G-code]({{L12}}) |
| 换层前 G-code | `before_layer_change_gcode` | [层占位符]({{L13}}) |
| 换层 G-code | `layer_change_gcode` | [层占位符]({{L14}})和[换层 G-code]({{L15}}) |
| 延时摄影 G-code | `time_lapse_gcode` | [层占位符]({{L16}})和[延时摄影和结块检测 G-code]({{L17}}) |
| 结块检测 G-code | `wrapping_detection_gcode` | [层占位符]({{L18}})、`most_used_physical_extruder_id` 和 `curr_physical_extruder_id` |
| 耗材丝更换 G-code | `change_filament_gcode` | [层占位符]({{L19}})和[耗材丝更换 G-code]({{L20}}) |
| 挤出类型更换 G-code | `change_extrusion_role_gcode`<br>`filament_change_extrusion_role_gcode`<br>`process_change_extrusion_role_gcode` | *`filament_change_extrusion_role_gcode` 和 `process_change_extrusion_role_gcode` 为 2.4.0 新增。* [挤出类型更换 G-code]({{L21}}) |
| 暂停 G-code | `machine_pause_gcode` | 无 |
| IDEX/IQEX 模式 G-code | `imex_mode_gcodes` | *2.5.0 新增。* 无。它在打印机起始 G-code 之前运行。其中的错误会以 `imex_mode_gcode` 的名称显示。 |
| 模板自定义 G-code | `template_custom_gcode` | 无 |
| 对象之间 G-code | `printing_by_object_gcode` | 无 |
| 结束 G-code（耗材丝） | `filament_end_gcode` | [层占位符]({{L22}})和[耗材丝起始和结束 G-code]({{L23}}) |
| 结束 G-code（打印机） | `machine_end_gcode` | [层占位符]({{L24}})，以及[耗材丝起始和结束 G-code]({{L25}})中与耗材丝相关的值 |
| 文件名模板 | `filename_format` | 另一套占位符：所有设置，以及标有*也可用于文件名*的占位符。参见[文件名模板]({{L26}})。 |

`machine_pause_gcode` 没有额外占位符。旧的 `color_change_extruder` 占位符已不再设置，使用它会失败。

## 表格说明

- **类型**列给出每个值的单位，例如 float（mm）。计数、文本和布尔值没有单位。
- 名称后面的 `[]` 表示列表，例如每种耗材丝一个值的列表。要取其中一个值，请参见[表达式与函数]({{L27}})。
- 对于耗材丝、挤出机或喷嘴索引，类型列会注明是三者中的哪一种。许多旧名称写的是 *extruder*（挤出机），实际指的却是耗材丝，例如 `current_extruder`、`previous_extruder` 和 `is_extruder_used`。请以类型列为准。
    - **耗材丝索引**：在耗材丝列表中的位置，从 0 开始计数。
    - **挤出机索引**：物理挤出机或工具头，从 0 开始计数，与 `current_extruder_id` 相同。`filament_map[]` 给出每种耗材丝对应的挤出机。
    - **喷嘴索引**：喷嘴。除非打印机的每个挤出机有多个喷嘴，否则它与挤出机索引相同。
- **类型 1** 和**类型 2** 擦拭塔是*擦拭塔类型*设置的两个取值。类型 1 是拓竹风格的擦拭塔。拓竹打印机总是使用类型 1。

## 表达式与函数

在 `{ }` 内部，OrcaSlicer 会对一种小型表达式语言求值。占位符名称区分大小写。可以用圆括号对表达式的各部分分组。

可用的运算符如下：

- 算术运算 `+`、`-`、`*`、`/` 和 `%`（取余）。例如，`{filament_diameter[0] / 2}` 是第一种耗材丝的半径。
- 比较运算 `==`、`!=`、`<`、`>`、`<=` 和 `>=`，结果为布尔值。
- 逻辑运算 `and` / `&&`、`or` / `||` 和 `not` / `!`。
- 条件运算 `condition ? a : b`，`condition` 为真时得到 `a`，为假时得到 `b`。
- 用 `+` 连接文本，例如 `{"v" + layer_num}`。
- 正则表达式匹配 `text =~ /pattern/`，当整段文本与模式匹配时为真；`!~` 则在不匹配时为真。要查找文本中的一部分，请在模式前后加上 `.*`，例如 `{if printer_notes =~ /.*BAMBU.*/}bambu{endif}`。

可用的函数如下：

| 函数 | 说明 |
| --- | --- |
| `int(x)` | 去掉小数部分的 `x`。`{int(13.9)}` 为 `13`。 |
| `round(x)`<br>`floor(x)`<br>`ceil(x)` | 把 `x` 四舍五入、向下或向上取整。 |
| `min(a, b)`<br>`max(a, b)` | 两个数中较小或较大的那个。 |
| `digits(value, width [, decimals])` | 把 `value` 在 `width` 个字符宽度内右对齐，可选指定固定的小数位数。 |
| `zdigits(value, width [, decimals])` | 与 `digits` 相同，但用前导零填充。`{zdigits(5, 4)}` 为 `0005`。 |
| `random(a, b)` | `a` 和 `b` 之间的随机数。 |
| `interpolate_table(x, (x0, y0), (x1, y1), ...)` | 在给定各点之间的连线上，`x` 对应的 `y` 值。各 x 值必须递增，并且 `x` 必须位于第一个和最后一个 x 值之间。 |
| `one_of(value, a, b, ...)` | 当文本 `value` 等于列出的某个文本时为真。列出的值可以是 `/regex/` 正则模式，此时必须匹配整段文本。`value` 必须是文本，不能是数字。 |
| `regex_replace(text, /pattern/, replacement)` | *2.5.0 新增。* 把 `text` 中每处与 `/pattern/` 匹配的内容替换为 `replacement`。替换内容可以使用捕获组（`$1`、`$2`……）。 |
| `size(list)`<br>`empty(list)` | 列表中值的个数，以及列表是否为空。 |
| `is_nil(name)` | 当值未设置时为真，例如留空的耗材丝覆盖值。对于列表，需要给出索引。 |
| `filament_change(n)` | 从自定义 G-code 中的这一位置起，不带索引的小数列表给出的是耗材丝 `n` 的值。 |

`{if}`、`{elsif}`、`{else}` 和 `{endif}` 用于在几段文本之间进行选择，例如 `{if layer_num == 0}first{else}later{endif}`。

可以把值存入变量。`{local name = "part"}{name}` 先定义一个变量，然后输出它。`{local}` 变量只存在于定义它的那段自定义 G-code 中。`{global}` 变量在同一次打印中稍后运行的自定义 G-code 里也可以使用。变量也可以保存列表：`{local temps = (200, 210)}` 生成一个包含两个值的列表，`{local zeros = repeat(4, 0)}` 生成一个包含四个零的列表。

要从列表中取一个值，请给出它的索引，从 0 开始计数。例如，`{nozzle_temperature[1]}` 是第二种耗材丝的值。在 `{ }` 内部，不带索引的小数列表给出的是当前耗材丝的值。不带索引的整数、布尔值、文本或坐标点列表会失败，并报错"Referencing a vector variable when scalar is expected"（需要标量时引用了向量变量）。

OrcaSlicer 也接受一种较旧的语法 `[name]`，它只输出一个占位符，不支持表达式。布尔值在 `{ }` 中输出为 `true` 或 `false`，在 `[ ]` 中输出为 `1` 或 `0`。

## 常见错误

当自定义 G-code 中的占位符出错时，G-code 导出会失败。错误消息以"Failed to generate G-code for invalid custom G-code."（由于错误的自定义 G-code，G-code 生成失败）开头，并针对每个出错的字段给出字段的键名及该字段中的第一个错误。`filename_format` 中的错误则以"Processing of the filename_format template failed."（处理文件名格式模板失败）开头。

| 错误 | 原因 |
| --- | --- |
| `Not a variable name`（不是变量名，出现在 `{ }` 中）或 `Variable does not exist`（变量不存在，出现在 `[ ]` 中） | 名称拼写错误、该字段没有这个占位符（参见[各 G-code 字段可用的占位符]({{L28}})），或者你使用的 OrcaSlicer 版本还没有它。在 `filename_format` 中，只有设置项和标有*也可用于文件名*的占位符存在，参见[文件名模板]({{L29}})。 |
| `Referencing a vector variable when scalar is expected`（需要标量时引用了向量变量） | 使用整数、布尔值、文本或坐标点列表时没有加索引。请加上索引，例如 `{nozzle_temperature[0]}`。 |
| `This value is known only after the G-code is generated. It can be printed, but not used in a calculation or a comparison.`（此值仅在生成 G-code 后才可知。它可以被输出，但不能用于计算或比较。） | 在计算中使用了标有*生成后填入*的值。参见[打印统计]({{L30}})。 |

## 耗材丝、挤出机和喷嘴

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `current_extruder`<br>`current_filament_id` | int（耗材丝索引） | *`current_filament_id` 为 2.5.0 新增。* 当前正在打印的耗材丝。这两个名称通常给出相同的值。在打印机结束 G-code 中，以及拓竹打印机第一种耗材丝的起始 G-code 中，`current_filament_id` 可能不同。参见[耗材丝起始和结束 G-code]({{L31}})。 |
| `current_extruder_id` | int（挤出机索引） | *2.5.0 新增。* 当前正在打印的挤出机。在 `change_filament_gcode` 中，它仍然是即将换下的挤出机。 |
| `current_nozzle_id` | int（喷嘴索引） | *2.5.0 新增。* 当前正在打印的喷嘴。 |
| `current_hotend` | int | *2.4.0 新增。* 在大多数打印机上，是当前正在打印的挤出机。在拓竹打印机上，当打印过程中耗材丝在喷嘴之间转移时，它是热端架上的喷嘴，否则为 `-1`。 |
| `has_single_extruder_multi_material_priming` | bool | 使用单挤出机多材料预挤出区域时为 `true`。 |
| `initial_extruder`<br>`initial_tool`<br>`initial_filament_id` | int（耗材丝索引） | *`initial_filament_id` 为 2.5.0 新增。* 打印中使用的第一种耗材丝。三个名称给出相同的值。`initial_extruder` 和 `initial_tool` 也可用于文件名。 |
| `initial_nozzle_id` | int（喷嘴索引） | *2.5.0 新增。* 第一种耗材丝所用的喷嘴。 |
| `initial_no_support_extruder`<br>`initial_no_support_tool`<br>`initial_no_support_filament_id` | int（耗材丝索引） | *`initial_no_support_filament_id` 为 2.5.0 新增。* 第一种非支撑耗材丝。`initial_no_support_extruder` 也可用于文件名。 |
| `initial_no_support_hotend` | int | *2.4.0 新增。* 该耗材丝所用的热端，规则与 `current_hotend` 相同。 |
| `is_extruder_used[]` | 每种耗材丝一个 bool | 打印中用到的每种耗材丝为 `true`。 |
| `filament_map[]` | 每种耗材丝一个 int（挤出机索引 + 1） | 每种耗材丝对应的挤出机，从 **1** 开始计数。在 `change_filament_gcode` 中，`filament_map[next_extruder] - 1` 是即将换上的挤出机。也可用于文件名。 |
| `first_tools[]`<br>`first_filaments[]` | 每个挤出机一个 int（耗材丝索引） | 每个挤出机打印的第一种耗材丝，或 `-1`。在拓竹打印机和 IDEX/IQEX 打印机上是正确的。在其他多挤出机打印机上，这些值目前是错误的。 |
| `first_non_support_tools[]`<br>`first_non_support_filaments[]`<br>`first_non_support_hotend[]` | 每个挤出机一个 int | *`first_non_support_hotend` 为 2.5.0 新增。* 与 `first_tools[]` 相同，但不包括支撑耗材丝。`first_non_support_hotend[]` 给出的则是该耗材丝的热端，规则与 `current_hotend` 相同。同样的限制也适用。 |
| `num_extruders` | int | 打印机上物理挤出机的数量，即使打印中用得更少也是如此。也可用于文件名。 |
| `nozzle_diameter_at_nozzle_id[]`<br>`nozzle_volume_types[]` | float（mm）<br>string | *2.5.0 新增。* 每个喷嘴的直径和流量类型。在每个挤出机只有一个喷嘴的打印机上，每个挤出机一个值。 |
| `flush_temperatures[]`<br>`flush_volumetric_speeds[]` | int（°C）<br>float（mm³/s） | 每种耗材丝的冲刷温度和冲刷速度。 |
| `retraction_distance_when_cut` | float（mm） | 当前耗材丝被 AMS 或切料器切断时的回抽距离。 |
| `long_retraction_when_cut` | bool | 当前耗材丝开启了*切料时长回抽*时为 `true`。 |
| `retraction_distance_when_ec`<br>`long_retraction_when_ec` | float（mm）<br>bool | 更换挤出机时对应的这两个值。 |
| `is_all_bbl_filament`<br>`has_tpu_in_first_layer`<br>`enable_high_low_temp_mix`<br>`hold_chamber_temp_for_flat_print`<br>`max_additional_fan`<br>`during_print_exhaust_fan_speed_num[]` | 多种 | 拓竹起始 G-code 使用的值。 |

## 温度

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `bed_temperature[]` | 每种耗材丝一个 int（°C） | 每种耗材丝在当前打印板类型下的热床温度。 |
| `bed_temperature_initial_layer[]`<br>`first_layer_bed_temperature[]` | 每种耗材丝一个 int（°C） | 每种耗材丝在当前打印板类型下的首层热床温度。 |
| `bed_temperature_initial_layer_single` | int（°C） | 最先打印的耗材丝（`initial_extruder`）的首层热床温度。如果热床温度计算方式设为取最高温度，则为首层所用各耗材丝中最高的首层热床温度。 |
| `first_layer_temperature[]` | 每种耗材丝一个 int（°C） | 每种耗材丝的首层喷嘴温度。 |
| `chamber_temperature[]` | 每种耗材丝一个 int（°C） | 每种耗材丝的腔体温度。也可用于文件名。 |
| `chamber_minimal_temperature[]` | 每种耗材丝一个 int（°C） | *2.4.1 新增。* 每种耗材丝的最低腔体温度。也可用于文件名。 |
| `overall_chamber_temperature` | int（°C） | 所用耗材丝中最高的 `chamber_temperature[]`。 |
| `min_vitrification_temperature` | int（°C） | 所用耗材丝中最低的软化温度。 |

## 尺寸

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `first_layer_print_convex_hull` | `[x, y]` 坐标对数组（mm） | 首层的凸包，以多边形表示。 |
| `first_layer_print_min` | float[2]（mm） | 首层的最小 X 和 Y。 |
| `first_layer_print_max` | float[2]（mm） | 首层的最大 X 和 Y。 |
| `first_layer_print_size` | float[2]（mm） | 首层的宽度和深度。 |
| `first_layer_center_no_wipe_tower` | float[2]（mm） | 首层上各对象（包括其 Brim）的中心。每个对象只计算第一个副本。不包括擦拭塔和裙边。 |
| `in_head_wrap_detect_zone` | bool | 当对象的俯视投影或首层触及包裹检测区域时为 `true`。 |
| `first_layer_height` | float（mm） | 首层高度。 |
| `print_bed_min` | float[2]（mm） | 热床的最小 X 和 Y。 |
| `print_bed_max` | float[2]（mm） | 热床的最大 X 和 Y。 |
| `print_bed_size` | float[2]（mm） | 热床的宽度和深度。 |
| `max_print_z` | int（mm） | 最高对象的高度，向上取整。 |
| `max_print_height` | int（mm） | 打印机的最大打印高度。 |
| `adaptive_bed_mesh_min`<br>`adaptive_bed_mesh_max` | float[2]（mm） | 探测区域的两个角点。参见[自适应网床]({{L32}})。 |
| `bed_mesh_probe_count`<br>`bed_mesh_algo` | int[2]<br>string | 该区域的探测点数量和插值算法。 |
| `has_wipe_tower` | bool | 打印包含擦拭塔时为 `true`。 |
| `wipe_tower_wait_pos_x`<br>`wipe_tower_wait_pos_y` | float（mm） | *2.5.0 新增。* 擦拭塔外侧紧邻的一个点，喷嘴可以在这里等待加热。`wipe_tower_center_pos_x` 和 `wipe_tower_center_pos_y` 以 Bambu Studio 使用的名称保存相同的值。 |
| `wipe_tower_wait_pos_valid` | bool | *2.5.0 新增。* 打印包含擦拭塔并且设置了上述点时为 `true`。`wipe_tower_center_pos_valid` 以 Bambu Studio 使用的名称保存相同的值。 |

## 打印统计

其中一些值标有*生成后填入*。OrcaSlicer 只有在整个 G-code 生成之后才知道这些值。在自定义 G-code 中，它先写入一个标记，最后再把标记替换为实际值。在自定义 G-code 中，这些值保留两位小数；在文件名中，它们可以有更多位数。

由于值此时还未知，你可以输出它、把它与文本连接，但不能用它进行计算：

| 可行 | 失败 |
| --- | --- |
| `{total_weight}` | `{total_weight * 2}` |
| `{"Weight: " + total_weight + " g"}` | `{total_weight + 5}` |
| `{local w = total_weight}{w}` | `{if total_weight > 100}heavy{endif}` |
| | `{int(total_weight)}` |

"失败"列中的表达式会使切片中止，并报错"This value is known only after the G-code is generated. It can be printed, but not used in a calculation or a comparison."。`round()`、`min()` 和 `one_of()` 等函数、正则表达式匹配，以及在变量中保存的该值副本，都会引发同样的错误。

OrcaSlicer 从左到右读取 `+`，文本与数字连接后仍然是文本。所以重量为 123.45 g 时，`{"W: " + total_weight + 5}` 会输出 `W: 123.455`，而不会加上 5。

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `normal_print_time`<br>`print_time` | string | 普通模式下的预计打印时间，写法如 `2d3h15m`、`2h15m`、`5m30s` 或 `45s`。一小时及以上的时间会四舍五入到分钟。生成后填入。也可用于文件名。 |
| `silent_print_time` | string | 静音模式下的预计打印时间，格式相同。除非 G-code 风格为 Marlin 且开启了*静音模式*，否则为 `0s`。生成后填入。也可用于文件名。 |
| `print_time_total_sec` | float（s） | *2.5.0 新增。* 普通模式下的预计打印时间，以秒为单位。生成后填入。 |
| `print_time_day`<br>`print_time_hour`<br>`print_time_minute`<br>`print_time_sec` | int（天）<br>int（时）<br>int（分）<br>int（秒） | *`print_time_day`、`print_time_hour` 和 `print_time_minute` 为 2.5.0 新增。* 普通模式打印时间中的天、时、分、秒部分。`print_time_sec` 只是其中的秒数部分，而不是总秒数。生成后填入。 |
| `total_layer_count` | int | 层数。 |
| `total_toolchanges` | int | 打印中的换料次数。打印开始时选中的耗材丝不计入。有擦拭塔时，这是擦拭塔的计数；没有擦拭塔时，OrcaSlicer 统计计划的工具顺序中的换料次数。在没有擦拭塔的逐件打印中为 `0`。也可用于文件名。 |
| `printing_filament_types` | string | *仅限[每夜构建版]({{L33}})。* 该盘打印所用的耗材丝类型，去除重复，按耗材丝列表的顺序用 `_` 连接。例如 `ABS_PLA`。也可用于文件名。 |
| `used_filament`<br>`used_filament_length` | float（m） | 整个打印使用的耗材丝长度。生成后填入。`used_filament` 也可用于文件名。 |
| `extruded_volume[]` | 每种耗材丝一个 float（mm³） | 每种耗材丝到目前为止的挤出体积。在自定义 G-code 中这是一个累计值，所以在起始 G-code 中为 `0`。`extruded_volume` 也可用于文件名，此时为总体积。 |
| `extruded_volume_total` | float（mm³） | `extruded_volume[]` 之和，同样是累计值。也可用于文件名，此时为整个打印的总量。 |
| `extruded_weight[]` | 每种耗材丝一个 float（g） | 每种耗材丝到目前为止的挤出重量，根据耗材丝密度计算。同样是累计值。 |
| `extruded_weight_total` | float（g） | `extruded_weight[]` 之和，同样是累计值。整个打印的重量请使用 `total_weight`。也可用于文件名，此时为整个打印的总量。 |
| `total_weight` | float（g） | 整个打印的耗材丝重量。生成后填入。也可用于文件名。 |
| `total_cost` | float（货币） | 耗材丝成本加上打印机的时间成本（每打印一小时的 `time_cost`）。生成后填入。也可用于文件名。 |
| `total_wipe_tower_cost` | float（货币） | 擦拭塔的耗材丝成本。生成后填入。使用类型 1 擦拭塔时目前为 `0`。也可用于文件名。 |
| `total_wipe_tower_filament` | float（mm） | 擦拭塔所用的耗材丝长度。生成后填入。使用类型 1 擦拭塔时目前为 `0`。也可用于文件名。 |

## 对象

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `num_objects` | int | 盘上的对象数量。对象的副本计入 `num_instances`。也可用于文件名。 |
| `num_instances` | int | 所有对象被打印的实例总数。也可用于文件名。 |
| `current_object_idx` | int | 当前正在打印的对象在打印顺序中的位置，从 0 开始计数。对象的每个副本都单独计数。只有在逐件打印时才会变化。 |
| `scale[]` | 每个对象一个 string | 每个对象的缩放比例文本，例如 `x:100% y:50% z:100%`。也可用于文件名。 |
| `input_filename_base` | string | 第一个可打印对象的名称，不含扩展名。如果对象没有名称，则为其源文件的名称。也可用于文件名，对于已保存的项目，此时为项目名称。 |
| `input_filename` | string | `input_filename_base` 后接 `.gcode`。也可用于文件名。 |
| `first_object_name` | string | *2.4.2 新增。* 盘上第一个可打印对象的名称。也可用于文件名。 |

## 盘

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `plate_name` | string | 盘的名称。也可用于文件名。 |
| `plate_number` | string | 盘的编号，从 1 开始计数并补足两位，例如 `01`。也可用于文件名。 |
| `model_name` | string | 3MF 项目中保存的模型名称，或为空。也可用于文件名。 |
| `imex_mode` | string | *2.5.0 新增。* 该盘所用 [IDEX/IQEX]({{L34}}) 并行模式的名称，主模式下为 `primary`。打印机不是 IDEX/IQEX 打印机时为空。 |
| `imex_mode_index` | int | *2.5.0 新增。* 该模式在打印机 `imex_mode_names` 中的索引，从 0 开始计数，即它在[模式]({{L35}})表格中的行号。`0` 表示主模式。 |
| `imex_mode_gcode` | string | *2.5.0 新增。* 该模式的[模式 G-code]({{L36}})，尚未填入其中的占位符。 |

## 预设

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `print_preset` | string | 工艺预设的名称。也可用于文件名。 |
| `filament_preset[]` | 每种耗材丝一个 string | 每种耗材丝的预设名称。也可用于文件名。 |
| `filament_type[]` | 每种耗材丝一个 string | 每种耗材丝的材料类型，例如 `PLA` 或 `PETG`。也可用于文件名。 |
| `printer_preset` | string | 打印机预设的名称。也可用于文件名。 |

## 时间戳

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `timestamp` | string（`yyyyMMdd-hhmmss`） | 开始导出 G-code 时的本地时间。也可用于文件名，此时为生成文件名时的时间。 |
| `year`<br>`month`<br>`day` | int | `timestamp` 的日期。也可用于文件名。 |
| `hour`<br>`minute`<br>`second` | int | `timestamp` 的时刻。也可用于文件名。 |

## 环境

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `user` | string | 取自 `USER` 或 `USERNAME` 环境变量的用户名，或 `unknown`。也可用于文件名。 |
| `version` | string | OrcaSlicer 版本。也可用于文件名。 |

## 工具头位置

这些值描述的是自定义 G-code 开始时工具头的状态。只有 `zhop` 是只读的。如果你的 G-code 移动了工具头，请更新 `position[]`，OrcaSlicer 会从新位置继续。

只有在关闭*单挤出机多材料*时，`e_position[]` 和 `e_retracted[]` 才是正确的，OrcaSlicer 也才会读回你的修改。这个设置默认是开启的。开启时，请不要使用这两个值。

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `zhop` | float（mm） | 自定义 G-code 开始时的 Z 抬升高度。只读。 |
| `position[]` | float[3]（mm） | 自定义 G-code 开始时工具头的 X、Y 和 Z 位置。 |
| `e_position[]` | 每种耗材丝一个 float（mm） | 挤出轴的位置。仅在 G-code 使用绝对 E 距离时使用。 |
| `e_retracted[]` | 每种耗材丝一个 float（mm） | 自定义 G-code 开始时耗材丝已回抽的长度。 |
| `e_restart_extra[]` | 每种耗材丝一个 float（mm） | 下一次回填之后额外挤出的长度。 |

## 特定 G-code 的占位符

OrcaSlicer 只在各小节所指明的 G-code 中设置本节的占位符。[各 G-code 字段可用的占位符]({{L37}})按字段列出了它们。

### 层占位符

这些占位符可用于换层前、换层、延时摄影、结块检测、耗材丝更换、耗材丝起始、耗材丝结束和打印机结束 G-code。

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `layer_num` | int | 当前层，从 0 开始计数。在第一层之前为 `-1`，例如打印开始时调用 `change_filament_gcode` 的那一次。`before_layer_change_gcode` 和 `layer_change_gcode` 得到的编号相同，都是即将打印的那一层。 |
| `layer_z` | float（mm） | 当前层顶面的高度。在耗材丝起始、耗材丝结束和打印机结束 G-code 中，是喷嘴当前的高度。使用类型 1 擦拭塔时，耗材丝起始和结束 G-code 得到的是擦拭塔层的高度。 |
| `max_layer_z` | float（mm） | 到目前为止打印的最高层的高度。 |

### 耗材丝起始和结束 G-code

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `filament_extruder_id` | int | 在 `filament_start_gcode` 中，是装入的耗材丝；在 `filament_end_gcode` 中，是卸下的耗材丝。在不使用类型 1 擦拭塔的换工具头过程中，`filament_end_gcode` 得到的则是该耗材丝的挤出机。`change_filament_gcode` 中不设置。 |
| `current_filament_id`<br>`current_nozzle_id` | int（耗材丝索引）<br>int（喷嘴索引） | *2.5.0 新增。* 该 G-code 所针对的耗材丝和喷嘴。大多数调用都会设置，包括来自类型 1 擦拭塔的调用。 |
| `retraction_distance_when_cut`<br>`long_retraction_when_cut` | float（mm）<br>bool | 在 `filament_start_gcode` 中，是装入的耗材丝的值。参见[耗材丝、挤出机和喷嘴]({{L38}})。 |

第一种耗材丝的起始 G-code 在第一层之前运行，所以那里的 `layer_num` 为 `-1`。在拓竹打印机上，这段耗材丝起始 G-code 紧接在打印机起始 G-code 之后运行，针对的是第一种非支撑耗材丝。

打印结束时，`filament_end_gcode` 会对耗材丝列表中的每种耗材丝各运行一次，然后运行 `machine_end_gcode`。使用单挤出机多材料时，它只对当前耗材丝运行。`machine_end_gcode` 得到的 `filament_extruder_id`、`current_filament_id`、`current_extruder_id` 和 `current_nozzle_id` 来自上述最后一次调用，这不一定是最后打印的那种耗材丝。

### 换层 G-code

`layer_change_gcode` 还有以下占位符：

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `current_filament_id`<br>`current_nozzle_id` | int（耗材丝索引）<br>int（喷嘴索引） | *2.5.0 新增。* 该层开始时正在打印的耗材丝和喷嘴。 |
| `most_used_physical_extruder_id` | int | 在打印中使用层数最多的物理挤出机。每一层的值都相同。 |
| `previous_layer_mass`<br>`curr_accumulated_mass` | float（g） | *2.5.0 新增。* 上一层的重量，以及到目前为止打印的全部重量。用于根据热床上的重量限制 Y 轴加速度的打印机。有擦拭塔时，重量包括整个擦拭塔的耗材丝。`curr_layer_mass` 以 Bambu Studio 使用的名称保存与 `previous_layer_mass` 相同的值。 |
| `curr_y_acceleration_limit` | float（mm/s²） | *2.5.0 新增。* 该重量下允许的 Y 轴加速度。 |

### 延时摄影和结块检测 G-code

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `most_used_physical_extruder_id` | int | 在打印中使用层数最多的物理挤出机。可用于 `time_lapse_gcode` 和 `wrapping_detection_gcode`。 |
| `curr_physical_extruder_id` | int | 该 G-code 运行时处于活动状态的物理挤出机。可用于 `time_lapse_gcode` 和 `wrapping_detection_gcode`。 |
| `timelapse_pos_x`<br>`timelapse_pos_y` | int（mm） | 为拍摄选定的 X 和 Y 位置，取整到毫米。仅用于 `time_lapse_gcode`。 |
| `has_timelapse_safe_pos` | bool | 找到了安全的拍摄位置时为 `true`。仅用于 `time_lapse_gcode`。 |
| `timelapse_inline_photo` | bool | *2.5.0 新增。* 拍摄时不移动到选定位置时为 `true`。仅用于 `time_lapse_gcode`。 |
| `farthest_point_timelapse_enabled` | bool | *2.5.0 新增。* 该层开启了最远点延时摄影时为 `true`。仅用于 `time_lapse_gcode`。 |
| `clear_to_x0` | bool | *2.5.0 新增。* 喷嘴可以移动到 X = 0 而不越过打印件时为 `true`。仅用于 `time_lapse_gcode`。 |

### 耗材丝更换 G-code

这些占位符在 `change_filament_gcode` 中设置。

在大多数非拓竹打印机上，`change_filament_gcode` 还会在打印开始、选择第一种耗材丝时运行一次。在拓竹打印机上，或者打印只使用第一种耗材丝时，不会进行这次调用。在这次调用中，`layer_num` 为 `-1`，`toolchange_count` 为 `1`。`previous_extruder`、`current_filament_id` 和 `current_hotend` 为 `-1`，除非打印机起始 G-code 用 `T` 命令选择了工具头。要跳过这次调用，请判断 `layer_num >= 0`。

开启*启用擦拭塔接触层功能*后，在擦拭塔接触层上进行的换工具头会让换上的耗材丝使用接触层打印温度。在 `change_filament_gcode` 中，`new_filament_temp`，以及 `temperature[]` 和 `first_layer_temperature[]` 中换上的耗材丝对应的值，都是这个温度。使用类型 2 擦拭塔时，`nozzle_temperature[]` 和 `nozzle_temperature_initial_layer[]` 也是如此，`filament_start_gcode` 中的这些值同样如此。

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `previous_extruder`<br>`next_extruder` | int（耗材丝索引） | 卸下的耗材丝和装入的耗材丝。 |
| `current_filament_id`<br>`next_filament_id` | int（耗材丝索引） | *2.5.0 新增。* 与 `previous_extruder` / `next_extruder` 的值相同。 |
| `current_hotend`<br>`next_hotend` | int | *2.4.0 新增。* 在大多数打印机上，是换下和换上的挤出机。在拓竹打印机上，当打印过程中耗材丝在喷嘴之间转移时，是热端架上的喷嘴，否则为 `-1`。 |
| `current_nozzle_id`<br>`next_nozzle_id` | int（喷嘴索引） | *2.5.0 新增。* 换下和换上的喷嘴。 |
| `old_extruder_variant`<br>`new_extruder_variant` | string | *2.5.0 新增。* 换下和换上的挤出机的挤出机变种，例如 `Direct Drive Standard`。 |
| `toolchange_z` | float（mm） | 发生换料的那一层的打印高度。使用类型 1 擦拭塔时，是擦拭塔层的高度。不包括 Z 抬升。 |
| `outer_wall_volumetric_speed` | float（mm³/s） | 新耗材丝的外墙体积速度，受其最大体积速度限制。 |
| `relative_e_axis` | bool | OrcaSlicer 使用相对 E 距离时为 `true`。 |
| `toolchange_count` | int | 到目前为止的换工具头次数，包括本次。当 `change_filament_gcode` 在打印开始时运行时，那次调用计为 `1`，所以第一次真正的换料是 `2`，最后一次是 `total_toolchanges + 1`。如果没有那次调用（例如在拓竹打印机上），第一次真正的换料就是 `1`。 |
| `fan_speed` | int | 旧占位符，保留它是为了让旧的 G-code 仍能工作。始终为 `0`。 |
| `filament_retract_length_nc` | float（mm） | *2.5.0 新增。* 换下的耗材丝在更换喷嘴时的回抽长度，没有时为 `0`。 |
| `new_extruder_retracted_length` | float（mm） | *2.5.0 新增。* 换上的挤出机中耗材丝当前已回抽的长度。 |
| `old_retract_length`<br>`new_retract_length` | float（mm） | 换下和换上的耗材丝的回抽长度。 |
| `old_retract_length_toolchange`<br>`new_retract_length_toolchange` | float（mm） | 换下和换上的耗材丝在换工具头时的回抽长度。 |
| `old_filament_temp`<br>`new_filament_temp` | int（°C） | 换下和换上的耗材丝的喷嘴温度。 |
| `old_filament_e_feedrate`<br>`new_filament_e_feedrate` | int（mm/min） | 换下和换上的耗材丝的挤出进给速度，由其体积速度上限计算而来。 |
| `x_after_toolchange`<br>`y_after_toolchange`<br>`z_after_toolchange` | float（mm） | 换料前的喷嘴位置，或者类型 1 擦拭塔上的起点。修改它们没有效果。要告诉 OrcaSlicer 喷嘴已经移动，请更新 `position[]`。 |
| `first_flush_volume`<br>`second_flush_volume` | float（耗材丝长度 mm） | 计划冲刷长度的前一半和后一半。 |
| `flush_length` | float（耗材丝长度 mm） | 本次换工具头的总冲刷长度。 |
| `flush_length_1` … `flush_length_4` | float（耗材丝长度 mm） | 冲刷的各个部分。未使用的部分为 `0`。 |
| `wipe_avoid_perimeter` | bool | 本次换料的空驶需要绕开擦拭塔时为 `true`。只由类型 1 擦拭塔设置，其他情况下为 `false`。 |
| `wipe_avoid_pos_x` | float（mm） | 空驶在擦拭塔周围避让的那条线的 X 位置。只由类型 1 擦拭塔使用。 |
| `is_prime_tower_interface` | bool | 使用类型 1 擦拭塔时，本次换料打印的是擦拭塔接触层则为 `true`。 |
| `filament_tower_interface_purge_volume`<br>`filament_tower_interface_print_temp` | float（耗材丝长度 mm）<br>int（°C） | 新耗材丝的接触层冲刷长度和接触层打印温度。 |
| `filament_cooling_before_tower[]` | 每种耗材丝一个 float（°C） | *2.4.0 新增。* 喷嘴进入擦拭塔之前降温的幅度。只由类型 1 擦拭塔设置，在首层和接触层上为 `0`。 |
| `wipe_tower_wait_pos_x`<br>`wipe_tower_wait_pos_y`<br>`wipe_tower_wait_pos_valid` | float（mm）<br>float（mm）<br>bool | *2.5.0 新增。* 与[尺寸]({{L39}})中的点相同。使用类型 1 擦拭塔时，该点紧邻本次换工具头开始的位置。Bambu Studio 的名称 `wipe_tower_center_pos_x`、`wipe_tower_center_pos_y` 和 `wipe_tower_center_pos_valid` 保存相同的值。 |
| `travel_point_1_x`<br>`travel_point_1_y` | float（mm） | 拓竹切料器所用空驶路径的第一个点。在其他打印机上为固定的默认值。 |
| `travel_point_2_x`<br>`travel_point_2_y` | float（mm） | 该空驶路径的第二个点。 |
| `travel_point_3_x`<br>`travel_point_3_y` | float（mm） | 该空驶路径的第三个点。 |

### 挤出类型更换 G-code

这些占位符可用于 `change_extrusion_role_gcode`、`filament_change_extrusion_role_gcode` 和 `process_change_extrusion_role_gcode`。

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `extrusion_role` | string | OrcaSlicer 即将打印的[挤出类型]({{L40}})，例如 `Perimeter`。 |
| `last_extrusion_role` | string | 上一个[挤出类型]({{L41}})。 |
| `layer_num` | int | 当前层，在这段 G-code 中从 **1** 开始计数。 |
| `layer_z` | float（mm） | 当前层的高度。 |

### 挤出类型

`extrusion_role` 和 `last_extrusion_role` 取以下值之一。请把它们当作文本进行比较，例如 `{if extrusion_role == "Perimeter"}...{endif}`。

| 值 | 说明 |
| --- | --- |
| `Perimeter` | 内墙。 |
| `ExternalPerimeter` | 外墙。 |
| `OverhangPerimeter` | 悬垂墙。 |
| `InternalInfill` | 稀疏填充。 |
| `SolidInfill` | 内部实心填充。 |
| `TopSolidInfill` | 顶面。 |
| `BottomSurface` | 底面。 |
| `Ironing` | 熨烫。 |
| `BridgeInfill` | 桥接，包括内部桥接。 |
| `GapFill` | 缝隙填充。 |
| `Skirt` | 裙边。 |
| `Brim` | Brim。 |
| `SupportMaterial` | 支撑。 |
| `SupportMaterialInterface` | 支撑接触面。 |
| `SupportTransition` | 支撑过渡层。 |
| `WipeTower` | 擦拭塔。 |
| `Mixed` | 多种类型混合，或其他任何类型。 |

## 文件名模板

文件名模板 `filename_format` 有自己的一套占位符。它可以使用所有设置，以及上面表格中标有*也可用于文件名*的占位符。使用其他任何占位符都会让文件名生成失败，并报错"Processing of the filename_format template failed."。

在文件名中：

- 打印统计始终是最终值。如果在 G-code 生成之前就需要文件名，OrcaSlicer 会在导出后再填入这些值。
- `extruded_volume`、`extruded_volume_total` 和 `extruded_weight_total` 是整个打印的总量。`extruded_volume` 是单个值，而不是列表。
- `extruded_volume_total`、`extruded_weight_total` 和 `initial_extruder` 从 2.4.0 起可用，`initial_no_support_extruder` 从 2.5.0 起可用。

以下占位符只能用于文件名：

| 占位符 | 类型 | 说明 |
| --- | --- | --- |
| `filament_name` | string | *2.4.0 新增。* 该盘所用编号最小的耗材丝的预设名称，截取到 `@` 之前。 |
| `num_filaments` | int | 挤出机数量，与 `num_extruders` 相同。 |

## 示例

### 带温度参数的起始宏

在打印机起始 G-code 中，把首层温度传给 Klipper 宏。`first_layer_temperature[]` 每种耗材丝一个值，所以用索引 `initial_extruder` 选出最先打印的耗材丝。

{{C1}}

### 层进度

在换层 G-code 中，把当前层显示在打印机屏幕上。`layer_num` 从 0 开始计数，所以要加 1。

{{C2}}

### 只处理真正的换料

在耗材丝更换 G-code 中，跳过打印开始时的那次调用。`layer_num` 在第一层之前为 `-1`。

{{C3}}

### 针对某种挤出类型的设置

在挤出类型更换 G-code 中，对外墙使用较低的加速度。

{{C4}}

### 查表取值

根据喷嘴直径选择冲刷长度，并把它存入变量。本例使用相对 E 距离。

{{C5}}

### 在文件头中写入打印摘要

在文件头 G-code 中写入打印时间和耗材丝用量，参见[打印统计]({{L42}})。

{{C6}}

### 文件名

这是默认的文件名模板。要加入盘编号，请在 `.gcode` 之前加上 `_plate{plate_number}`。要为多材料打印列出所有耗材丝类型，而不只是第一种，请用 `{printing_filament_types}` 代替 `{filament_type[initial_tool]}`。

{{C7}}
