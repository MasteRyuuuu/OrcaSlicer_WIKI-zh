# 自适应网床

OrcaSlicer 为多种固件（包括 Marlin、Klipper 和 RepRapFirmware（RRF））全面支持自适应网床调平。  
这项功能让你可以把自适应网床命令无缝地整合到打印机起始 G-code 中。  
它的实现简单直接，无需额外的插件，也不用修改固件设置，直接在 OrcaSlicer 中就能改善使用体验和打印质量。  
{{I1}}

{{T1}}

## 网床范围

{{M1}}
这个选项设置允许的网床区域的最小点和最大点。由于探针存在 XY 偏移，大多数打印机无法探测整个热床。为确保探测点不会超出热床范围，应适当设置网床的最小点和最大点。  
OrcaSlicer 会确保 adaptive_bed_mesh_min/adaptive_bed_mesh_max 的值不超过这些最小/最大点。这些信息通常可以从打印机厂商那里获得。  
默认设置为 (-99999, -99999)，表示没有限制，允许探测整个热床。

## 网格点间距离

{{M2}}
这个选项设置 X 和 Y 方向上探测点之间的首选距离（网格大小），X 和 Y 的默认值都是 50mm。

## 网床边缘外扩

{{M3}}
这个选项决定自适应网床区域在 XY 方向上额外向外扩展的距离。

> [!NOTE]
> Klipper 用户：OrcaSlicer 会按照这个外扩值调整自适应网床区域。建议在 Klipper 配置中把 margin 设为 0，或者在调用 BED_MESH_CALIBRATE 命令时传入 0（请参考下面的示例）。

## 自适应网床命令可用的 G-code 变量

`bed_mesh_probe_count`：表示 X 和 Y 方向上的探测点数量。这个值根据自适应网床区域的大小和探测点之间的距离计算得出。

`adaptive_bed_mesh_min`：指定自适应网床区域的最小坐标，定义网格的起点。

`adaptive_bed_mesh_max`：确定自适应网床区域的最大坐标，表示网格的终点。

`ALGORITHM`：标识自适应网床插值所用的算法。这个变量对 Klipper 用户很有用。如果 bed_mesh_probe_count 小于 4，算法设为 `lagrange`，否则设为 `bicubic`。

## OrcaSlicer 中使用自适应网床的示例

### Marlin

{{C1}}

### Klipper

{{C2}}

### RRF

{{C3}}

{{I2}}
