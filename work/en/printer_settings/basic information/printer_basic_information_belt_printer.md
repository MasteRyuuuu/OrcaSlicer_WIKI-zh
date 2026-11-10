# Belt Printer

{{I1}}

These settings configure conveyor belt printers and are found in **Printer settings → Basic information → Belt printer**. The group is shown when the settings mode is **Advanced** or higher. The settings below [Enable belt printing]({{L1}}) remain hidden until that option is enabled.

The [Belt Printing]({{L2}}) guide explains how these settings work together. The belt profiles included with OrcaSlicer are configured for a typical 45° machine, so most users only need to check the [Tilt angle]({{L3}}).

{{T1}}

## Enable belt printing

{{M1}}
Enables belt printer mode. The model is rotated by the [belt tilt]({{L4}}) before slicing, and the G-code is transformed for the tilted gantry and moving belt.

Enabling this option also changes how several features behave:

- The [brim]({{L5}}) is printed on the belt, and additional brim options become available.
- Supports end on the belt surface.
- The [belt purge tower]({{L6}}) replaces the prime tower.
- Features that cannot work on a belt are disabled. See [Features that are not available]({{L7}}).

When this option is disabled, belt-specific processing is inactive and the remaining settings on this page are hidden.

## Infinite Y axis

{{M2}}
Removes the build volume limit along Y, allowing a part to extend beyond the plate displayed in Prepare.

The displayed plate size stays the same, but OrcaSlicer ignores the Y boundary when checking whether an object lies outside the printable area. The belt width (X) and the [printable height]({{L8}}) are still enforced.

Disable this option to have OrcaSlicer flag parts that extend beyond the plate along Y.

## Belt tilt

{{M3}}
Defines the tilt of the gantry relative to the belt. The angle and axis control:

- the rotation applied to the model before slicing,
- the [machine-frame tilt]({{L9}}) applied to the G-code,
- the belt surface used to generate supports and the brim,
- the [build plate tilt]({{L10}}) used for support generation,
- the size and position of the [belt purge tower]({{L11}}) and the order in which [Auto arrange]({{L12}}) packs parts.

Every object is rotated about one common origin, so parts at different positions along the belt share the same set of tilted layers and each part prints at its assigned position.

### Tilt angle

{{M4}}
The angle between the belt and the gantry, in degrees. Most belt printers use 45°.

A positive value rotates counter-clockwise when looking down the positive tilt axis. The sign determines the direction in which the layers lean, and the magnitude specifies the physical tilt angle.

> [!NOTE]
> A brim is only generated on a belt printer when the tilt axis is X or Y and the angle is between 1° and 85°.

### Tilt axis

{{M5}}
The axis about which the model is rotated. It is part of the printer's kinematics, so it is only shown when the settings [mode]({{L13}}) is **Developer**; the belt profiles set it once.

{{I2}}

- **X:** The usual layout. The gantry is tilted about X and the belt travels along Y in Prepare.
- **Y:** The gantry is tilted about Y and the belt travels along X in Prepare.
- **Z:** Rotates the model in the plane of the bed. This is not a tilt: no machine-frame transform is applied and no brim is generated.
- **None:** No rotation. The model is sliced as on a flat bed.

## Support floor Z offset

{{M6}}
Shifts the belt surface used for support generation up or down, in mm. A negative value lowers this support floor, preserving more of the support geometry. A positive value raises it.

This is a diagnostic setting. Leave it at 0 unless supports are cut off above the belt or extend below it.

Supports always stop at the belt surface. Under an overhang at the leading end of a part they reach the belt ahead of the part's first contact with it, so the support can start before the part itself.
