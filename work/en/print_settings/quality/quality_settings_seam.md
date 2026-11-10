# Seam

Unless printed in spiral vase mode, every layer needs to begin somewhere and end somewhere. That start and end of the extrusion is what results in what visually looks like a seam on the perimeters. This section contains options to control the visual appearance of a seam.

{{T1}}

## Seam Position

{{M1}}
Controlling the position of seams can help improve the appearance and strength of the final print.

Typically, [Aligned Back]({{L1}}), [Aligned]({{L2}}), or [Back]({{L3}}) work the best, especially in combination with [seam painting]({{L4}}) or [Precise Seam]({{L5}}) modifiers.  
However, as seams create weak points and slight surface "bulges" or "divots", [random]({{L6}}) seam placement may be optimal for parts that need higher strength as that weak point is spread to different locations between layers (e.g., a pin meant to fit through a hole).

### Aligned

Will attempt to align the seams vertically across layers, placing them at the least visible spots of the model, such as concave corners.

{{I1}}

### Aligned Back

Combines [Aligned]({{L7}}) and [Back]({{L8}}) strategies by prioritizing seam placement away from the front-facing side while still finding optimal hidden locations for other orientations.  
This is particularly useful for directional models like sculptures or figurines that have a clear front view.  
Unlike "Back" which always places seams at the rearmost position, "Aligned Back" uses intelligent positioning that avoids the front while maintaining sophisticated seam hiding capabilities.

{{I2}}

### Nearest

Picks the seam at the point that is closest to where the nozzle already is (while still preferring concave corners, avoiding overhangs, and avoiding visible spots). This reduces travel moves but results in seams scattered around the object rather than aligned in a vertical line.

{{I3}}

### Back

This option places the seam on the back side (Max Y point in that layer) of the object, away from the view. It is useful for objects that will be displayed with a specific orientation.

{{I4}}

### Random

This option places the seam randomly across the object, which can help to distribute the seam points and increase the overall strength of the print.

{{I5}}

## Modifiers

### Staggered inner seams

{{M2}}
As the seam location forms a weak point in the print, staggering the seam on the internal perimeters can help reduce stress points. This setting shifts the seam of each internal wall along the loop, away from the external perimeter seam, by an amount based on the wall's depth, forming a zigzag pattern. This way, the internal and external seams don't all align at the same point, distributing those weak points further away from the seam location, hence making the part stronger. It can also help improve the water tightness of your model.

{{I6}}

### Seam gap

{{M3}}
Controls the gap in mm or as a percentage of the nozzle size between the two ends of a loop starting and ending with a seam.

- A larger gap will reduce the bulging seen at the seam.
- A smaller gap reduces the visual appearance of a seam.

For a well-tuned printer with [pressure advance]({{L9}}) and [filament retraction]({{L10}}), a value of **0-15%** is typically optimal.

{{I7}}

### Scarf joint seam

{{M4}}
`Advanced` [Variables]({{L11}}): `seam_slope_type`, `seam_slope_conditional`, `scarf_angle_threshold`, `scarf_overhang_threshold`, `scarf_joint_speed`, `seam_slope_start_height`, `seam_slope_entire_loop`, `seam_slope_min_length`, `seam_slope_steps`, `seam_slope_inner_walls`.  
`Expert` [Variable]({{L12}}): `scarf_joint_flow_ratio`.  
Adjusts the extrusion flow rate at seam points to create a smooth overlap between the start and end of each loop, minimizing visible defects.

{{I8}}

Advantages:

- Reduces visible z-seams
- Improves cosmetic quality of curved surfaces
- Can slightly improve part strength at seams by softening transitions

Disadvantages:

- May increase print time slightly
- Less effective on sharp corners and overhangs
- Requires tuning of parameters like length, speed, and flow for best results

Scarf joints are never applied on the first layer, in [spiral vase]({{L13}}) mode, or on [belt printers]({{L14}}).

