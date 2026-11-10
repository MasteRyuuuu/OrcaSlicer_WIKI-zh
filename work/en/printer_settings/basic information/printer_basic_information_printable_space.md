# Printable Space

This section defines the printer’s physical build area and how the slicer maps models to it. Configure the bed shape, dimensions and origin so the virtual bed matches your machine; use a circular or rectangular profile for standard beds or supply an STL for custom shapes. Add a texture or model to improve visual alignment in the 3D view.

Specify any excluded (unprintable) regions as a polygon so the arranger avoids them, and any obstacles the toolhead must not hit as collision volumes. Set the printable height to your maximum Z travel, and use Z offset to correct endstop inaccuracies (this value is added to every Z coordinate in exported G‑code). The best object position is a normalized [0–1] preference used by automatic arranging, and preferred orientation controls automatic Z-axis alignment on import.

{{T1}}

## Printable area (Bed Shape)

Defines the printable area on the print bed.

### Shape

Shape of the printable area on the print bed.

- Rectangular: Standard rectangular print bed.
- Circular: Circular print bed.
- Custom: Custom shape defined by STL file.

### Settings

- Size: Size in X and Y of the rectangular plate.
- Origin: Distance of the 0,0 G-code coordinate from the front left corner of the rectangle.

### Texture

SVG or PNG texture image file to be used as a background for the print bed in the 3D view.

### Model

STL file defining the custom shape of the print bed.

## Excluded bed area

{{M1}}
Unprintable area in XY plane. For example, X1 Series printers use the front left corner to cut filament during filament change. The area is expressed as polygon by points in following format: "XxY, XxY, ..."  
It keeps models and printed material out of the area, but the toolhead can still travel through it, as the X1 does to cut the filament. To also keep the toolhead's moves out, set [Toolhead collision volumes]({{L1}}).

## Toolhead collision volumes

{{M2}}

Obstacles the toolhead must not hit, such as bed clips, a tool dock, a camera arm or parts of the gantry. Each one is a polygon on the bed that can cover the full printable height or only a range of Z, so a low clip only blocks the first millimeters.

Unlike the [Excluded bed area]({{L2}}), which only keeps material out, collision volumes are also kept clear by the toolhead's moves:

- **Models:** an object that enters a volume, at any height where both exist, is reported as an error. It is checked for every nozzle it prints with.
- **Generated material:** brims and supports are cut back so they don't print inside a volume.
- **Travel:** travel moves are routed around the volumes.
- **G-code check:** after slicing, every move in the final G-code is checked again, and a warning is shown for any move that crosses a volume.

The field is empty by default, and nothing changes until a volume is entered. Collision volumes are added to the Excluded bed area, so a printer can keep its filament cutter area and add collision volumes elsewhere.

### Volume format

Coordinates are in millimeters on the bed, as in the [Excluded bed area]({{L3}}).

- `XxY, XxY, ...` is a polygon that covers the full [Printable height]({{L4}}).
- `ZMIN..ZMAX;XxY, XxY, ...` is a polygon that only covers the heights from ZMIN to ZMAX. Either one can be left out: `..10;` covers from the bed up to 10 mm, and `30..;` from 30 mm up to the printable height.
- `|` separates volumes.

For example, a full-height volume in the front left corner and a second one from 8 to 22 mm:

{{C1}}

Z ranges are limited to the Printable height. An invalid definition is reported as an error.

> [!TIP]
> If you paste a definition in this format into the [Excluded bed area]({{L5}}), Orca offers to add it to the collision volumes instead. The Excluded bed area keeps its previous value.

[Arrange]({{L6}}) uses the bounding box of a non-convex volume, so it may keep objects further away than needed.

### Collision volume behavior

Only shown for printers with more than one extruder. Sets how the volumes apply to each nozzle:

- **Shared by all nozzles:** every nozzle uses the same volumes. This is the default.
- **Toolhead-relative (nozzle offsets):** the volumes are entered once, as seen from the main nozzle (usually the first), and each other nozzle uses them shifted by the difference between its [Extruder offset]({{L7}}) and the main nozzle's. Every extruder must have an offset. The Excluded bed area isn't shifted.
- **Individual per extruder:** hides the Toolhead collision volumes field and shows [Extruder collision volumes]({{L8}}) on each extruder's page instead. When this mode is selected and no extruder has volumes yet, the shared volumes are copied to every extruder.

### Extruder collision volumes

The collision volumes of one extruder, in the **Individual per extruder** behavior. Set them in each extruder's page of the printer settings, with the same [format]({{L9}}) as the shared volumes. Leave it empty for an extruder with no collision volumes.

Volumes follow the physical extruder that prints, not the filament.

### Preview

The footprint of each volume is shown on the bed. Volumes that apply only to some nozzles have a thin border in the color of their nozzle.

**View > Show all collision volumes** (`Ctrl + Shift + K` by default, see [Keyboard Shortcuts]({{L10}})) shows every volume over its full height, even on an empty bed. It only changes the display, not the slicing or the G-code check, and is remembered across printers.

### Limitations

> [!WARNING]
> Collision volumes reduce the risk of a collision, but don't guarantee safe G-code. A warning from the G-code check doesn't fix the move; check the G-code before printing.

- **Firmware macros:** moves made inside a macro called from the G-code (e.g. `PRINT_START` on Klipper) can't be seen or checked.
- **Homing:** after a homing command, the homed axes are unknown until the G-code moves to an explicit position. A move with an unknown Z is checked against every height.
- **Extrusion:** only travel moves are rerouted. Extrusions aren't, and [skirts and draft shields]({{L11}}) aren't rebuilt around the volumes.
- **Spiral Z-hop:** the circle a [Spiral Z-hop]({{L12}}) draws isn't taken into account when the travel is routed.

## Printable height

{{M3}}
This is the maximum printable height which is limited by the height of the build area.

## Support multi bed types

{{M4}}
Once enabled, you can select the bed type in the drop-down menu, corresponding bed temperature will be set automatically.

{{I1}}

This also enabled you to set each bed type in the [filament settings]({{L13}}).

{{I2}}

Orca also support `curr_bed_type` variable in custom G-code.
For example, the following sample G-codes can detect the selected bed type and adjust the G-code offset accordingly for Klipper:

{{C2}}

Available bed types are:

- Smooth Cool Plate
- Smooth High Temp Plate
- Textured Cool Plate
- Textured PEI Plate
- Engineering Plate
- Cool Plate (SuperTack)

## Best object position

{{M5}}
Best auto arranging position in range [0,1] w.r.t. bed shape.

## Z offset

{{M6}}
This value will be added (or subtracted) from all the Z coordinates in the output G-code. It is used to compensate for bad Z endstop position: for example, if your endstop zero actually leaves the nozzle 0.3mm far from the print bed, set this to -0.3 (or fix your endstop).

## Preferred orientation

{{M7}}
Automatically orient STL files on the Z axis upon initial import.
