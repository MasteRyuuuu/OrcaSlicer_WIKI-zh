# 运动能力

与打印机运动能力相关的设置。

{{T1}}

## 写入限制到 G-code

{{M1}}
启用后，机器限制会写入 G-code 文件。
如果 G-code 风格设为 Klipper，这个选项会被忽略。

## 共振补偿

共振补偿是用来减少打印机在高速运动时的振动的方法，这些振动会在模型表面造成振纹。

### 共振规避

{{M2}}
通过降低外墙速度来避开打印机的共振区间，从而避免模型表面出现振纹。

> [!TIP]
> 参阅 [VFA 校准]({{L1}})。

### 输入整形

{{M3}}
在高速运动时，振动可能造成一种叫"振纹（ringing）"的现象，即打印表面出现周期性的波纹。输入整形通过抵消这些振动，提供了一种有效的解决办法，在无需大幅降低打印速度的情况下提升打印质量，并减少部件磨损。

> [!NOTE]
> 有些打印机内置了加速度计，可以**自动**测量打印机的共振频率。  
> 如果你的打印机有加速度计，建议优先使用它：结果更准确、耗时更短，而且通常会自动保存到打印机固件中。

> [!TIP]
> 一般建议每年做一次[输入整形校准]({{L2}})；在发生任何机械或结构变化后也应重新校准，例如搬动位置、更换放置台面、换新皮带、电机、框架等。

> [!IMPORTANT]
> **RepRap** 只能为 X 和 Y 两轴设置同一个频率，所以你需要选一个对两轴都效果不错的频率。

{{I1}}

#### 输入整形器类型

{{M4}}
输入整形器类型决定用于抵消振动的算法。  
通常推荐使用 MZV、EI（尤其适合 Delta 打印机）或 ZV，它们简单而有效。  
并不是所有固件都提供所有输入整形器类型，其效果也可能因固件实现和打印机机械结构而异。

##### 默认

选择"默认"时，使用固件默认的输入整形器。  
每种固件甚至每个版本的默认类型都可能不同，但通常是：

- Klipper：MZV
- Marlin：ZV
- RepRap：
    - 版本 >= 3.4：MZV
    - 版本 < 3.4：DAA
    - 版本 < 3.2：DAA（无阻尼选项）

##### 版本对照表

| 类型 | 名称 | [Klipper]({{L3}}) | [RepRap]({{L4}}) | [Marlin 2]({{L5}}) |
| --- | --- | --- | --- | --- |
| MZV | Modified Zero Vibration（改进零振动） | >=0.9.0 | >=3.4 | - |
| ZV | Zero Vibration（零振动） | >=0.9.0 | = 3.5 | >2.1.2 |
| ZVD | Zero Vibration Derivative（零振动一阶导数） | >=0.9.0 | >=3.4 | - |
| ZVDD | Zero Vibration Double Derivative（零振动二阶导数） | - | >=3.4 | - |
| ZVDDD | Zero Vibration Triple Derivative（零振动三阶导数） | - | >=3.4 | - |
| EI | Extra Insensitive（超不敏感） | >=0.9.0 | - | - |
| 2HUMP_EI / EI2 | Two-Hump Extra Insensitive（双峰超不敏感） | >=0.9.0 | >=3.4 | - |
| 3HUMP_EI / EI3 | Three-Hump Extra Insensitive（三峰超不敏感） | >=0.9.0 | >=3.4 | - |
| [FT_MOTION]({{L6}}) | Fixed-Time Motion（固定时间运动） | - | - | >2.1.3 |
| DAA | Damped Anti-Resonance（阻尼抗共振） | - | < 3.4 | - |

###### 固定时间运动

待完成：这项校准测试目前正在开发中。更多信息请参阅 [Marlin 文档]({{L7}})。

## 速度限制

为各轴设定最大速度的安全上限。
如果工艺设定的速度超过这些值，会被限制在这些值以内。

## 加速度限制

{{M5}}
`简单` [变量]({{L8}})：`machine_max_acceleration_x`、`machine_max_acceleration_y`、`machine_max_acceleration_z`、`machine_max_acceleration_e`、`machine_max_acceleration_extruding`、`machine_max_acceleration_retracting`。  
`高级` [变量]({{L9}})：`machine_max_acceleration_travel`。  
{{M6}}
为各轴设定最大加速度的安全上限。
如果工艺设定的加速度超过这些值，会被限制在这些值以内。

## 抖动限制

为各轴设定最大抖动的安全上限。

> [!TIP]
> 参阅[转角校准]({{L10}})。

### 最大抖动

{{M7}}
各轴的最大[抖动]({{L11}})（M205 X、Y、Z、E；对于 Marlin 2 固件，仅在 JD = 0 时生效）

### 最大结点偏差

{{M8}}
最大[结点偏差]({{L12}})（M205 J；对于 Marlin 固件，仅在 JD > 0 时生效。如果你的 Marlin 2 打印机使用经典抖动，请把这个值设为 0。）
