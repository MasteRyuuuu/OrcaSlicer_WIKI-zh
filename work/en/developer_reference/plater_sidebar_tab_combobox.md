# Application Structure Overview

WIP...

> [!WARNING]
> !! incomplete, possibly inaccurate, being updated with new info !!

## [`Plater`]({{L1}})

Refers to the entire application. The whole view, file loading, project saving and loading is all managed by this class. This class contains members for the model viewer, the sidebar, gcode viewer and everything else.

## [`Sidebar`]({{L2}})

This is relating the the sidebar in the application window

{{I1}}

## [`ComboBox`]({{L3}})

The drop down menus where you can see and select presets

{{I2}}

## [`Tab`]({{L4}})

Refers to the various windows with settings. e.g. the Popup to edit printer or filament preset. Also the section to edit process preset and the object list. These 4 are managed by `TabPrinter`, `TabFilament`, `TabPrint` and `TabPrintModel` respectively.

{{I3}}
