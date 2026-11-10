# Advanced Printer Settings

Advanced settings related to the printer configuration.

{{T1}}

## Printer structure

{{M1}}
The physical arrangement and components of a printing device.

## G-code flavor

{{M2}}
What kind of G-code the printer is compatible with.

## Skip G-code config block

{{M3}}

Removes the `CONFIG_BLOCK` (the commented-out block listing every resolved slicer setting) from the exported G-code file.

Some printer firmware parsers crash when reading certain lines in this block, most notably Anycubic's go-klipper choking on `; filament_colour_type = 1;1;1;1`. Enabling this option avoids those upload/parsing failures by not writing the block at all.

> [!CAUTION]
> The G-code file will no longer contain the resolved slicer settings, so it can no longer be used to recover the print configuration afterward.

## Pellet Modded Printer

{{M4}}
Enable this option if your printer uses pellets instead of filaments.
Large format printers with print volumes in the order of 1m^3 generally use pellets for printing.
The overall tech is very similar to FDM printing.
It is FDM printing, but instead of filaments, it uses pellets.

The difference here is that where filaments have a filament_diameter that is used to calculate the volume of filament ingested, pellets have a particular flow_coefficient that is empirically devised for that particular pellet.

pellet_flow_coefficient is basically a measure of the packing density of a particular pellet.
Shape, material and density of an individual pellet will determine the packing density and the only thing that matters for 3d printing is how much of that pellet material is extruded by one turn of whatever feeding mehcanism/gear your printer uses. You can emperically derive that for your own pellets for a particular printer model.

We are translating the pellet_flow_coefficient into filament_diameter so that everything works just like it does already with very minor adjustments.

$$
\text{filament\_diameter} = \sqrt{\frac{4}{\text{pellet\_flow\_coefficient} \cdot \pi}}
$$

sqrt just makes the relationship between flow_coefficient and volume linear.

Higher packing density -> more material extruded by single turn -> higher pellet_flow_coefficient -> treated as if a filament of larger diameter is being used. All other calculations remain the same for slicing.

## Use 3rd-party print host

{{M5}}
Not available via CLI — see [Setting Overrides]({{L1}}) for the full list of excluded keys.  
Allow controlling BambuLab's printer through 3rd party print hosts.

## Printer Agent

{{M6}}
Not available via CLI — see [Setting Overrides]({{L2}}) for the full list of excluded keys.  
Select the network agent implementation used to communicate with the printer. The list contains the built-in agents plus any agents registered by loaded [printer agent plugins]({{L3}}). When empty, Bambu Lab printers use `bbl` and all other printers use `orca`.

> [!NOTE]
> Plugin printer agents only receive print jobs when **Preferences → Developer → Experimental Features → Use printer agents instead of print hosts** is enabled.

## Scan first layer

{{M7}}
Enable this to enable the camera on printer to check the quality of first layer.

## Power Loss Recovery

{{M8}}
Enable or Disable power loss recovery by inserting commands in generated G-code.  
Set `Printer configuration` to use the current printer's power loss recovery configuration.

> [!NOTE]
> Only for [Bambu Lab]({{L4}}) or [Marlin 2 firmware]({{L5}}) based printers.

Power loss recovery saves the current execution point to non-volatile memory (SD card) but this can introduce some issues:

- When the slicer generates many short moves (e.g. curves), frequent save/read operations can introduce pauses that may leave blobs.
- Repeated writes also increase wear on the memory device and its Terabytes Written (TBW).

> [!TIP]
> If enabled, it's recommended to enable [Arc fitting]({{L6}}) in `Quality Settings > Precision` to reduce the number of G-code commands.

> [!CAUTION]
> High warping models or materials will not be recovered properly due to bed adhesion loss after power-off.

## Disable set remaining print time

{{M9}}
Disable generating of the M73: Set remaining print time in the final G-code.

## G-code thumbnails

{{M10}}
Picture sizes to be stored into a .gcode and .sl1 / .sl1s files, in the following format: "XxY, XxY, ..."

## Use relative E distances

{{M11}}
Relative extrusion is recommended when using "label_objects" option. Some extruders work better with this option unchecked (absolute extrusion mode). Wipe tower is only compatible with relative mode. It is recommended on most printers. Default is checked.

## Use firmware retraction

{{M12}}
This experimental setting uses G10 and G11 commands to have the firmware handle the retraction. This is only supported in recent Marlin.

## Bed temperature type

{{M13}}
This option determines how the bed temperature is set during slicing: based on the temperature of the first filament or the highest temperature of the printed filaments.

## Time cost

{{M14}}
The printer cost per hour.

## Build plate tilt

{{M15}}

**Build plate tilt X** and **Build plate tilt Y** specify the build surface's tilt in degrees. Support generation uses these values to adjust its gravity direction, so overhangs are evaluated relative to the machine's actual downward direction rather than the slicer's Z axis.

Set both to 0 for a level bed.

On a [belt printer]({{L7}}), these values are derived from the [belt tilt]({{L8}}) each time a print is prepared, overwriting any manual entries. A belt tilt about X sets **Build plate tilt X**, and a belt tilt about Y sets **Build plate tilt Y**.
