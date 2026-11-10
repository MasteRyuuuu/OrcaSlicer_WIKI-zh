# Z Contouring

{{M1}}
Z contouring, also called Z-layer anti-aliasing or ZAA, reduces visible stair-stepping on curved and sloped top surfaces by adjusting the Z height of individual extrusion points so the toolpath follows the original model surface more closely.

{{I1}}

Instead of keeping every move at a single flat Z for the whole layer, OrcaSlicer processes eligible top-surface toolpaths and emits varying Z values inside the affected layer.  
This can noticeably smooth domes, chamfers, shallow slopes, and similar top-facing geometry without changing the nominal layer height of the rest of the print.

{{I2}}

> [!NOTE]
> Current implementation targets top-facing curved or sloped surfaces.  
> **Downward-facing or upside-down curves are not handled.**

{{T1}}

## Minimize wall height angle

{{M2}}
Reduce the height of top-surface perimeters so they better match the model edge on slopes steeper than this angle.  
This setting affects both internal and external perimeters.  
Set `0` to disable it.

The default of 35 degrees is a reasonable starting point.

## Minimum z height

{{M3}}
Minimum local layer height allowed for contoured toolpaths. This setting also controls the slicing plane used for contoured layers.

- Lower values allow stronger contouring but leave less minimum layer thickness.
- Higher values move the slicing plane up (it sits this far above the bottom of the layer), and paths are never lowered below it, so walls and top surface infill can drop less. Top surface infill can also rise up to this amount above the nominal layer height, while walls are never raised.

## Don't alternate fill direction

{{M4}}
Keep the fill direction consistent from layer to layer instead of alternating it.  
This can help produce a more consistent surface pattern on curved top surfaces. It only has an effect when Z contouring is enabled for that region.
