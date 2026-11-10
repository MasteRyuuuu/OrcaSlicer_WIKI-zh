# Raft

{{M1}}
A raft is a platform of support material printed under the object. The object is printed on the raft instead of on the build plate, and the raft is removed after printing.

A raft helps when:

- The material tends to warp or lift at the corners, like ABS, ASA, PC or Nylon.
- The object touches the bed with a small area, thin features or sharp edges that would not stay attached.
- The build plate is uneven or worn: the raft absorbs small height variations before the first object layer.

In exchange, the bottom of the object is rougher, the print takes more time and material, and the raft has to be removed.

> [!TIP]
> If the problem is only adhesion or warping, try a [brim]({{L1}}) first. It is faster, uses less material and keeps the bottom surface clean.

{{T1}}

## How a raft is built

The raft is made by the support generator, so it is printed with the support settings and filaments even when [supports]({{L2}}) are disabled. When supports are enabled, the raft also extends under the supports that stand on the build plate.

From the build plate up, a raft has:

1. **First layer**: with two or more raft layers, printed at the [first layer height]({{L3}}), with the [Initial layer density]({{L4}}), and widened by the [Initial layer expansion]({{L5}}) to stick to the bed. A one-layer raft has only the contact layer, printed at the first layer height with the interface settings described below and without the extra widening of the Initial layer expansion.
2. **Base layers**: sparse layers spaced by the [Base pattern spacing]({{L6}}) and printed with the [base support filament]({{L7}}).
3. **Interface layers**: denser layers that alternate direction, spaced by the [Interface spacing]({{L8}}) and printed with the [interface support filament]({{L9}}). The top one is the contact layer the object sits on.

Above the contact layer comes the [Contact Z distance]({{L10}}) gap, then the first layer of the object.

## Layers

Number of raft layers printed under the object. The object is raised by the height of the raft. `0` disables the raft.

Half of the layers, rounded up, are interface layers, and the rest are base layers. With two or more layers, the first layer counts as a base layer.

| Layers | Base layers | Interface layers |
| --- | --- | --- |
| 1 | 0 | 1 (printed as the first layer) |
| 2 | 1 | 1 |
| 3 | 1 | 2 |
| 4 | 2 | 2 |
| 5 | 2 | 3 |

Except for the first layer, raft layers are printed at least 75% of the nozzle diameter thick, or at the [layer height]({{L11}}) if that is thicker, so the raft is usually thicker than the number of layers times the layer height.

Because the first layer height applies to the raft, the first layer of the object is printed at the normal layer height.

> [!TIP]
> 2 to 4 layers are enough for most prints. Use more layers when the build plate is uneven, or when the material warps strongly.

## Contact Z distance

Vertical gap between the top of the raft and the bottom of the object.

- **Larger gap**: the raft is easier to remove, but the bottom of the object is rougher because its first layer is printed over the gap.
- **Smaller gap**: the bottom surface is smoother, but the raft is harder to remove.

The value is rounded to a multiple of the layer height, unless [Independent support layer height]({{L12}}) is enabled.

> [!NOTE]
> This setting is hidden and ignored when the support top [Z distance]({{L13}}) is `0`, which is meant for soluble supports. The object is then printed directly on the raft without a gap.

## Expansion

Expands every raft layer in the XY plane around the first layer of the object. A wider raft spreads the warping forces over a larger area and gives the object a more stable base, at the cost of more material, longer print time and more space on the build plate.

This setting is shown only when [Layers]({{L14}}) is above `0`.

> [!NOTE]
> The [Tree Slim]({{L15}}), [Tree Strong]({{L16}}) and [Tree Hybrid]({{L17}}) support styles ignore this setting and size the raft with the [Initial layer expansion]({{L18}}) only, so the setting is disabled when one of them is selected.

When the raft has more than one layer, its first layer is widened again by the [Initial layer expansion]({{L19}}), so with the default values it reaches 1.5 mm + 2 mm = 3.5 mm beyond the object.

> [!TIP]
> Rafts of neighboring objects are not merged. When several objects with rafts share a plate, set the [Auto Arrange]({{L20}}) spacing to at least twice the raft's reach, so their rafts do not overlap.

## Interaction with other settings

- **[Elephant foot compensation]({{L21}})** is not applied when a raft is used, because the object is not printed on the build plate.
- **[Support ironing]({{L22}})** can be enabled with a raft, even when supports are disabled, to smooth the top of the raft. Ironing also makes the raft interface layers solid.
- **[Prime tower]({{L23}})**: all objects on the plate must use the same number of raft layers.
- **[Belt printers]({{L24}})** cannot print a raft.
