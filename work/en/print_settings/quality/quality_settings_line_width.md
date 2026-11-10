# Line Width

{{M1}}
These settings define how wide each extruded line of filament will be.  
Line width can be configured in two ways:

- Fixed value in millimeters (mm)
- Percentage of the nozzle diameter

> [!TIP]
> Using percentages allows the slicer to automatically adjust the line width when the nozzle size changes, helping maintain consistent print quality across different nozzle sizes.

A good starting point is setting the line width to **100% of the nozzle diameter**. Values below this may lead to poor adhesion, while values above **150%** can cause **over-extrusion**, resulting in blobs or poor surface quality.  
However, slightly wider lines generally improve **layer bonding** and **print strength**, especially for internal features like walls and infill.

> [!NOTE]
> **Line width is the width of the line as laid on the layer.** Orca calculates the extruded volume from the line width and layer height, so a 100% line width gives a line as wide as the nozzle, and higher values squish the line wider than the nozzle opening.  
> You can read more on the flow math here: [Flow Math]({{L1}}).

> [!IMPORTANT]
> This will match only if using the [**Classic** wall generator]({{L2}}).  
> [**Arachne**]({{L3}}) will adjust the line width dynamically based on the model's geometry, using these values as a reference.

## Line Types

In OrcaSlicer, you can assign different line widths to specific parts of the print. Each type can be customized:

### Default

Fallback value used when a specific line width is not set (set to `0`).

### First Layer

{{M2}}
A wider first layer (with a higher [first layer height]({{L4}})) improves bed adhesion and compensates for uneven build surfaces.  
First layer line width also overrides [Brim's]({{L5}}) and [Skirt's]({{L6}}) line width.

### Outer Wall

{{M3}}
Controls dimensional accuracy and surface finish.  
Recommended: **105%–120%** of the nozzle diameter for clean overhangs and detail.

### Inner Wall

{{M4}}
Can be set wider than the outer wall to enhance structural strength.  
Typical value: **≥120%**.

### Top Surface

{{M5}}
Affects the quality of visible top layers.  
Recommended: **100%–105%** for smooth results without over-extrusion.

### Sparse Infill

{{M6}}
Recommended to use a conservative value, typically around 115% to improve layer adhesion without getting near volumetric flow limitations.  
If you need stronger infill, it's recommended to use [infill line multiplier]({{L7}}) when possible.

### Internal Solid Infill

{{M7}}
Used for internal solid infill, bottom surfaces, and [100% infill]({{L8}}).  
Recommended: **~110%** for good layer adhesion and visual quality.

### Support

{{M8}}
Typically set to **100%** to balance material usage and functionality. Reducing it too much can lead to weak support structures that may not hold up during printing or break easily during removal, leaving debris on the model.

### Bridge

{{M9}}
Bridges are printed in mid-air, so the bridge line width can't exceed the nozzle diameter.  
To make adjacent bridge lines bond properly and reduce sagging, it's recommended to use **~100%** of the nozzle diameter and increase [Bridge density]({{L9}}).

{{I1}}
{{I2}}

> [!TIP]
> If disabled (set to 0), [Internal Solid Infill]({{L10}}) line width will be used for bridges (thick bridges use the nozzle diameter instead).  
> This allows you to use a theoretically wider line width for bridges.  
> However, it is recommended to use [thick bridges]({{L11}}) or a [bridge flow adjustment]({{L12}}) instead.
