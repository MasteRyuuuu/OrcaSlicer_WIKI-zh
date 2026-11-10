# 切片流水线

`orca.slicing` 模块为在切片流水线的某些节点，或在导出 G-code 后处理环节运行的插件提供 `SlicingPipelineCapabilityBase`。

| 基类 | `get_type()` 返回 | 必需的方法 | 调用者 |
|---|---|---|---|
| `orca.slicing.SlicingPipelineCapabilityBase` | `SlicingPipeline` | `get_name()`、`execute(self, ctx) -> ExecutionResult` | 切片流水线和 G-code 导出路径 |

## 上下文

{{C1}}

在几何处理步骤中，`ctx.print` 以及（对于对象级步骤）`ctx.object` 提供实时的切片图。这些引用只在 `execute(ctx)` 期间有效。`ctx.step` 标识当前的钩子，`ctx.config_value(key)` 读取解析后的打印设置。

在 `orca.slicing.Step.psGCodePostProcess` 时，`ctx.print` 和 `ctx.object` 为 `None`。上下文提供 `gcode_path`、`host` 和 `output_name`；插件直接就地编辑工作中的 G-code 文件。这一步在传统的后处理脚本之后运行，并且可能会针对文件导出和网络上传分别运行。

该功能在切片工作线程上运行。不要在其中调用 `orca.host.ui.*`：GUI 可能正在等待切片完成，此时把 UI 调用调度到主线程可能导致死锁。请通过日志或执行结果报告结果。

## 流水线步骤

公开的 `orca.slicing.Step` 枚举包括 `posSlice`、`posPerimeters`、`posPrepareInfill`、`posInfill`、`posIroning`、`posContouring`、`posSupportMaterial` 和 `posSimplifyPath` 等几何处理步骤，以及生成结构的步骤 `psWipeTower` 和 `psSkirtBrim`。`psGCodePostProcess` 步骤就是上面所说的导出环节。

> [!IMPORTANT]
> 流水线插件可以修改实时的切片图，并影响生成的输出。文件系统访问会受到审计：在 `psGCodePostProcess` 时写入 G-code 文件不需要提示，因为在该调用期间，它所在的文件夹是预先批准的允许根目录。其他任何文件系统/网络/进程操作在第一次发生时都会用"是/否"对话框提示用户，并为该插件记住答复。参见[插件审计钩子]({{L1}})。

关于注册请参见[注册]({{L2}})，关于模型和几何绑定请参见[宿主]({{L3}})。
