# 预设与预设包

本页解释代码中的 3 个类。

## [`Preset`]({{L1}})

顾名思义，这个类处理各种东西的预设。它定义了一个枚举 `Type`，基本上用来说明预设包含的是哪种数据。下面解释其中几种及其对应的界面元素。

> [!WARNING]
> 代码库中有大量过时的遗留代码。

- `TYPE_PRINT`：指工艺预设。它被称为"Print"，大概是由于某些遗留代码。

{{I1}}

- `TYPE_FILAMENT`：顾名思义，这种预设用于耗材丝

{{I2}}

- `TYPE_PRINTER`：打印机的预设。

{{I3}}

还有其他预设类型，但其中一些是用于 SLA 的。那是遗留代码，因为已经不再支持 SLA 打印机。上面这 3 种才是重要的类型。

## [`PresetBundle`]({{L2}})

这是一个包含几种 `PresetCollection` 的预设包。一个预设包中有若干打印机、耗材丝和工艺（TYPE_PRINT）的预设。

`PresetCollection            prints`\
`PresetCollection            filaments`\
`PrinterPresetCollection     printers`

它们分别包含工艺、耗材丝和打印机的集合。

> [!IMPORTANT]
> 预设包中的打印机、耗材丝和工艺并不一定彼此兼容。实际上，所有已保存的预设都存放在同一个 `PresetBundle` 中。`PresetBundle` 在启动时加载。为某台打印机显示的耗材丝和工艺列表，是 `filaments` 和 `prints` 这两个 `PresetCollection` 的子集。

## [`PresetCollection`]({{L3}})

`PrinterPresetCollection` 是从 `PresetCollection` 派生的类。

它们包含一组预设。这些预设可以是任何类型。\
这里值得注意的函数有：

`get_edited_preset()`：返回当前选中的预设，以及用户所做的任何修改。\
`get_selected_preset()`：返回当前选中的预设，不包含用户所做的修改。
