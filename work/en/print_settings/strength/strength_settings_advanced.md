# Strength Advanced

{{T1}}

## Align directions to model

{{M1}}
Aligns [infill]({{L1}}), [bridge]({{L2}}), [ironing]({{L3}}) and [top/bottom surface fill]({{L4}}) directions to follow the model's orientation on the build plate.  
When enabled, these directions rotate together with the model so the printed features keep their intended orientation relative to the part, preserving optimal strength and surface characteristics regardless of how the model is placed.

{{I1}}

## Bridge infill direction

{{M2}}
If left to zero, the bridging angle will be calculated automatically for each specific bridge.  
Otherwise the provided angle will be used according to:

- The absolute coordinates
- The absolute coordinates + Model rotation: If [Align directions to model]({{L5}}) is enabled
- The optimal automatic angle + this value: If [Relative Bridge Angle]({{L6}}) is enabled

> [!NOTE]
> Use 180° for zero absolute angle.

## Relative Bridge Angle

{{M3}}
When enabled, the bridge angle values are added to the automatically calculated bridge direction instead of overriding it.  
A small angle (<10°) is recommended to improve bridge coverage in closed shapes.

{{I2}}
{{I3}}
{{I4}}

## Minimum sparse infill threshold

{{M4}}
Sparse infill areas smaller than the threshold value (in mm²) are replaced by [internal solid infill]({{L7}}).
This setting helps to ensure that small areas of sparse infill do not compromise the strength of the print. It is particularly useful for models with intricate designs or small features where sparse infill may not provide sufficient support.

## Infill Combination

{{M5}}
Automatically combine [sparse infill]({{L8}}) of several layers so they print together, reducing print time. Walls are still printed with the original [layer height]({{L9}}).

{{I5}}

### Max layer height

{{M6}}
Maximum layer height for the combined sparse infill.  
Set it to 0 or 100% to use the nozzle diameter (for maximum reduction in print time), or to a value of ~80% to maximize sparse infill strength.

The number of layers over which infill is combined is derived by dividing this value by the layer height and rounding down to a whole number.

Use either absolute mm values (e.g., 0.32mm for a 0.4mm nozzle) or percentages (e.g., 80%). This value must not be larger than the nozzle diameter.

## Detect narrow internal solid infill

{{M7}}
This option auto-detects narrow internal solid infill areas. If enabled, the [concentric pattern]({{L10}}) will be used in those areas to speed up printing. Otherwise, they use the selected [internal solid infill]({{L11}}) pattern (for example, the [rectilinear pattern]({{L12}})).

## Ensure vertical shell thickness

{{M8}}
Add solid infill near sloping surfaces to guarantee the vertical shell thickness (top and bottom solid layers).

- **None**: No solid infill will be added anywhere. **Caution:** Use this option carefully if your model has sloped surfaces.
- **Critical Only**: Avoid adding solid infill for walls.
- **Moderate**: Add solid infill for heavily sloping surfaces only.
- **All (default)**: Add solid infill for all suitable sloping surfaces.
