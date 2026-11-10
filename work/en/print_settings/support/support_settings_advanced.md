# Support Advanced

{{T1}}

## Z distance

{{M1}}
The Z gap between the support and the object: **Top Z distance** is the gap between the top of the support and the overhang above it, and **Bottom Z distance** the gap between the object and a support standing on it. Both are rounded to a multiple of the layer height unless [Independent support layer height]({{L1}}) is enabled.

A Top Z distance of `0` is meant for soluble supports. In that case, Bottom Z distance is also ignored when there are bottom interface layers, and the support is printed in direct contact with the object.

## Support wall loops

{{M2}}
This setting specifies the number of support walls, from 0 to 2. 0 means auto.

## Base Pattern

{{M3}}
Line pattern for the base of the support.

`Default` depends on the support type: normal supports use `Rectilinear`, and tree supports are left `Hollow`, with only the branch walls printed. With the [Tree Hybrid]({{L2}}) style, `Default` fills the parts printed as normal support with `Rectilinear` and leaves the branches hollow, while choosing `Rectilinear` fills the branches too.

### Base pattern spacing

{{M4}}
Spacing between support lines.

## Pattern angle

{{M5}}
Use this setting to rotate the support pattern on the horizontal plane.

## Interface layers

{{M6}}
The number of interface layers.

The number you set is the total thickness of the dense interface, counted in printed layers and including the layer that faces the model. Set `1` and you get a single dense layer; set `3` and you get three. More layers give a flatter, better supported surface but take longer to print and are harder to peel off.

The top and bottom interfaces are set separately:

- **Top interface layers** (`support_interface_top_layers`) are the layers printed under an overhang, below the [Z distance]({{L3}}) gap. These are the ones that determine the finish of the supported surface.
- **Bottom interface layers** (`support_interface_bottom_layers`) are the layers printed where a support lands on top of the model, protecting that surface from the support body. `Same as top` reuses the top value. You can use bottom interfaces on their own, with top interface layers set to `0`.

With both set to `0` there is no interface at all: the support prints all the way through with the [Base Pattern]({{L4}}), which is fastest and easiest to remove but leaves the roughest overhangs.

> [!TIP]
> When the interface has its own filament assigned, this number also decides how the layers are shared between the two materials. See [Interface filament transitions]({{L5}}).

## Interface pattern

{{M7}}
The pattern used for the support interface.

Each option lays the interface lines out differently, and all of them are measured from [Pattern angle]({{L6}}), so rotating that rotates the interface with it. The same rules apply to normal and tree supports.

| Option | What you get |
| --- | --- |
| `Default` | Straight lines crossing the support at 90° to Pattern angle. Switches to concentric loops when the interface touches the model, which is the usual case for soluble supports. |
| `Rectilinear` | Straight lines at 90° to Pattern angle. With the [Snug]({{L7}}) style they are rotated a further 45°. |
| `Concentric` | Loops following the outline of the interface, which peel off in one piece and leave no line ends on the surface. |
| `Spiral Inset` | Like `Concentric`, but the loops are joined into a continuous [spiral]({{L8}}), so the nozzle steps from one ring to the next without stopping. |
| `Rectilinear Interlaced` | Straight lines that swing 45° one way then the other on each successive layer, so the layers cross instead of stacking. This ties the interface together and makes it stiffer under the overhang. |
| `Grid` | Straight lines crossing in a grid on every layer: one set runs along Pattern angle, in line with the [Base Pattern]({{L9}}) below, and the other at 90° to it. |

If [Interface spacing]({{L10}}) is wide enough that the interface is no longer solid, `Default` and `Rectilinear` switch to the base support pattern so that the sparse lines still anchor to each other.

## Interface spacing

{{M8}}
Spacing of interface lines. Zero means solid interface.

The top (`support_interface_spacing`) and bottom (`support_bottom_interface_spacing`) values are set separately and neither one affects the other, so a bottom interface keeps the spacing you gave it even if you have turned top interfaces off.

When [Support ironing]({{L11}}) is enabled, the top interface is always printed solid and the top value is ignored.

## Normal support expansion

{{M9}}
Expand (+) or shrink (-) the horizontal span of normal support.

## Support/object XY distance

{{M10}}
XY separation between an object and its support.

## Support/object first layer gap

{{M11}}
XY separation between an object and its support at the first layer.

## Don't support bridges

{{M12}}
Don't support bridge areas, which would otherwise make the support very large. Bridges can usually be printed directly without support if they are not very long.

This option is only shown for normal supports. Tree supports use [Max bridge length]({{L12}}) instead.

## Max bridge length

{{M13}}
The longest bridge that tree supports leave unsupported. It replaces [Don't support bridges]({{L13}}) for every tree style, including Organic. Bridges up to this length that are anchored at both ends are printed without support, and longer ones are supported along their whole length. `0` supports all bridges, and a very large value leaves every bridge unsupported.

With the Tree Slim, Tree Strong and Tree Hybrid styles, the branch tips placed inside an overhang are also spaced at least half this length apart, so a value above twice [Branch Distance]({{L14}}) spreads them further apart.

## Independent support layer height

{{M14}}
Support layers use a layer height independent of the object layers. This allows a custom Z gap and saves print time. This option is ignored when a prime tower is printed, and it is not available with the Organic tree support style.

Turning this on changes the height of the support layers, not their number: you still get exactly the [Interface layers]({{L15}}) you asked for, including with the `Tree Slim`, `Tree Strong` and `Tree Hybrid` styles.
