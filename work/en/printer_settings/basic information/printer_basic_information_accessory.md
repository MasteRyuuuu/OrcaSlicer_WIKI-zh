# Printer Accessory

{{T1}}

## Nozzle type

{{M1}}
The metallic material of the nozzle: This determines the abrasive resistance of the nozzle and what kind of filament can be printed.

## Nozzle HRC

{{M2}}
The Nozzle Hardness ([Hardness Rockwell C]({{L1}})) value is used in OrcaSlicer to validate nozzle compatibility with abrasive filaments and prevent nozzle damage during printing.

| Material          | Value |
|-------------------|-------|
| Disable Check     | 0     |
| Brass             | 2     |
| Stainless Steel   | 20    |
| Hardened Steel    | 55    |
| Tungsten Carbide  | 85    |

## Auxiliary Part Cooling Fan

{{M3}}
Enable this option if machine has auxiliary part cooling fan.  
The speed will be set for each material in the [material cooling settings]({{L2}}).

G-code command:

{{C1}}

### Auxiliary Fan

OrcaSlicer uses `M106 P#` (Set Fan Speed) / `M107 P#` (Fan Off) to control any fans managed by the slicer.
The `P` parameter indicates the fan index as defined by OrcaSlicer:

- `P0`: part cooling fan (default layer fan)
- `P1` (if present): an additional fan
- `P2`: often used as Aux / CPAP / Booster
- `P3` (and higher): sometimes Exhaust / Enclosure, etc.

With Klipper you can create macros that translate both the OrcaSlicer numeric fan index `P` and **human‑readable names** for your physical fans. This keeps compatibility with generated G‑code (M106 P0 / M106 P2 …) while letting you address fans by name internally.

> [!WARNING]
> Adjust pin names and parameters (power, cycle_time, etc.) to match your hardware.

{{T2}}

#### Simple option (indexes only → fan0, fan2, fan3)

This is the original basic example where the `P` index is concatenated (`fan0`, `fan2`, `fan3`). Use it if you don't need custom names:

{{C2}}

#### Advanced option (Index ⇄ Name mapping)

Lets you use descriptive names like `CPAP`, `EXHAUST`, etc. Useful if you re‑wire or repurpose fans without changing slicer output. Just keep `fan_map` updated.

{{C3}}

##### Quick customization

1. Add / remove entries in `fan_map` to reflect the indexes the slicer may use.
2. Keep comments like `# fan X OrcaSlicer` next to each `[fan_generic]` for easy correlation.
3. Tune `max_power`, `off_below`, `cycle_time` according to fan type (CPAP blower vs axial exhaust).

##### Usage

- From OrcaSlicer: `M106 P0 S255` (100% CPAP), `M106 P3 S128` (~50% EXHAUST).
- Turn one off: `M107 P3`. Turn all off: `M107`.
- You can still manually use `SET_FAN_SPEED FAN=CPAP SPEED=0.7` in the Klipper console.

---

Pick the variant that best fits your workflow; the advanced version provides extra clarity and flexibility while remaining fully compatible with standard OrcaSlicer G-code output.

## Support controlling chamber temperature

{{M4}}
OrcaSlicer use `M141/M191` command to control active chamber heater.

If your Filament's [Activate temperature control]({{L3}}) and your printer `Support control chamber temperature` option are checked , OrcaSlicer will insert `M191` command at the beginning of the gcode (before `Machine G-code`).

{{I1}}
{{I2}}

> [!NOTE]
> If the machine is equipped with an auxiliary fan, OrcaSlicer will automatically activate the fan during the heating period to help circulate air in the chamber.

### Using Chamber Temperature Variables in Machine G-code

You can use chamber temperature variables in your `Machine G-code` to control the chamber temperature manually, if desired:

- To set the chamber temperature to the value specified for the first filament:

  {{C4}}

- To set the chamber temperature to the highest value specified across all filaments:

  {{C5}}

### Klipper Chamber Temperature

If you are using Klipper, you can define these macros to control the active chamber heater.
Bellow is a reference configuration for Klipper.

> [!IMPORTANT]
> Don't forget to change the pin name/values to the actual values you are using in the configuration.

{{C6}}

## Support air filtration

{{M5}}
Air Filtration/Exhaust Fan Control in OrcaSlicer.  
OrcaSlicer use `M106 P3` command to control air-filtration/exhaust fan.

If you are using Klipper, you can define a `M106` macro to control both the normal part cooling fan, auxiliary fan, and exhaust fan.

Below is a reference configuration for Klipper.

> [!NOTE]
> Don't forget to change the pin name to the actual pin name you are using in the configuration.

{{C7}}
