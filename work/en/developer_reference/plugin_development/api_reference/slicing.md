# Slicing Pipeline

The `orca.slicing` module exposes `SlicingPipelineCapabilityBase` for plugins that run at points
in the slicing pipeline or at the exported-G-code post-processing seam.

| Base class | `get_type()` returns | Required methods | Invoked by |
|---|---|---|---|
| `orca.slicing.SlicingPipelineCapabilityBase` | `SlicingPipeline` | `get_name()`, `execute(self, ctx) -> ExecutionResult` | the slicing pipeline and G-code export path |

## Context

{{C1}}

During geometry steps, `ctx.print` and (for object-scoped steps) `ctx.object` expose the live
slicing graph. These references are valid only during `execute(ctx)`. `ctx.step` identifies the
current hook, and `ctx.config_value(key)` reads a resolved print setting.

At `orca.slicing.Step.psGCodePostProcess`, `ctx.print` and `ctx.object` are `None`. The context
provides `gcode_path`, `host`, and `output_name`; the plugin edits the working G-code file in place.
This step runs after classic post-processing scripts and may run separately for file export and
network upload.

The capability runs on the slicing worker thread. Do not call `orca.host.ui.*` from it: the GUI
may be waiting for slicing to finish, so marshaling a UI call can deadlock. Use the log or the
execution result to report outcomes.

## Pipeline steps

The exposed `orca.slicing.Step` enum includes geometry steps such as `posSlice`, `posPerimeters`,
`posPrepareInfill`, `posInfill`, `posIroning`, `posContouring`, `posSupportMaterial`, and
`posSimplifyPath`, plus generated-structure steps `psWipeTower` and `psSkirtBrim`. The
`psGCodePostProcess` step is the export seam described above.

> [!IMPORTANT]
> Pipeline plugins can mutate the live slicing graph and affect generated output. Filesystem
> access is audited: writing to the G-code file at `psGCodePostProcess` needs no prompt, since
> its folder is a pre-approved allowed root for the duration of that call. Any other
> filesystem/network/process action prompts the user with a Yes/No dialog the first time, and
> the answer is remembered for that plugin. See [Plugin Audit Hook]({{L1}}).

See [Registry]({{L2}}) for registration and [Host]({{L3}}) for the model and geometry bindings.
