# Material Flow Ratio and Pressure Advance

Flow ratio and pressure advance settings for the selected material.

{{T1}}

## Flow Ratio

{{M1}}
The material may have volumetric change after switching between molten and crystalline states. This setting changes all extrusion flow of this filament in G-code proportionally.  
The recommended value range is between 0.95 and 1.05. You may be able to tune this value to get a nice flat surface if there is slight overflow or underflow.  
The final object flow ratio is this value multiplied by the [filament flow ratio]({{L1}}).

> [!TIP]
> Check the [Flow Ratio Calibration guide]({{L2}}).

## Pressure Advance

{{M2}}
`Simple` [Variable]({{L3}}): `enable_pressure_advance`.  
`Advanced` [Variable]({{L4}}): `pressure_advance`.  
{{M3}}
Pressure advance [Klipper]({{L5}}) and [RepRap]({{L6}}) AKA [Linear advance (Marlin)]({{L7}}) is a feature that compensates for the lag in filament pressure within the nozzle during acceleration and deceleration. It helps improve print quality by reducing issues like blobs, oozing, and inconsistent extrusion, especially at corners or during fast movements.

> [!NOTE]
> Auto calibration result will be overwritten once enabled

> [!TIP]
> Check the [Pressure Advance Calibration guide]({{L8}}).

### Enable adaptive Pressure Advance (beta)

{{M4}}
With increasing print speeds (and hence increasing volumetric flow through the nozzle) and increasing accelerations, it has been observed that the effective PA value typically decreases. This means that a single PA value is not always 100% optimal for all features and a compromise value is usually used that does not cause too much bulging on features with lower flow speed and accelerations while also not causing gaps on faster features.

This feature aims to address this limitation by modeling the response of your printer's extrusion system depending on the volumetric flow speed and acceleration it is printing at. Internally, it generates a fitted model that can extrapolate the needed pressure advance for any given volumetric flow speed and acceleration, which is then emitted to the printer depending on the current print conditions.

When enabled, the pressure advance value above is overridden. However, a reasonable default value above is strongly recommended to act as a fallback and for when tool changing.

> [!TIP]
> Check the [Adaptive Pressure Advance Calibration guide]({{L9}}).

#### Enable adaptive pressure advance for overhangs (beta)

{{M5}}
Enable adaptive PA for overhangs as well as when flow changes within the same feature. This is an experimental option, as if the PA profile is not set accurately, it will cause uniformity issues on the external surfaces before and after overhangs.

#### Pressure advance for bridges

{{M6}}
Pressure advance value for bridges. Set to 0 to disable.  
A lower PA value when printing bridges helps reduce the appearance of slight under extrusion immediately after bridges.  
This is caused by the pressure drop in the nozzle when printing in the air and a lower PA helps counteract this.

#### Adaptive pressure advance measurements (beta)

Add sets of **pressure advance** (PA) values, the **volumetric flow speeds** and **accelerations** they were measured at, separated by a comma.  
One set of values per line. For example:

{{C1}}

{{C2}}

##### How to calibrate Adaptive Pressure Advance

It's highly recommended to use the [Adaptive Pressure Advance Calibration guide]({{L10}}).

1. Run the pressure advance test for at least 3 speeds per acceleration value. It is recommended that the test is run for at least the speed of the external perimeters, the speed of the internal perimeters and the fastest feature print speed in your profile (usually it's the sparse or solid infill). Then run them for the same speeds for the slowest and fastest print accelerations, and no faster than the recommended maximum acceleration as given by the Klipper input shaper.
2. Take note of the optimal PA value for each volumetric flow speed and acceleration. You can find the flow number by selecting "flow" from the color scheme drop down and move the horizontal slider over the PA pattern lines. The number should be visible at the bottom of the page. The ideal PA value should be decreasing the higher the volumetric flow is. If it is not, confirm that your extruder is functioning correctly. The slower and with less acceleration you print, the larger the range of acceptable PA values. If no difference is visible, use the PA value from the faster test.
3. Enter the triplets of PA values, Flow and Accelerations in the text box here and save your filament profile.
