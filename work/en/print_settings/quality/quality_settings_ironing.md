# Ironing

Ironing is a process used to improve the surface finish of 3D prints by smoothing out the top layers. This is achieved by printing a second time at the same height, but with a very [low flow rate]({{L1}}) and a specific [pattern]({{L2}}). The result is a smoother surface that can enhance the aesthetic quality of the print at the cost of increased print time.

{{I1}}

> [!TIP]
> For multi-material prints, consider using [Material Setting Overrides]({{L3}}) to customize ironing settings for each material.

> [!IMPORTANT]
> Ironing can cause filament to move very slowly through the hotend, which increases the risk of heat creep and potential clogging. Monitor your printer during ironing and ensure your hotend cooling is adequate to prevent jams.

## Type

{{M1}}
This setting controls which layers are ironed.

- **All top surfaces**: All [top surfaces]({{L4}}) will be ironed. This is the most common setting and is used to smooth out the top layers of the print.  
  {{I2}}
- **Topmost surface only**: Only the last [top layer]({{L5}}) of each object will be ironed. This is useful for prints where only the last layer needs to be smoothed.  
  {{I3}}
- **All solid layers**: All solid layers, including [internal solid infill]({{L6}}) and [top layers]({{L7}}), will be ironed. This can be useful for prints that require a very smooth finish on all solid surfaces but may increase print time significantly.  
    {{I4}}

## Pattern

{{M2}}
The pattern that will be used when ironing. Usually, the best pattern is the one with the most efficient coverage of the surface.  

> [!TIP]
> See [Infill Patterns Wiki List]({{L8}}) with **detailed specifications**, including their strengths and weaknesses.

The ironing patterns are:

- **[Concentric]({{L9}})**
- **[Rectilinear]({{L10}})**

## Flow

{{M3}}
The amount of material to extrude during ironing.  
It is a percentage of the flow of a normal layer height. A lower value will result in a smoother finish but may not cover the surface completely. A higher value may cover the surface better but can lead to over-extrusion or a rougher finish.

A lower layer height may require higher flow due to less volumetric extrusion per distance.

## Line spacing

{{M4}}
The distance between the lines of ironing.  
It's recommended to set this value to be equal to or less than the nozzle diameter for optimal coverage and surface finish.

## Inset

{{M5}}
The distance to keep from the edges, which can help prevent over-extrusion at the edges of the surface being ironed.

{{I5}}

If this value is set to 0, an inset of half the nozzle diameter is used, so the [ironing pattern]({{L11}}) stays slightly inside the outer boundaries of the top surface being ironed.

## Angle Offset

{{M6}}
The angle of ironing lines offset relative to the top surface solid infill direction.  
This option can only be edited when the ironing [Pattern]({{L12}}) is Rectilinear.

Commonly used ironing angle offsets are 0°, 45°, and 90°, each producing a [different surface finish]({{L13}}) which will depend on your printer nozzle.

> [!TIP]
> Enable [Align directions to model]({{L14}}) to make the ironing direction follow the model's orientation on the build plate.

## Fixed Angle

{{M7}}
Use a fixed absolute angle for ironing that is not offset from the top surface infill direction. This results in an ironing finish that does not have alternating line directions and may result in a more uniform surface finish and reduced tiger striping effect when reflecting light.

When enabled, the [Angle Offset]({{L15}}) value is used as the absolute ironing angle. Choose an angle that is well offset from all the affected top surface solid infill directions.

Suggested fixed ironing angles are 0° and 90° if you are using the default solid infill direction of 45°.

This option can only be edited when the ironing [Pattern]({{L16}}) is Rectilinear.

## Speed

See [Speed settings for other layers]({{L17}}) for more information about ironing speed.
