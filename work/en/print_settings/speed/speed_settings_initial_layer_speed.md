# Initial layer speed

Printing the first layer slower than the rest of the print is a widely recommended practice. This helps ensure strong adhesion to the print bed, reduces the chances of warping or curling at the edges, and allows better compensation for minor leveling inconsistencies.

## Initial layer

{{M1}}
This setting determines the printing speed of the [outer/inner walls]({{L1}}) and the brim on the first layer.  
All other first layer extrusions, such as [solid infill]({{L2}}) and the [sparse infill]({{L3}}) printed when [bottom layers]({{L4}}) is set to 0, use the [First layer infill]({{L5}}) speed.  
Adjusting this speed helps ensure proper adhesion and print quality for the initial layer.

## Initial layer infill

{{M2}}
Defines the speed used for everything on the first layer except walls and brim, mainly the [solid infill]({{L6}}) regions. These areas require more precise and consistent extrusion to create a flat and stable surface for subsequent layers. Printing this section too fast may result in high internal stresses (increased risk of warping), poor layer uniformity, or adhesion failures.

## Initial layer travel speed

{{M3}}
Sets the travel (non-printing movement) speed for the first layer. This doesn't affect print quality and can be set as a percentage of the [travel speed]({{L7}}).  
Usually, this is set to 100% of the [travel speed]({{L8}}), but it can be reduced if you want to minimize vibrations or if your printer has issues with high-speed travel movements.

## Number of slow layers

{{M4}}
Specifies how many of the first layers should be printed at a reduced speed. Instead of jumping straight to full speed after the first layer, the speed gradually increases in a linear fashion over this number of layers. This gradual ramp-up helps maintain adhesion and gives the print more stability in its early stages, especially on prints with a small contact area or materials prone to warping.

{{I1}}
