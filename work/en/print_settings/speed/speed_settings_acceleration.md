# Acceleration

Acceleration in 3D printing is usually set in the printer's firmware.  
These settings override the firmware acceleration when the [normal printing acceleration]({{L1}}) is greater than 0.  
Orca limits the acceleration so it doesn't exceed the maximum set in the printer's Motion Ability settings.

{{T1}}

## Normal printing

{{M1}}
The default acceleration for both normal printing and travel after the first layer.

> [!NOTE]
> If this value is set to 0, Orca doesn't send acceleration commands, so the printer's own acceleration is used and the other acceleration settings are disabled.

## Outer wall

{{M2}}
Acceleration for [outer wall]({{L2}}) printing. This is usually set to a lower value than normal printing to ensure better quality.

## Inner wall

{{M3}}
Acceleration for [inner wall]({{L3}}) printing. This is usually set to a higher value than outer wall printing to improve speed.

## Bridge

{{M4}}
Acceleration of [bridges]({{L4}}). If the value is expressed as a percentage (e.g. 50%), it will be calculated based on the outer wall acceleration.

## Sparse infill

{{M5}}
Acceleration of [sparse infill]({{L5}}). If the value is expressed as a percentage (e.g. 100%), it will be calculated based on the default acceleration.

## Internal solid infill

{{M6}}
Acceleration of [internal solid infill]({{L6}}). If the value is expressed as a percentage (e.g. 100%), it will be calculated based on the default acceleration.

## Initial layer

{{M7}}
Acceleration of [initial layer]({{L7}}). Using a lower value can improve build plate adhesion.

## Initial layer travel

{{M8}}
Acceleration of [initial layer travel]({{L8}}).
Using a lower value can improve build plate adhesion. If the value is expressed as a percentage (e.g. 50%), it will be calculated based on the [Travel Acceleration]({{L9}}).

## Top surface

{{M9}}
Acceleration of [top surface infill]({{L10}}). Using a lower value may improve top surface quality.  
A value similar to the [outer wall acceleration]({{L11}}) is recommended.

## Travel

{{M10}}
Acceleration of [travel]({{L12}}) moves. This is usually set to a higher value than normal printing to reduce travel time.

## Enable accel to decel

{{M11}}
Adjusts Klipper's `max_accel_to_decel` automatically. Each time Orca sets the acceleration with `SET_VELOCITY_LIMIT ACCEL=`, it adds `ACCEL_TO_DECEL=` at the [accel to decel]({{L13}}) percentage of that acceleration. When disabled, `ACCEL_TO_DECEL` is not sent.  
This option is only shown when the [G-code flavor]({{L14}}) is Klipper, and it is enabled by default.

### Accel to decel

{{M12}}
Percentage of the acceleration that Klipper's `max_accel_to_decel` is set to, from 1% to 100% (default 50%).  
For example, at 5000 mm/s² and 50%, Orca sends `SET_VELOCITY_LIMIT ACCEL=5000 ACCEL_TO_DECEL=2500`.  
It can only be edited when [Enable accel to decel]({{L15}}) is checked.
