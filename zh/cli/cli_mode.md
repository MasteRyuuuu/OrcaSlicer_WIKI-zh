# 命令行模式

OrcaSlicer 可以在命令行中以无界面方式运行，无需打开图形界面即可加载、变换和切片模型。这对自动化、批量处理和 CI 流水线很有用。

{{T1}}

## 调用方式

{{C1}}

任何不以 `-` 开头的参数都会被当作要加载的输入文件（模型或项目），按给出的顺序加载。支持的输入格式与[支持的文件格式]({{L1}})中列出的相同。

单独使用 `--` 可以让 OrcaSlicer 不再把后面的参数当作标志解析——之后的所有内容都被视为位置参数形式的输入文件，即使以短横线开头也一样。

## 标志语法

### 布尔标志

对应简单开/关设置的标志（例如 `--info`、`--export-stl`）不需要值——只要写上这个标志就会启用它。也可以显式写 `=1` / `=0` 来强制开启或关闭。完整规则请参见[布尔值]({{L2}})，其中包括用空格分隔的 `--flag 0` 这个陷阱——它的效果并不像看上去那样。

### 带值标志

对应单个值的标志，既可以把值作为单独的参数给出，也可以用 `=` 连接：

{{C2}}

> [!IMPORTANT]
> 每个设置的键（如其 wiki 页面所示，例如 `layer_height`）都使用下划线。在命令行中，OrcaSlicer 总是把下划线转换为连字符来构成标志名——所以 `layer_height` 变成 `--layer-height`。这条规则统一适用：约 50 个仅限命令行的选项，以及所有常规的工艺、耗材丝和打印机设置都一样。命令行标志请始终使用连字符，而不要直接写带下划线的原始键名。

### 向量（多值）标志

有些设置为每个挤出机、耗材丝或对象各保存一个值（例如 `retraction_length[extruder_idx]`）。它们接受**逗号分隔的列表**，列表中的位置即索引（从 0 开始）：

{{C3}}

使用之前需要了解两种行为：

- **填充。** 如果你提供的值少于条目数（挤出机、耗材丝等），缺少的位置会用你给出的*第一个*值重复填充——而不是各条目自己的默认值。在 4 挤出机打印机上，`--retraction-length=1.2` 会变成 `[1.2, 1.2, 1.2, 1.2]`；`--retraction-length=0.9,0.8,1.2` 会变成 `[0.9, 0.8, 1.2, 0.9]`（索引 3 会悄悄得到第一个值 0.9，而不是它的默认值）。
- **重复会追加，而不是覆盖。** 多次传入同一个向量标志会追加到列表中，而不是替换它：`--retraction-length=0.8 --retraction-length=1.2` 的结果是 `[0.8, 1.2]`，而不是 `[1.2]`。要完全替换向量的内容，请在一次标志中传入整个列表。

## 设置覆盖

除了本 wiki 中记录的仅限命令行的选项（参见下方的[参考页面]({{L3}})），`--key=value` 几乎接受[打印机设置]({{L4}})、[材料设置]({{L5}})和[工艺设置]({{L6}})中记录的任何工艺、耗材丝或打印机/机器设置——也就是图形界面中打印机、耗材丝和工艺选项卡里显示的那些设置。每个选项的页面都会在 `[Variable]`/`[Variables]` 标签旁显示其键名；把下划线换成连字符即可得到标志名，并按照上面的[标志语法]({{L7}})规则处理布尔值、单值和向量。

有一组固定的 43 个键完全不会在命令行中开放。如果某个 `--key=value` 覆盖因 `Invalid option` 被拒绝，在认定是拼写错误之前，先对照下面的列表检查一下：

**预设标识与继承**（直接手写 `.json` 配置文件时使用——参见[如何创建配置文件]({{L8}})）：
`preset_name`、`compatible_printers`、`compatible_printers_condition`、`compatible_prints`、`compatible_prints_condition`、`compatible_machine_expression_group`、`compatible_process_expression_group`、`different_settings_to_system`、`print_compatible_printers`、`default_filament_profile`、`default_print_profile`、`filament_ids`、`filament_vendor`、`inherits`、`inherits_group`、`host_type`、`printer_model`、`printer_variant`、`material_vendor`、`default_sla_material_profile`、`sla_material_settings_id`、`default_sla_print_profile`、`sla_print_settings_id`

**打印主机 / 网络连接**（直接发送到联网打印机时使用的凭据和连接信息）：
`bbl_use_printhost`、`use_3mf`、`printer_agent`、`print_host`、`print_host_webui`、`printhost_apikey`、`flashforge_serial_number`、`printhost_port`、`printhost_cafile`、`printhost_user`、`printhost_password`、`printhost_ssl_ignore_revoke`、`printhost_authorization_type`

**内部挤出机/变种索引**（OrcaSlicer 内部维护的记录，用于在打印机、工艺和耗材丝配置之间匹配挤出机）：
`extruder_variant_list`、`printer_extruder_id`、`printer_extruder_variant`、`print_extruder_id`、`print_extruder_variant`、`filament_extruder_variant`、`filament_self_index`

## 参考页面

仅限命令行的选项按照与源代码相同的方式分组（`CLIActionsConfigDef`、`CLITransformConfigDef`、`CLIMiscConfigDef`）：

- [操作]({{L9}})——对加载的模型做什么：导出、切片、检查。
- [变换]({{L10}})——摆放、朝向、旋转、缩放，以及其他在切片之前应用的几何变化。
- [其他]({{L11}})——加载设置/耗材丝、输出位置、日志和元数据。

## 示例

{{C4}}

加载 `model.3mf`，应用给定的工艺/打印机/耗材丝设置，自动摆放各个盘，对每个盘进行切片，并把结果导出为 3MF。
