# Other layers speed

## Speed limitations

> [!IMPORTANT]
> Every speed setting is limited by several parameters like:
>
> - [Maximum Volumetric Speed]({{L1}})
> - Machine / Motion ability
> - [Acceleration]({{L2}})
> - [Jerk settings]({{L3}})
> - [Filament layer cooling time]({{L4}})

{{T1}}

## Outer wall

{{M1}}
Speed of the outer wall, which is the outermost, visible wall. It is usually printed slower than the [inner wall]({{L5}}) to get better quality and good layer adhesion.
This setting is also limited by [Machine / Motion ability / Resonance avoidance speed settings]({{L6}}).  
It can be excluded from the [layer cooling slowdown]({{L7}}) with [Don't slow down outer walls]({{L8}}).

## Inner wall

{{M2}}
Speed of the inner walls, which are printed faster than the outer wall to reduce print time. Their flow is still recommended to stay well below the [maximum volumetric speed]({{L9}}) to ensure good layer adhesion and reduce internal stresses in the material.

## Small perimeters

{{M3}}
Speed of walls with a theoretical radius <= [small perimeters threshold]({{L10}}).
Any shape (not only circles) will be considered as a small perimeter.

If expressed as a percentage (for example: 80%), it will be calculated on the [outer wall speed]({{L11}}).

> [!NOTE]
> The default is 50% of the [outer wall speed]({{L12}}).

### Small perimeters threshold

{{M4}}
**Radius** in millimeters below which the speed of perimeters will be reduced to the [small perimeters speed]({{L13}}).  
A perimeter is considered small when:

$$
\frac{\text{Perimeter Length}}{2\pi} \leq \text{Threshold}
$$

For example, if the threshold is set to 5 mm, then the perimeter length must be less than or equal to 31.4 mm `(2 * π * 5 mm)` to be considered a small perimeter.

- A Circle with a diameter of 10 mm will have a perimeter length of approximately 31.4 mm, which is equal to the threshold, so it will be considered a small perimeter.
- A Cube of 10mm x 10mm will have a perimeter length of 40 mm, which is greater than the threshold, so it will not be considered a small perimeter.
- A Cube of 5mm x 5mm will have a perimeter length of 20 mm, which is less than the threshold, so it will be considered a small perimeter.

> [!NOTE]
> Zero will disable [small perimeters speed]({{L14}}), and walls will use their regular speed, such as the [outer wall speed]({{L15}}).

## Sparse infill

{{M5}}
Speed of [sparse infill]({{L16}}) which is printed faster than solid infill to reduce print time.  
If you are using your [Infill Pattern]({{L17}}) as an aesthetic feature, you may want to set it closer to the [outer wall speed]({{L18}}) to get better quality.

## Internal solid infill

{{M6}}
Speed of internal solid infill, which fills the interior of the model with solid layers.  
This is typically set faster than the [top surface speed]({{L19}}) to optimize print time, while still ensuring adequate strength and layer adhesion. Adjusting this speed can help balance print quality and efficiency, especially for models requiring strong internal structures.  
Solid infill is also considered when [infill % is set to 100%]({{L20}}).

## Top surface

{{M7}}
Speed of the [topmost solid layers]({{L21}}) of the print. This is usually set similar to the [outer wall speed]({{L22}}) to achieve a smoother and higher-quality finish on visible surfaces. Lower speeds help minimize surface defects and improve the appearance of the final printed object.

## Gap infill

{{M8}}
Speed of [gap infill]({{L23}}), which is used to fill small gaps or holes in the print.

## Ironing speed

{{M9}}
[Ironing]({{L24}}) and [Support Ironing]({{L25}}) speed, typically slower than the top surface speed to ensure a smooth finish.  
Each filament can replace this speed with its own Ironing speed in its [setting overrides]({{L26}}).

## Support

{{M10}}
Speed at which [support]({{L27}}) material is printed. Slower speeds help ensure that supports are stable and effective during the print process.

## Support interface

{{M11}}
Speed for the support interface layers, which are the layers directly contacting the model. This is usually set even slower than the main [support speed]({{L28}}) to maximize surface quality where the support meets the model and to make support removal easier.

## Small tree support perimeters

{{M12}}

Same as [Small perimeters]({{L29}}), but for supports.  
This separate setting affects the speed of support extrusions whose length is within the [small support perimeters threshold]({{L30}}).  
If expressed as a percentage (for example: 80%), it will be calculated on the [support]({{L31}}) or [support interface]({{L32}}) speed.  
The default is 50% of the [support]({{L33}}) or [support interface]({{L34}}) speed.

### Small tree support perimeters threshold

{{M13}}
Sets the threshold below which the [small support perimeters]({{L35}}) speed is applied. Like the [small perimeters threshold]({{L36}}), it is a radius: a support extrusion is considered small when its length is <= 2π × threshold.  
The default threshold is 0 mm, which disables it.
