# Wall and surfaces

{{T1}}

## Walls printing order

{{M1}}
Print sequence of the internal (inner) and external (outer) walls.  
The order applies to each side of a wall on its own: the walls around a hole follow it just like the walls around the contour.

> [!NOTE]
> Under an [Outer]({{L1}}), [Outer and Inner]({{L2}}) or [Leading edge only]({{L3}}) brim, the first layer prints its outer walls first whatever this setting, so the brim runs straight on into the outer wall.  
> [Auto]({{L4}}), [Mouse Ears]({{L5}}) and [Painted]({{L6}}) brims may leave the outer walls bare, so they keep this order.

### Inner/Outer

Use Inner/Outer for best overhangs. This is because the overhanging walls can adhere to a neighboring perimeter while printing. However, this option results in slightly reduced surface quality as the external perimeter is deformed by being squashed to the internal perimeter.

{{I1}}

### Inner/Outer/Inner

Use Inner/Outer/Inner for the best external surface finish and dimensional accuracy as the external wall is printed undisturbed from an internal perimeter. However, overhang performance will reduce as there is no internal perimeter to print the external wall against. This option requires a minimum of 3 walls to be effective as it prints the internal walls from the 3rd perimeter onwards first, then the external perimeter and, finally, the first internal perimeter. This option is recommended over the Outer/Inner option in most cases.

{{I2}}

- The first layer is printed [Inner/Outer]({{L7}}).
- Where a side has fewer than 3 walls there is nothing to print first, so that side is printed [Outer/Inner]({{L8}}).
- A wall too narrow for an inner wall on each side prints the hole first, see [Narrow walls]({{L9}}).

### Outer/Inner

Use Outer/Inner for the same external wall quality and dimensional accuracy benefits of [Inner/Outer/Inner]({{L10}}) option. However, the Z seams will appear less consistent as the first extrusion of a new layer starts on a visible surface.

{{I3}}

### Narrow walls

When a wall is too narrow for the walls of both its sides, like the wall of a thin tube, the contour and the hole share the room between them:

- **2 lines**: only the outer walls of the contour and the hole fit, touching each other. The hole's outer wall is printed first so the contour's leans on it, unless the order is [Outer/Inner]({{L11}}).
- **3 lines**: the two outer walls and one line between them. [Arachne]({{L12}}) prints that line as an inner wall shared by both sides, and it follows the wall order like any other inner wall. [Inner/Outer/Inner]({{L13}}) has no 3rd wall to print first, so it prints the hole's outer wall, then the contour's, then the line between them.

For example, a tube with 0.5mm walls and 3 wall loops, with Arachne:

| Tube wall | Lines | Inner/Outer | Outer/Inner | Inner/Outer/Inner, after the first layer |
| --- | --- | --- | --- | --- |
| 1mm | 2 | hole, contour | contour, hole | hole, contour |
| 1.5mm | 3 | middle, contour, hole | contour, hole, middle | hole, contour, middle |
| 2mm | 4 | each side inner, outer | each side outer, inner | each side outer, inner |

[Classic]({{L14}}) fills the middle of a 3 line wall with [gap fill]({{L15}}) instead, printed after both outer walls, which keep the 2 line order.

### Print infill first

{{M2}}
When this option is enabled, the [infill]({{L16}}) and [top/bottom shells]({{L17}}) are printed first, followed by the walls. The first layer always prints the walls first, for better bed adhesion. This can be useful for some overhangs where the infill can support the walls.

{{I4}}

**However**, the infill will slightly push out the printed walls where it is attached to them, resulting in a worse external surface finish. It can also cause the infill to shine through the external surfaces of the part.

{{I5}}

When using this option, it is recommended to use the [Precise Wall]({{L18}}), [Inner/Outer/Inner]({{L19}}) wall printing order or reduce [Infill/Wall Overlap]({{L20}}) to avoid the infill pushing out the external wall.

## Wall loop direction

{{M3}}
The direction in which the **contour** wall loops are extruded when looking down from the top.  
Holes are printed in the opposite direction to the contour to maintain alignment with layers whose contour polygons are incomplete and change direction, also partially forming the contour of a hole.
A hole whose outer wall touches the contour's with nothing between them, like a [narrow wall]({{L21}}) 2 lines wide, runs with the contour instead, so both walls are laid side by side in the same direction.
Check [PR 12669]({{L22}}) for more details about reversing hole direction.

The usage of [Reverse on even]({{L23}}) will reverse wall direction based on this setting.

