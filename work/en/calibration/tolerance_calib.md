# Filament Tolerance Calibration

Each filament and printer combination can result in different tolerances. This means that even using the same filament and print profile, tolerances may vary from one printer to another.
To correct for these variations, OrcaSlicer provides:

- Filament Compensation:
    - [Shrinkage (XY)]({{L1}})
    - [Shrinkage (Z)]({{L2}})  
    {{I1}}
- [Process Compensation]({{L3}}):
    - [X-Y hole compensation]({{L4}})
    - [X-Y contour compensation]({{L5}})
    - [Precise wall]({{L6}})
    - [Precise Z height]({{L7}})  
  {{I2}}

> [!TIP]
> Follow the recommended calibration order in the [Calibration Guide]({{L8}}).

## Handy Models

OrcaSlicer includes several handy models to help you test and calibrate your printer.  
Right-click on your plate in Prepare mode and select "Add Handy Model" to access these models.  
{{I3}}

### Orca Tolerance Test

This calibration test is designed to evaluate the dimensional accuracy of your printer and filament. The model consists of a base with six hexagonal holes, each with a different tolerance: 0.0 mm, 0.05 mm, 0.1 mm, 0.2 mm, 0.3 mm, and 0.4 mm, as well as a hexagon-shaped tester.

{{I4}}

You can check the tolerance using either an 6mm Allen key or the included printed hexagon tester.
Use calipers to measure both the holes and the inner tester. Based on your results, you can fine-tune the X-Y hole compensation and X-Y contour compensation settings. Repeat the process until you achieve the desired precision.

{{I5}}
{{I6}}
