# Jerk XY

In printer firmware, **Jerk** is the maximum speed change (in mm/s) the printer can make instantly, without accelerating. It controls direction changes and velocity transitions during movement.

{{T1}}

## Key Effects

- **Corner Control**:
    - Lower values = smoother corners, better quality.
    - Higher values = faster cornering, potential artifacts.
- **Print Speed**: Higher jerk reduces deceleration at direction changes, increasing overall speed.
- **Surface Quality**: Lower jerk minimizes vibrations and ringing, especially important for outer walls.

This setting overrides firmware jerk values when different motion types need specific settings. Orca limits jerk to not exceed the Printer's Motion Ability settings.

> [!TIP]
> Jerk can work in conjunction with [Pressure Advance]({{L1}}), [Adaptive Pressure Advance]({{L2}}), and [Input Shaping]({{L3}}) to optimize print quality and speed.  
> It's recommended to follow the [calibration guide]({{L4}}) order for best results.

## Cornering Control Types

- **Jerk**: Traditional method, sets a maximum speed for direction changes.
    - Klipper: [Square corner velocity]({{L5}})
    - RepRapFirmware: [Maximum instantaneous speed changes]({{L6}})
    - Marlin 2: [Classic Jerk]({{L7}}) (deprecated in favor of [Junction Deviation]({{L8}}), but can still be used).
    - Marlin Legacy: [Classic Jerk]({{L9}}).
- **[Junction Deviation]({{L10}})**: Modern method, calculates cornering speed based on acceleration.

> [!TIP]
> Calibrate your cornering values using the [Cornering Calibration guide]({{L11}}).

### Junction Deviation

{{M1}}
Alternative to Jerk, Junction Deviation is the default method for controlling cornering speed in Marlin 2 printers.  
Instead of setting a cornering speed for each line type, it calculates the cornering speed from [each line's acceleration]({{L12}}) and the corner angle. A Junction Deviation equivalent to a given jerk value can be estimated with the formula:

$$
JD = 0.4 \cdot \frac{\text{Jerk}^2}{\text{Accel.}}
$$

Higher values result in faster and more aggressive cornering speeds, while lower values produce smoother, more controlled cornering.

> [!NOTE]
> Classic Jerk can still be used in Marlin 2, but it is deprecated in favor of Junction Deviation.  
> If your printer uses Classic Jerk, set [Maximum Junction Deviation]({{L13}}) to `0` in the printer settings to enable the Jerk settings.

This value is limited by [Printer settings > Motion ability > Maximum Junction Deviation]({{L14}}).

## Default

{{M2}}
Default Jerk value.

> [!NOTE]
> If this value is set to 0, the jerk will be set to the printer's default jerk.

### Outer wall

{{M3}}
Jerk for outer wall printing. This is usually set to a lower value than normal printing to ensure better quality.

### Inner wall

{{M4}}
Jerk for inner wall printing. This is usually set to a moderately higher value than outer wall jerk to improve speed.

### Infill

{{M5}}
Jerk for infill printing. This is usually set to a value higher than inner wall printing to improve speed.

### Top surface

{{M6}}
Jerk for top surface printing. This is usually set to a lower value than infill to ensure better quality.

### Initial layer

{{M7}}
Jerk for initial layer printing. This is usually set to a lower value than top surface to improve adhesion.

### Initial layer travel

{{M8}}
Jerk for initial layer travel.
Using a lower value can improve build plate adhesion. If the value is expressed as a percentage (e.g. 50%), it will be calculated based on the [Travel Jerk]({{L15}}).

### Travel

{{M9}}
Jerk for travel moves. This is usually set to a higher value than infill to reduce travel time.

## Useful links

- [Klipper Kinematics]({{L16}})
- [Marlin Junction Deviation]({{L17}})
- [JD Explained and Visualized, by Paul Wanamaker]({{L18}})
- [Computing JD for Marlin Firmware]({{L19}})
- [Improving GRBL: Cornering Algorithm]({{L20}})
- [Pressure Advance Calibration]({{L21}})
- [Adaptive Pressure Advance]({{L22}})
