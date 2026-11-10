# Multimaterial Advanced

{{T1}}

## Interlocking Beam

{{M1}}
Generates an interlocking beam structure at the locations where different filaments touch. This improves the adhesion between filaments, especially for models printed in different materials.

## Toolchange Ordering

{{M2}}

Determines the order of tool changes on each layer:

- **Default:** starts with the last used extruder to minimize tool changes.
- **Cyclic:** uses a fixed tool sequence each layer. This sacrifices speed for better surface quality, as the extra tool changes allow layers more time to cool.

### Toolchange Order

{{M3}}

Only available when [Toolchange Ordering]({{L1}}) is set to `Cyclic`.

**Cyclic order** sets the filament sequence the cyclic ordering follows, written as filament numbers separated by commas (e.g. `3,2,1,4`). Each layer prints its filaments in that order, and filaments left out of the sequence are printed last, in ascending order. Leave it empty to cycle through all filaments in ascending order.

Entries that cannot be used are dropped and the rest of the sequence still applies:

- Numbers outside the range of your filaments, such as `0` or a number higher than your filament count.
- Repeated numbers, where only the first occurrence counts.
- Anything that is not a plain number, such as `abc` or `2x`.

**Apply cyclic order to first layer** extends that sequence to the first layer as well. It is disabled by default, because the first layer is instead ordered for the best bed adhesion: filaments that print small, fragile first-layer features are printed last, so the following tool changes and travel moves are less likely to knock those weakly anchored parts loose. This adhesion order also honors a custom first layer filament sequence when one is set. The cooling benefit of the cyclic order does not apply to the first layer anyway, since it is printed slowly and hot for adhesion.

> [!TIP]
> Enable it only if you need the exact same tool sequence on every layer, including the first, at the cost of that adhesion optimization.

## Interface Shells

{{M4}}
Forces the generation of solid shells between adjacent materials/volumes. Useful for multi-extruder prints with translucent materials or manual soluble support material.

## Maximum Width of Segmented Region

{{M5}}
Maximum width of a segmented region. Zero disables this feature. Ignored when [Interlocking Beam]({{L2}}) is enabled.

## Interlocking depth of Segmented Region

{{M6}}
Interlocking depth of a segmented region. On every other layer, the painted region reaches only this deep into the model instead of the [Maximum Width of Segmented Region]({{L3}}), so consecutive layers interlock. Zero disables this feature. Hidden and ignored when [Interlocking Beam]({{L4}}) is enabled.

## Interlocking Beam Width

{{M7}}
The width of the interlocking structure beams.

## Interlocking Direction

{{M8}}
Orientation of the interlocking beams.

## Interlocking Beam Layers

{{M9}}
The height of the beams of the interlocking structure, measured in number of layers. Fewer layers are stronger, but more prone to defects.

## Interlocking Depth

{{M10}}
The distance from the boundary between filaments to generate interlocking structure, measured in cells. Too few cells will result in poor adhesion.

## Interlocking Boundary Avoidance

{{M11}}
The distance from the outside of a model where interlocking structures will not be generated, measured in cells.
