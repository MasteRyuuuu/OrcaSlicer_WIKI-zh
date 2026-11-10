# Overhang Speed

{{T1}}

## Slow down for overhang

{{M1}}
Enable this option to slow printing down for different overhang degrees.
This can help improve print quality and reduce issues like sagging.

### Slow down for curled perimeters

{{M2}}
Enable this option to slow down printing in areas where perimeters may have curled upwards.  
For example, additional slowdown will be applied when printing overhangs on sharp corners like the front of the Benchy hull, reducing curling which compounds over multiple layers.

{{I1}}

It is generally recommended to have this option switched on unless your printer cooling is powerful enough or the print speed is slow enough that perimeter curling does not happen.  
If printing with a high external perimeter speed, this parameter may introduce wall artifacts when slowing down, due to the potentially large variance in print speeds causing the extruder to be unable to keep up with the requested flow change.  
Root cause of these artifacts is most likely PA tuning being slightly off, especially when combined with a high PA smooth time.

> [!TIP]
> When enabling this option:
>
> 1. For Klipper machines: Reduce Pressure Advance smooth time to 0.015 - 0.02 so the extruder reacts quickly to the speed changes.
> 2. Increase the minimum print speeds to limit the magnitude of the slowdown and reduce the variance between fast and slow segments.
> 3. If artifacts still appear, enable [Extrusion rate smoothing]({{L1}}) to further smooth the flow transitions.

> [!NOTE]
> When this option is enabled, overhang perimeters are treated like overhangs, meaning the overhang speed is applied even if the overhanging perimeter is part of a bridge.  
> For example, when the perimeters are 100% overhanging, with no wall supporting them from underneath, the 75% [overhang speed]({{L2}}) will be applied, capped at the external [bridge speed]({{L3}}).

### Speed

{{M3}}
This is the speed for various overhang degrees. Overhang degrees are expressed as a percentage of [line width]({{L4}}).  
If expressed as a percentage, the speed is calculated from the [outer wall speed]({{L5}}) for outer walls and from the [inner wall speed]({{L6}}) for inner walls.

> [!NOTE]
> 0 speed means no slowing down for the overhang degree range and wall speed is used.

## Bridge speed

Set speed for external and internal bridges.  
It's usually recommended to increase internal bridge speed to reduce print time, while external bridge speed should be reduced to improve print quality.  
The internal bridge speed can be set in mm/s or as a percentage of the external bridge speed (default 150%).

When [Slow down for overhang]({{L7}}) is enabled and [Slow down for curled perimeters]({{L8}}) is disabled, the external bridge speed also applies to overhang walls supported by less than 13% of their line width: their speed blends from the 75% [overhang speed]({{L9}}) to the external bridge speed as the support drops to 0%.
