# Layer Height

{{M1}}
Layer height defines the vertical thickness of each printed layer, playing a crucial role in both print quality and printing speed.

> [!NOTE]
> You can use a variable layer height with the [Variable Layer Height]({{L1}}) feature.

Using smaller layer heights increases print time but results in:

- Smoother surface finishes
- Less noticeable layer lines
- Enhanced detail on curves
- [Better performance on overhangs]({{L2}})

{{I1}}

{{T1}}

## Quick Reference

| Nozzle Size | Min    | Max    | [First Layer Height]({{L3}}) |
|-------------|--------|--------|-------------------------------------------|
| 0.2mm       | 0.04mm | 0.16mm | 0.12mm                                    |
| 0.3mm       | 0.06mm | 0.24mm | 0.18mm                                    |
| 0.4mm       | 0.08mm | 0.32mm | 0.25mm                                    |
| 0.5mm       | 0.10mm | 0.40mm | 0.30mm                                    |
| 0.6mm       | 0.12mm | 0.48mm | 0.35mm                                    |
| 0.8mm       | 0.16mm | 0.64mm | 0.45mm                                    |
| 1.0mm       | 0.20mm | 0.80mm | 0.55mm                                    |

## Layer Height Guidelines

Usually, the optimal range for layer height is between 20% and 80% of the nozzle diameter.

- **Below 20%:** Flow inconsistencies and "fish scale" patterns may occur, especially at high speeds.
- **Over 80%:** Increased risk of layer adhesion issues and reduced print quality.

## First Layer Height

Controls the thickness of the initial layer.  
A thicker first layer improves bed adhesion and compensates for build surface imperfections.

**Recommended:** 0.25mm for 0.4mm nozzle (62.5% of nozzle diameter)  
**Recommended maximum:** 65% of nozzle diameter

## Layer Height Overhangs Impacts

Layer height directly affects [overhang angle]({{L4}}) capability and quality.

{{I2}}

**Smaller layer heights** enable steeper overhangs by reducing the unsupported distance between layers, while **larger layer heights** increase this gap, leading to more sagging and requiring support material at shallower angles.
