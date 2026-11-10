# Skirt

A skirt is one or more additional perimeters printed around the model outline on the first layer(s). It helps prime the hotend, stabilize extrusion before the model starts, and can act as a basic wind/draft shield when built taller.

{{T1}}

## Loops

{{M1}}
Number of skirt loops to print.  
Usually 2 loops are recommended, but more loops improve priming and give a larger buffer between the nozzle and the part, at the cost of extra filament and time.  
Set to 0 to disable the skirt.

{{I1}}

## Type

{{M2}}

### Combined

A single skirt that surrounds all objects on the bed.
  Recommended for general use.

{{I2}}

### Per object

Each object gets its own skirt printed separately. Objects close enough for their skirts to overlap share a single skirt.
  Recommended when using [Print sequence by object]({{L1}}).

{{I3}}

## Minimum extrusion Length

{{M3}}
Minimum filament extrusion length in mm when printing the skirt. Zero means this feature is disabled.  
Using a non-zero value is useful if the printer is set up to print without a prime line.  
The final number of loops is not taken into account when arranging objects or validating the distance between them. Increase the number of loops in that case.

## Distance

{{M4}}
Distance from skirt to brim or object.  
Increasing this distance can help avoid collisions with brims or supports, but will increase the footprint of the skirt and filament usage.

## Start point

{{M5}}
Start angle for the skirt relative to the object center. 0° is the right-most position (along the +X axis), angles increase counter-clockwise.  
Use this to control where the skirt begins to better align with part features or prime locations.

## Speed

{{M6}}
Printing speed for the skirt in mm/s. Set to 0 to use the [First layer infill]({{L2}}) speed on the first layer and the [Support]({{L3}}) speed on higher layers.  
Slower speeds give a more reliable prime; very fast skirt speeds may not adhere properly and come off, causing problems with the part.

## Height

{{M7}}
Number of layers the skirt should be printed for. Usually 1 layer for priming. Increase the height if you want a taller draft shield effect.

## Shield

{{M8}}
When enabled, the skirt is printed as a draft shield: a taller wall surrounding the part to help protect prints (especially ABS/ASA) from drafts and sudden temperature changes.  
This is most useful for open-frame printers without an enclosure.

- Enabled: the shield is as tall as the tallest printed model on the bed.
- Disabled: the skirt uses the [Height]({{L4}}) value.

> [!NOTE]
> The skirt is printed at the [skirt distance]({{L5}}) from the brim, or from the object if it has no brim, so the draft shield does not intersect brims.

## Single loop after first layer

{{M9}}
When enabled, limits the skirt or draft shield to a single wall after the first layer (i.e. only one loop is printed on subsequent layers). This reduces filament and print time but makes the shield less robust and more prone to warping or cracking.