> [!NOTE]
> Read more here: [Better Seams - An OrcaSlicer Guide]({{L15}}).

#### Scarf joint seam Type

- **None:** Scarf joint seams are disabled (default).
- **Contour:** Applies scarf seams only to the outer wall of the model's contours, not to holes.
- **Contour and hole:** Applies scarf seams to the outer walls of both contours and holes.

#### Conditional scarf joint

Applies scarf joints only to smooth, curved perimeters, where a traditional seam cannot be hidden in a sharp corner. A perimeter with a corner sharper than the *Conditional angle threshold* (default 155°) keeps a standard seam, as does a seam whose overhang exceeds the *Conditional overhang threshold* (default 40% of the wall width).

#### Scarf joint speed

This option sets the printing speed for scarf joints.  
It is recommended to print scarf joints at a slow speed (less than 100 mm/s).  
It's also advisable to enable [Extrusion rate smoothing]({{L16}}) if the set speed varies significantly from the speed of the outer or inner walls. If the speed specified here is higher than the speed of the outer or inner walls, the printer will default to the slower of the two speeds. When specified as a percentage (e.g., 80%), the speed is calculated based on the respective outer or inner wall speed. The default value is set to 100%.

#### Scarf joint height

Defines the vertical offset for the start of the scarf ramp, specified either in millimeters or as a percentage of the current layer height.  
A value of 0 means the scarf begins at the top of the previous layer and ramps up to the full layer height over the scarf length.  
For example, on the second layer with a 0.2 mm layer height, setting this to 50% (0.1 mm) will start the scarf at 0.3 mm and ramp up to 0.4 mm by the end of the scarf length, while the rest of the lines print at 0.4 mm.  
This setting helps create a smoother transition and can reduce visible seam artifacts.

#### Scarf around entire wall

If enabled, the scarf joint wraps around the full perimeter of the wall. Typically disabled, as this may increase print time without significant seam improvement.

#### Scarf length

Defines the horizontal length over which the scarf ramp transitions. A value of 0 disables the scarf joint. The default (20 mm) generally offers smooth and effective blending.

#### Scarf steps

Minimum number of segments used to build the scarf transition.  
More steps create a smoother gradient, but the default value (10) is sufficient in most cases.

#### Scarf joint flow ratio

Adjusts extrusion flow during scarf printing. A value of 1 applies standard flow. Lower values reduce flow but may introduce under-extrusion.  
Recommended to keep at 1.

#### Scarf joint for inner walls

When enabled, scarf joints are also applied to inner walls, not only to the outer wall. This has minimal visual impact and is usually left disabled unless inner seam quality is a priority.

### Role based wipe speed

{{M5}}
Controls the speed of a wipe motion, i.e., how fast the nozzle will move over a printed area to "clean" it before traveling to another area of the model.  
It is recommended to turn this option on, to ensure the nozzle performs the wipe motion with the same speed that the feature was printed with.

### Wipe speed

{{M6}}
If [Role based wipe speed]({{L17}}) is disabled, this sets the wipe speed, either as an absolute value or as a percentage of the travel speed.

### Wipe on loop (inward movement)

{{M7}}
When finishing printing an outer wall "loop" (i.e., an extrusion that starts and ends at the same point), move the nozzle slightly inwards towards the part. This only applies when [Wall loops]({{L18}}) is greater than 1. That move aims to reduce seam unevenness by tucking in the end of the seam to the part. It also slightly cleans the nozzle before traveling to the next area of the model, reducing stringing.  
The inward move itself is a short, fixed move of about 20% of the nozzle diameter. The wipe and retraction that follow use your printer/material Wipe distance and Retract amount before wipe values.

{{I9}}

{{I10}}

### Wipe inward

{{M8}}

Shifts the wipe that follows an external wall away from the outer surface and onto the inner wall next to it. Instead of running the hot nozzle back over the outside of the part it has just extruded, the nozzle wipes over material that is no longer visible, which reduces the reheating that leaves a mark around the seam. This is most noticeable at layer heights below 0.1 mm, where wipe marks stand out the most.

