# Basic Extruder Information

This section contains the basic information about the extruder.  
When using multiple extruders, you can set different values for each extruder.

{{T1}}

## Nozzle diameter

{{M1}}
The diameter of the nozzle for each extruder.  

> [!TIP]
> You can use different nozzle diameters for each extruder to achieve different print qualities and speeds.  
> Follow the [Mixed Nozzle Sizes]({{L1}}) guide for more information on how to use this feature.

## Nozzle volume

{{M2}}
Volume of nozzle between the filament cutter and the end of the nozzle

## Extruder Layer Height Limits

{{M3}}
Min and max layer height limits for the extruder. These settings are used when adaptive layer height is enabled.

## Extruder printable area

{{M4}}
The area of the bed that each extruder can reach, on printers whose extruders can't all cover the whole bed. On the Bambu Lab H2D, for example, the left nozzle reaches X 0 to 325 mm and the right nozzle X 25 to 350 mm of the 350 mm wide bed, so a 25 mm strip on each side can only be printed by one nozzle.

Orca uses these areas to:

- Show the left and right nozzle-only areas on the plate.
- Warn before slicing when an object extends beyond the printable range of the nozzle that has to print one of its filaments.
- Keep a filament off an extruder that can't reach every part printed with it when filaments are grouped automatically.
- Clip the brim to the area of the extruder that prints it.
- Keep the prime tower inside the area that every extruder can reach.
- Report an error after slicing when a filament's G-code path leaves the printable range of its extruder.

When the profile leaves it empty, every extruder can reach the whole [printable area]({{L2}}).

This value comes from the printer profile and can't be edited. It is only shown for printers with two extruders.

## Extruder offset Position

{{M5}}
If your firmware doesn't handle the extruder displacement you need the G-code to take it into account. This option lets you specify the displacement of each extruder with respect to the first one. It expects positive coordinates (they will be subtracted from the XY coordinate).
