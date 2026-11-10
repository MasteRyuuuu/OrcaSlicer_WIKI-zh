# Motion Ability

Settings related to the motion capabilities of the printer.

{{T1}}

## Emit limits to G-code

{{M1}}
If enabled, the machine limits will be emitted to G-code file.
This option will be ignored if the G-code flavor is set to Klipper.

## Resonance Compensation

Resonance Compensations are the methods used to reduce the vibrations of the printer during high-speed movements, which can cause ringing on the surface of the model.

### Resonance Avoidance

{{M2}}
By reducing the speed of the outer wall to avoid the resonance zone of the printer, ringing on the surface of the model are avoided.

> [!TIP]
> Check the [VFA Calibration]({{L1}}).

### Input Shaping

{{M3}}
During high-speed movements, vibrations can cause a phenomenon called "ringing," where periodic ripples appear on the print surface. Input Shaping provides an effective solution by counteracting these vibrations, improving print quality and reducing wear on components without needing to significantly lower print speeds.

> [!NOTE]
> Some Printers have built-in accelerometers that can be used to **automatically** measure the resonant frequencies of the printer.  
> If your printer has one, consider using it as it can provide more accurate results in less time and usually is autosaved into the printer firmware.

> [!TIP]
> It's usually recommended to perform [Input Shaping calibration]({{L2}}) once a year or after any mechanical or structural changes such as relocation, changing the support surface, new belts, motors, frame, etc.

> [!IMPORTANT]
> **RepRap** can only set one frequency for both X and Y axes so you will need to select a frequency that works well for both axes.

{{I1}}

#### Input Shaping Type

{{M4}}
The Input Shaping type determines the algorithm used to counteract the vibrations.  
It is usually recommended to use MZV, EI (specially for Delta printers) or ZV as a simple and effective solution.  
Not all Input Shaping types are available in all firmware and their performance may vary depending on the firmware implementation and the printer's mechanics.

##### Default

When "Default" is selected, the firmware's default input shaper will be used.  
Every firmware and even its version may have a different default type but usually are:

- Klipper: MZV
- Marlin: ZV
- RepRap:
    - Version >= 3.4: MZV
    - Version < 3.4: DAA
    - Version < 3.2: DAA (without damping option)

##### Version Table

| Type | Name | [Klipper]({{L3}}) | [RepRap]({{L4}}) | [Marlin 2]({{L5}}) |
| --- | --- | --- | --- | --- |
| MZV | Modified Zero Vibration | >=0.9.0 | >=3.4 | - |
| ZV | Zero Vibration | >=0.9.0 | = 3.5 | >2.1.2 |
| ZVD | Zero Vibration Derivative | >=0.9.0 | >=3.4 | - |
| ZVDD | Zero Vibration Double Derivative | - | >=3.4 | - |
| ZVDDD | Zero Vibration Triple Derivative | - | >=3.4 | - |
| EI | Extra Insensitive | >=0.9.0 | - | - |
| 2HUMP_EI / EI2 | Two-Hump Extra Insensitive | >=0.9.0 | >=3.4 | - |
| 3HUMP_EI / EI3 | Three-Hump Extra Insensitive | >=0.9.0 | >=3.4 | - |
| [FT_MOTION]({{L6}}) | Fixed-Time Motion | - | - | >2.1.3 |
| DAA | Damped Anti-Resonance | - | < 3.4 | - |

###### Fixed-Time Motion

TODO: This calibration test is currently under development. See the [Marlin documentation]({{L7}}) for more information.

## Speed limitation

Safeguard maximum speeds for all axes.
This will cap the speed set by the process if it exceeds these values.

## Acceleration limitation

{{M5}}
`Simple` [Variables]({{L8}}): `machine_max_acceleration_x`, `machine_max_acceleration_y`, `machine_max_acceleration_z`, `machine_max_acceleration_e`, `machine_max_acceleration_extruding`, `machine_max_acceleration_retracting`.  
`Advanced` [Variable]({{L9}}): `machine_max_acceleration_travel`.  
{{M6}}
Safeguard maximum accelerations for all axes.
This will cap the acceleration set by the process if it exceeds these values.

## Jerk limitation

Safeguard maximum jerks for all axes.

> [!TIP]
> Check the [Cornering Calibration]({{L10}}).

### Maximum Jerk

{{M7}}
Maximum [jerk]({{L11}}) for each axis (M205 X, Y, Z, E, only apply if JD = 0 for Marlin 2 Firmware)

### Maximum Junction Deviation

{{M8}}
Maximum [junction deviation]({{L12}}) (M205 J, only apply if JD > 0 for Marlin Firmware. If your Marlin 2 printer uses Classic Jerk set this value to 0.)