> [!NOTE]
> This option will be disabled if spiral vase mode is enabled.

## Surface flow ratio

{{M4}}
The Flow ratio (`print_flow_ratio`) scales all extrusion flow of the object proportionally.

The top and bottom surface flow ratios affect the amount of material for [top or bottom solid infill]({{L24}}). You can decrease them slightly to get a smoother surface finish.  
The actual top or bottom surface flow used is calculated by multiplying this value by the [filament flow ratio]({{L25}}), and if set, the object's flow ratio.

Other flow ratios, such as ratios for the first layer (does not affect brims and skirts), outer and inner walls, overhang perimeters, sparse infill, internal solid infill, gap fill, support, and support interfaces, can also be adjusted after enabling the "Set other flow ratios" option.

> [!TIP]
> Before using a value other than 1, it is recommended to [calibrate the flow ratio]({{L26}}) to ensure that the flow ratio is set correctly for your printer and filament.

## Only one wall

{{M5}}
Use only one wall on flat surfaces, to give more space to the [top infill pattern]({{L27}}).
Especially useful in small features, like letters, where the top surface is very small and [concentric pattern]({{L28}}) from walls would not cover it properly.

{{I6}}

Each option needs the shell it acts on, so they are only available when the matching [Shell Layers]({{L29}}) is greater than 0: without a top shell there is no top surface for the top option to act on, and the same applies to the first layer and the bottom shell.

> [!TIP]
> See [Surface Expansion and Only One Wall]({{L30}}) for how the inner walls are handled over an expanded top surface when using more than one wall.

### Threshold

{{M6}}
If a top surface has to be printed and it's partially covered by another layer, it won't be considered as a top layer where its width is below this value. This can be useful to keep *Only one wall on top surfaces* from triggering on surfaces that should be covered only by walls.  
This value can be in mm or a % of the inner wall line width.

{{I7}}

> [!WARNING]
> If enabled, artifacts can be created if you have some thin features on the next layer, like letters. Set this setting to 0 to remove these artifacts.

## Avoid crossing walls

{{M7}}
This option instructs the slicer to avoid crossing perimeters (walls) during travel moves.  
Instead of traveling directly through a wall, the print head will detour around it, which can significantly reduce surface defects and stringing.

While this increases print time slightly, the improvement in print quality, especially with materials prone to stringing like **PETG** or **TPU**, often justifies the trade-off.  
Highly recommended for detailed or aesthetic prints.

{{I8}}

### Max detour length

{{M8}}
Defines the maximum distance the printer is allowed to detour to avoid crossing a wall.
Can be set as:

- **Absolute value in millimeters:** exactly how far the detour can extend (e.g., `5mm`).
- **Percentage** of the direct travel path (e.g., `50%`).
- **0** disables the **limit** and allows detours of **any length**.

Use this setting to balance print time and wall quality: longer detours mean fewer wall crossings but slower prints.

## Small area flow compensation

{{M9}}
Enables adaptive flow control for small infill areas.
This feature helps address extrusion problems that often occur in small regions of solid infill, such as the tops of narrow letters or fine features.  
In these cases, standard extrusion flow may be too much for the available space, leading to over-extrusion or poor surface quality.

{{I9}}

It works by dynamically adjusting the extrusion flow based on the length of the extrusion path, ensuring more precise material deposition in small spaces.

The compensation only applies to internal solid infill, top surfaces and first layer bottom surfaces, and only when that surface uses the [Rectilinear]({{L31}}), [Aligned Rectilinear]({{L32}}), [Monotonic]({{L33}}) or [Monotonic line]({{L34}}) pattern.

This is a native implementation of @Alexander-T-Moss's [Small Area Flow Compensation]({{L35}}).

### Flow Compensation Model

The model uses a list of Extrusion Length and Flow Correction Factor value pairs. Each pair defines how much flow should be used for a specific Extrusion Length.  
For values between the listed points, the flow follows a smooth curve through them (PCHIP interpolation), which never overshoots the listed values.

{{I10}}

For example, for the following model:

| Extrusion Length | Flow Correction Factor |
|------------------|------------------------|
| 0                | 0                      |
| 0.2              | 0.4444                 |
| 0.4              | 0.6145                 |
| 0.6              | 0.7059                 |
| 0.8              | 0.7619                 |
| 1.5              | 0.8571                 |
| 2                | 0.8889                 |
| 3                | 0.9231                 |
| 5                | 0.952                  |
| 10               | 1                      |

You should write it as:

{{C1}}
