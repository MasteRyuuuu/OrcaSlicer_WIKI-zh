# Overhangs

Overhangs are areas of a print that extend outward without full support underneath.  
Low overhang angles can be printed without support, while higher angles may require support, speed reduction, or specific settings to ensure good print quality.

{{T1}}

## Detect overhang wall

{{M1}}
Detects the overhang percentage relative to the line width and uses a different speed to print.
Walls with 100% overhang are printed with the bridge settings.

{{I1}}

## Unsupported wall last

{{M2}}

Wall loops that lie entirely in mid-air, with nothing under them on the layer below, are printed once something can hold them: they are extruded after the walls that anchor them, innermost first, whatever the [walls printing order]({{L1}}) is.

Anchorage spreads outwards, so a loop leaning on a loop that is itself anchored counts as anchored too. What is left over falls into two cases:

- A loop running alongside a supported wall belongs to the same wall stack and keeps its place before the infill, which needs it as an anchor.
- A loop that touches nothing has only the infill to rest on, so it is held back and extruded in a second wall pass after the infill of its layer. This includes loops that only the bridges of the layer can anchor, which wait until those bridges are down.

This works with both the classic and Arachne wall generators, and with either setting of [print infill first]({{L2}}).

> [!NOTE]
> Only available when [Detect overhang wall]({{L3}}) is enabled. If that condition is not met, this setting will be hidden.

## Make overhang printable

{{M3}}
This setting will modify the geometry to print overhangs without support material.  
Every overhang exceeding the [maximum angle]({{L4}}) will be modified to be printable.

### Maximum angle

{{M4}}
Maximum angle of overhangs to allow after making steeper overhangs printable.  
90° will not change the model at all and allow any overhang, while 0 will replace all overhangs with conical material.

{{I2}}

> [!TIP]
> Usually, a value between 45° and 60° works well for most printers and models.

### Hole area

{{M5}}
Maximum area of a hole in the base of the model before it's filled by conical material.  
A value of 0 will fill all the holes in the model base.

## Extra perimeters on overhangs

{{M6}}
Create additional perimeter (overhang wall) paths over steep overhangs and areas where bridges cannot be anchored.

This option only works when [Detect overhang walls]({{L5}}) is enabled, even though it stays visible and editable when that option is off.

{{I3}}

## Reverse on even

{{M7}}
Extrude perimeters that have a part over an overhang in the reverse direction on even layers. This alternating pattern can drastically improve steep overhangs thanks to material squishing direction.

This setting can also help reduce part warping due to the reduction of stresses as they are now distributed in alternating directions. Useful for warp-prone materials, like ABS/ASA, and also for elastic filaments, like TPU and Silk PLA.  
It can also help reduce warping on floating regions over supports.

For this setting to be the most effective, it is recommended to set the [Reverse Threshold]({{L6}}) to 0 so that all walls print in alternating directions on even layers irrespective of their overhang degree.
A disadvantage of this setting is that the outer wall may show a texture due to the alternating extrusion direction.

{{I4}}

### Reverse internal only

{{M8}}
A simple way to reduce the texture on the outer wall is to only reverse the internal walls.
This will still provide almost all of the benefits of alternating extrusion direction on even layers (if using [inner/outer]({{L7}})), but the outer wall will be printed in the same direction, resulting in a smoother surface finish.

### Reverse threshold

{{M9}}
You can set a threshold for the overhang reversal to be considered useful.
Can be set as:

- **0**: Disables the threshold, meaning that all walls will be reversed on even layers.
- **mm**: A fixed distance in millimeters.
- **%**: A percentage of the perimeter width.

When using this setting, the walls will make the reversal texture in the layers where the overhang is above the threshold, and the rest of the walls will be printed in the normal direction.
This could result in uneven texture, sometimes considered worse than the full reversal texture, so it is recommended to use this setting only if you are sure that the overhang reversal will not be useful for your model.

> [!NOTE]
> Only available when:
>
> - [Detect overhang wall]({{L8}}) is enabled
> - [Reverse on even]({{L9}}) is enabled
> - [Reverse internal only]({{L10}}) is disabled
>
> If those conditions are not met, this setting will be hidden.
