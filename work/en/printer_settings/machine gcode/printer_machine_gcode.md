# Machine G-code

Machine G-code are custom G-code scripts that are executed at specific points during the printing process. These scripts can be used to customize printer behavior, such as setting temperatures, moving the print head, or controlling fans.

> [!TIP]
> See your printer's firmware documentation for supported G-code commands and features.
>
> - [Marlin G-code]({{L1}})
> - [RepRap G-code]({{L2}})
> - [Klipper G-code]({{L3}})

> [!IMPORTANT]
> Machine G-code scripts are powerful tools for customizing your printing process. However, they can also cause issues if not used correctly.  
> It's recommended to use a known base of G-code commands for your specific printer firmware (e.g., Marlin, RepRap, etc.) and to understand the implications of each command used in the scripts.  
> Always test your G-code scripts thoroughly before using them in production.

{{T1}}

## Machine start G-code

{{M1}}
This G-code is executed at the beginning of a print job, before any printing starts. It is typically used to prepare the printer for printing, such as homing axes, heating the bed and nozzle, and performing any necessary pre-print checks.

You can also use it for setting up custom notifications with M300 (play beep sound) or use a custom purge sequence:

{{C1}}

## Machine end G-code

{{M2}}
This G-code is executed at the end of a print job, after all printing is complete. It is typically used to turn off heaters, move the print head away from the print, and perform any necessary post-print actions.

## Printing by object G-code

{{M3}}
This G-code is executed at the start of printing each individual object in a multi-object print job. It can be used to set specific parameters or perform actions for each object.

## Before layer change G-code

{{M4}}
This G-code is inserted at every layer change before the Z lift.

## Layer change G-code

{{M5}}
This G-code is inserted at every layer change after the Z lift.

## Timelapse G-code

{{M6}}
This G-code is used for capturing timelapse videos. It typically includes commands to move the print head out of the way for a photo and then return it to the previous position.

## Clumping detection G-code

{{M7}}
This G-code is inserted on every layer when [Enable clumping detection]({{L4}}) is enabled, to run the printer's check for filament clumped around the nozzle. Use the `layer_num` placeholder to choose the layers to check; the Bambu Lab profiles check a few of the early layers.

## Change filament G-code

{{M8}}
This G-code is inserted when filament is changed, including T commands to trigger tool change.

## Change extrusion role G-code

{{M9}}
This G-code is inserted when the [extrusion role]({{L5}}) is changed.
This is the Machine section of the feature "Change Extrusion Role G-code" that is also available in the [Material settings]({{L6}}) and [Process settings]({{L7}}).

Example G-codes:

- Marlin g-code to set fan speed to 10% (S25 out of S255) for BridgeInfill role and 30% (S75 out of S255) for other roles:

  {{C2}}
  
- Marlin G-code to set the fan speed to 0% for the ['Internal Sparse Infill' role]({{L8}}) and the first three layers, and to 30% `0.3*255` for the other roles. This achieves good layer adhesion while maintaining perimeter quality.:

  {{C3}}
  
- Marlin g-code to set pressure advance to 0 for ['Internal Sparse Infill' role]({{L9}}) and restore it to previous value for other roles:

  {{C4}}

## Pause G-code

{{M10}}
This G-code will be used as a code for the pause print. Users can insert pause G-code in the G-code viewer.

## Template Custom G-code

{{M11}}
This section allows users to define custom G-code templates that can be reused across different print jobs. Users can create and manage their own G-code snippets for various purposes.
