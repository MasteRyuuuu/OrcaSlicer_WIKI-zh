# CLI Mode

OrcaSlicer can run headless from the command line to load, transform, and slice models without opening the GUI. This is useful for automation, batch processing, and CI pipelines.

{{T1}}

## Invocation

{{C1}}

Any argument that doesn't start with `-` is treated as an input file (model or project) to load, in the order given. Supported input formats are the same ones listed under [Supported File Formats]({{L1}}).

Use `--` on its own to stop OrcaSlicer from parsing any further arguments as flags — everything after it is treated as a positional input file, even if it starts with a dash.

## Flag Syntax

### Boolean flags

Flags backed by a plain on/off setting (e.g. `--info`, `--export-stl`) don't need a value — including the flag alone enables it. An explicit `=1` / `=0` is also accepted to force it on or off. See [Boolean]({{L2}}) for the full rules, including a space-separated `--flag 0` gotcha that does *not* do what it looks like it does.

### Value flags

Flags backed by a single value accept it either as a separate argument or with `=`:

{{C2}}

> [!IMPORTANT]
> Every setting's key (as shown on its wiki page, e.g. `layer_height`) uses underscores. On the command line, OrcaSlicer always converts underscores to hyphens to build the flag name — so `layer_height` becomes `--layer-height`. This applies uniformly: all ~50 CLI-only options and every regular print, filament, and printer setting alike. Always write CLI flags with hyphens, never the raw underscore key.

### Vector (multi-value) flags

Some settings hold one value per extruder, filament, or object (e.g. `retraction_length[extruder_idx]`). These take a **comma-separated list**, where position in the list = index (0-based):

{{C3}}

Two behaviors to know before using these:

- **Padding.** If you supply fewer values than there are entries (extruders, filaments, etc.), the missing slots are filled by repeating the *first* value you gave — not each entry's own default. `--retraction-length=1.2` on a 4-extruder printer becomes `[1.2, 1.2, 1.2, 1.2]`; `--retraction-length=0.9,0.8,1.2` on 4 extruders becomes `[0.9, 0.8, 1.2, 0.9]` (index 3 silently gets 0.9, the first value, not its default).
- **Repetition appends, not overwrites.** Passing the same vector flag more than once appends to the list instead of replacing it: `--retraction-length=0.8 --retraction-length=1.2` results in `[0.8, 1.2]`, not `[1.2]`. To fully replace a vector's contents, pass the whole list in a single flag occurrence.

## Setting Overrides

Beyond the CLI-only options documented on this wiki (see [Reference Pages]({{L3}}) below), `--key=value` accepts almost any print, filament, or printer/machine setting documented under [Printer Settings]({{L4}}), [Material Settings]({{L5}}), and [Process Settings]({{L6}}) — the same settings shown in the GUI's Printer/Filament/Process tabs. Each option's page shows its key next to a `[Variable]`/`[Variables]` tag; convert underscores to hyphens to get the flag name, following the [Flag Syntax]({{L7}}) rules above for booleans, values, and vectors.

A fixed set of 43 keys are never exposed on the CLI at all. If a `--key=value` override is rejected with `Invalid option`, check it against the list below before assuming it's a typo:

**Preset identity & inheritance** (used when hand-authoring `.json` profiles directly — see [How to Create Profiles]({{L8}})):
`preset_name`, `compatible_printers`, `compatible_printers_condition`, `compatible_prints`, `compatible_prints_condition`, `compatible_machine_expression_group`, `compatible_process_expression_group`, `different_settings_to_system`, `print_compatible_printers`, `default_filament_profile`, `default_print_profile`, `filament_ids`, `filament_vendor`, `inherits`, `inherits_group`, `host_type`, `printer_model`, `printer_variant`, `material_vendor`, `default_sla_material_profile`, `sla_material_settings_id`, `default_sla_print_profile`, `sla_print_settings_id`

**Print host / network connection** (credentials and connection details for sending directly to a networked printer):
`bbl_use_printhost`, `use_3mf`, `printer_agent`, `print_host`, `print_host_webui`, `printhost_apikey`, `flashforge_serial_number`, `printhost_port`, `printhost_cafile`, `printhost_user`, `printhost_password`, `printhost_ssl_ignore_revoke`, `printhost_authorization_type`

**Internal extruder/variant indexing** (bookkeeping OrcaSlicer maintains internally to match extruders across printer/print/filament configs):
`extruder_variant_list`, `printer_extruder_id`, `printer_extruder_variant`, `print_extruder_id`, `print_extruder_variant`, `filament_extruder_variant`, `filament_self_index`

## Reference Pages

CLI-only options are grouped the same way they're grouped in the source (`CLIActionsConfigDef`, `CLITransformConfigDef`, `CLIMiscConfigDef`):

- [Actions]({{L9}}) — what to do with the loaded model(s): export, slice, inspect.
- [Transform]({{L10}}) — arrange, orient, rotate, scale, and other geometry changes applied before slicing.
- [Misc]({{L11}}) — loading settings/filaments, output locations, logging, and metadata.

## Example

{{C4}}

Loads `model.3mf`, applies the given process/printer/filament settings, auto-arranges the plate(s), slices every plate, and exports the result as a 3MF.