It applies only to external walls, including the walls around holes. On an outer contour the wipe moves inwards; around a hole it moves outwards, away from the hole and into the surrounding material. Inner walls, infill and supports keep their regular wipe.

The inward wipe runs at the end of the external loop, after the [Wipe on loop]({{L19}}) move if that option is enabled, and without retracting filament, so a short travel to the next wall still will not force a retraction or Z hop.

For the option to take effect:

- [Wipe while retracting]({{L20}}) must be enabled for the filament in use, and the length of the move is limited by the [Wipe distance]({{L21}}).
- An inner wall beside the seam must already be on the plate when the wipe runs, so the region needs more than one wall and a wall order that prints the inner walls first. With [Outer/Inner]({{L22}}) order the inner wall has not been printed yet, so the regular wipe is kept.

Orca keeps the regular wipe path whenever no supported inward path exists: single wall areas, places where the inner wall is locally missing, tight corners, narrow features or a wide [seam gap]({{L23}}). The fallback is silent and only affects the loops concerned. Both the classic and Arachne wall generators are supported, and the real width of each path is used, so automatic [line widths]({{L24}}) and Arachne's variable widths are taken into account.

> [!NOTE]
> Inward wiping is switched off automatically during the [Pressure Advance]({{L25}}) and [Retraction]({{L26}}) calibrations so that it cannot mask the behavior being measured.

#### Wipe inward distance

How far the wipe path is shifted away from the external perimeter, either in millimeters or as a percentage of the actual outer wall extrusion width. The default, 50%, shifts the path by half of the outer wall width, which places it over the boundary between the outer and the inner wall.

The offset is clamped by the actual outer wall width and by the spacing available to the adjacent wall, so values above 100%, or the equivalent absolute distance, have no further effect. Setting it to 0 disables the offset and the regular wipe is used.

This option is only shown when *Wipe inward* is enabled.

### Wipe Before External

{{M9}}
To minimize the visibility of potential over-extrusion at the start of an external perimeter, the de-retraction move is performed slightly inside the model, next to the start of the external perimeter. That way, any potential over-extrusion is hidden from the outside surface.

This is useful when printing with [Outer/Inner]({{L27}}) or [Inner/Outer/Inner]({{L28}}) wall print order, as in these modes it is more likely that an external perimeter is printed immediately after a de-retraction move, which would cause slight extrusion variance at the start of a seam.

## Tips

With seams being inevitable when 3D printing using FFF, there are two distinct approaches on how to deal with them:

1. **Try and hide the seam as much as possible:** This can be done by enabling scarf seam, which works very well, especially with simple models with limited overhang regions.
2. **Try and make the seam as "clean" and "distinct" as possible:** This can be done by tuning the seam gap and enabling role-based wipe speed, wipe on loops, wipe inward, and wipe before the external loop.

## Troubleshooting Seam Performance

The section below will focus on troubleshooting traditional seams. For scarf seam troubleshooting, refer to the guide linked above.

There are several factors that influence how clean the seam of your model is, with the biggest one being extrusion control after a travel move. As a seam defines the start and end of an extrusion, it is critical that:

1. **The same amount of material is extruded at the same point across layers** to ensure a consistent visual appearance at the start of a seam.
2. **The printer consistently stops extruding at the same point** across layers.

However, due to mechanical and material tolerances, as well as the very nature of 3D printing with FFF, that is not always possible. Hopefully with some tuning you'll be able to achieve prints like this!

{{I11}}

### Troubleshooting the Start of a Seam

Imagine the scenario where the toolhead finishes printing a layer line on one side of the bed, retracts, travels the whole distance of the bed to de-retract, and starts printing another part. Compare this to the scenario where the toolhead finishes printing an internal perimeter and only travels a few mm to start printing an external perimeter, without even retracting or de-retracting.

The first scenario has much more opportunity for the filament to ooze outside the nozzle, resulting in a small blob forming at the start of the seam or, conversely, if too much material has leaked, a gap/under-extrusion at the start of the seam.

The key to a consistent start of a seam is to reduce the opportunity for ooze as much as possible. The good news is that this is mostly tunable by:

1. **Ensure your pressure advance is calibrated correctly**. A too low pressure advance will result in the nozzle experiencing excess pressure at the end of the previous extrusion, which increases the chance of oozing when traveling.
2. **Make sure your travel speed is as fast as possible within your printer's limits**, and the travel acceleration is as high as practically possible, again within the printer's limits. This reduces the travel time between features, reducing oozing.
3. **Enable Wipe before external loop** – this setting performs the de-retraction move inside the model, hence reducing the visual appearance of the "blob" if it does appear at the seam.
4. **Increase your travel distance threshold to be such that small travel moves do not trigger a retraction and de-retraction operation**, reducing extrusion variances caused by the extruder tolerances. 2-4mm is a good starting point as, if your PA is tuned correctly and your travel speed and acceleration are high, it is unlikely that the nozzle will ooze in the milliseconds it will take to travel to the new location.
5. **Enable retract on layer change**, to ensure the start of your layer is always performed under the same conditions – a de-pressurized nozzle with retracted filament.

In addition, some toolhead systems are inherently better at seams compared to others. For example, high-flow nozzles with larger melt zones usually have poorer extrusion control as more of the material is in a molten state inside the nozzle. They tend to string more, ooze easier, and hence have poorer seam performance. Conversely, smaller melt zone nozzles have more of the filament solid in their heat zone, leading to more accurate extrusion control and better seam performance.

So this is a trade-off between print speed and print quality. From experimental data, volcano-type nozzles tend to perform the worst at seams, followed by CHT-type nozzles, and finally regular flow nozzles.

In addition, larger nozzle diameters allow for more opportunity for material to leak compared to smaller diameter nozzles. A 0.2/0.25 mm nozzle will have significantly better seam performance than a 0.4, and that will have much better performance than a 0.6mm nozzle and so forth.

### Troubleshooting the End of a Seam

The end of a seam is much easier to get right, as the extrusion system is already at a pressure equilibrium while printing. It just needs to stop extruding at the right time and consistently.

**If you are getting bulges at the seam**, the extruder is not stopping at the right time. The first thing to tune would be **pressure advance** – too low of a PA will result in the nozzle still being pressurized when finishing the print move, hence leaving a wider line at the end as it stops printing.

And the opposite is true too – **too high PA will result in under extrusion at the end of a print move**, shown as a larger-than-needed gap at the seam. Thankfully, tuning PA is straightforward, so run the calibration tests and pick the optimal value for your material, print speed, and acceleration.

Furthermore, the printer mechanics have tolerances – the print head may be requested to stop at point XY but practically it cannot stop precisely at that point due to the limits of micro-stepping, belt tension, and toolhead rigidity. Here is where tuning the seam gap comes into effect. **A slightly larger seam gap will allow for more variance to be tolerated at the end of a print move before showing as a seam bulge**. Experiment with this value after you are certain your PA is tuned correctly and your travel speeds and retractions are set appropriately.

Finally, the techniques of **wiping can help improve the visual continuity and consistency of a seam** (please note, these settings do not make the seam less visible, but rather make them more consistent!). Wiping on loops with a consistent speed helps tuck in the end of the seam, hiding the effects of retraction from view.

### The Role of Wall Ordering in Seam Appearance

The order of wall printing plays a significant role in the appearance of a seam. **Starting to print the external perimeter first after a long travel move will always result in more visible artifacts compared to printing the internal perimeters first and traveling just a few mm to print the external perimeter.**

For optimal seam performance, printing with **inner-outer-inner wall order is typically best, followed by inner-outer**. It reduces the amount of traveling performed prior to printing the external perimeter and keeps the nozzle pressure as consistent as possible, compared to printing outer-inner.
