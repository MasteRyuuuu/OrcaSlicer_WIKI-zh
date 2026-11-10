# Material Cooling

{{T1}}

## Material Cooling for Specific Layer

This setting allows you to customize the cooling behavior of your 3D printer for specific layers of your print.  
Proper cooling is essential for achieving high-quality prints, especially when dealing with overhangs and bridges.

### No cooling for the first

{{M1}}
Number of initial layers during which part-cooling fans are disabled.
Disabling the fan for the first few layers improves build-plate adhesion and reduces early-layer warping.

### First layer fan speed

{{M2}}

Sets an exact fan speed (in %) for the first layer, overriding all other cooling settings.  
This is useful for protecting 3D-printed toolhead parts (e.g. Voron-style ABS/ASA ducts) from a hot bed: a small amount of airflow cools the ducts down without using full cooling, which may in certain conditions hurt first-layer adhesion. From the second layer onwards, normal cooling resumes.  
If [Full fan speed at layer]({{L1}}) is also set, the fan ramps smoothly from this value on the first layer up to your target by the chosen layer.  
Only available when [No cooling for the first]({{L2}}) is 0. Set to `-1` to disable it.

### Full fan speed at layer

{{M3}}
Fan speed is increased linearly from 0% starting at the layer specified by [close_fan_the_first_x_layers]({{L3}}) up to the maximum part-cooling speed at this specified layer.  
If this layer is less than or equal to [close_fan_the_first_x_layers]({{L4}}), it is ignored and the fan will reach the maximum allowed speed on the layer immediately after [close_fan_the_first_x_layers]({{L5}}) (i.e. at layer [close_fan_the_first_x_layers]({{L6}}) + 1).  
Set this option to `0` to disable the automatic ramp.

## Material Part Cooling Fan

{{M4}}
These settings control the behavior of the part cooling fan during printing. Proper configuration of these parameters can significantly enhance print quality by optimizing cooling for different features and layer times.

### Fan speed threshold

These settings define how the slicer manages part-cooling behavior and printing speed based on the estimated time it takes to print each layer.

#### Min fan speed threshold

When a layer’s estimated print time falls below the minimum time, the slicer begins enabling the part-cooling fan. The fan speed is gradually interpolated between the configured minimum and maximum fan speeds, depending on how short the layer time is.
If a minimum speed threshold is defined, the slicer may also slow down the G-code printing speed for layers faster than this value to ensure adequate cooling.

#### Max fan speed threshold

Layers with an estimated time below the maximum time may trigger additional print-speed reduction to improve cooling.
When auto-cooling is enabled, the fan speed may increase as needed, up to the defined maximum fan speed, which acts as the upper limit for cooling adjustments.

### Keep fan always on

{{M5}}
Enabling this setting means that part cooling fan will never stop entirely and will instead run at least at minimum speed to reduce the frequency of starting and stopping.

### Slow printing down for better layer cooling

{{M6}}
Enable this option to slow printing speed down to ensure that the final layer time is not shorter than the **Layer time** threshold in [Max fan speed threshold]({{L7}}), so that the layer can be cooled for a longer time. This can improve the quality for small details.

This happens after the [print speeds]({{L8}}) have been applied, so on small or fast layers the printed speed can be lower than the value you set. It applies to every layer, including the first one, and the slowed-down speeds are written into the G-code: you can see them in the Preview **Speed** view.

The slowdown has a floor: no extrusion is slowed down below the filament's [Min print speed]({{L9}}).  
If the layer would still be shorter than the Layer time with every extrusion at Min print speed, everything that can be slowed down prints at Min print speed and the layer finishes earlier than the target.

> [!TIP]
> If small layers still don't cool enough because Min print speed was reached, print several copies of the part at once so each layer takes longer.

#### How the slowdown is calculated

1. **Estimate the layer time.** For each layer, OrcaSlicer adds up the time of every move (extrusions, travels and dwells) as `length / speed`, starting at the first extrusion of the layer. Acceleration is not taken into account, so the real layer time is usually a bit longer than the estimate.
2. **Compare it with the Layer time.** If the estimate is equal or longer, the layer is not changed.
3. **Find the missing time.** Otherwise the missing time is `Layer time - estimated time`.
4. **Slow down the fastest extrusions first.** Only extrusion moves are slowed down: travels and wipes keep their speed but still count towards the layer time. Instead of scaling every speed by the same factor, OrcaSlicer finds a speed cap $F$. Every extrusion faster than $F$ is lowered to $F$, and slower extrusions keep their speed. $F$ is chosen so that the extra time equals the missing time:

$$
\sum_{v_i > F} t_i \left(\frac{v_i}{F} - 1\right) = \text{Layer time} - \text{Estimated time}
$$

Where $v_i$ is the speed and $t_i$ the time of each extrusion faster than $F$.  
$F$ is never lower than the [Min print speed]({{L10}}).

For example, a layer with a Layer time of 15 s:

| Feature | Length | Set speed | Time | Speed after slowdown | Time after slowdown |
| --- | --- | --- | --- | --- | --- |
| Outer wall | 200 mm | 100 mm/s | 2 s | 100 mm/s | 2 s |
| Inner wall | 600 mm | 200 mm/s | 3 s | 150 mm/s | 4 s |
| Sparse infill | 1200 mm | 300 mm/s | 4 s | 150 mm/s | 8 s |
| Travel | - | - | 1 s | - | 1 s |
| **Total** | | | **10 s** | | **15 s** |

5 s are missing. The infill and inner wall are capped at $F = \frac{600 + 1200}{3 + 4 + 5} = 150$ mm/s, and the outer wall, which is already slower than 150 mm/s, is not touched.

> [!NOTE]
> - The part cooling fan speed is calculated from the layer time **after** the slowdown.
> - When a layer prints with several filaments, the time of all of them is added up and only the filaments with the slowdown enabled are slowed down.
> - If Min print speed is set to `0`, there is no floor and all the extrusions are slowed down by the same factor instead.

### Don't slow down outer walls

{{M7}}
If enabled, this setting will ensure external perimeters are not slowed down to meet the minimum layer time. This is particularly helpful in the below scenarios:

1. To avoid changes in shine when printing glossy filaments
2. To avoid changes in external wall speed which may create slight wall artifacts that appear like Z banding
3. To avoid printing at speeds which cause VFAs (fine artifacts) on the external walls

When enabled, the outer walls are left out of the slowdown: they always print at their [outer wall speed]({{L11}}) and their time counts as fixed time, like travels.

The whole missing time is then taken from the rest of the extrusions, so:

- Inner walls, infill and other features are slowed down more than they would be otherwise, and can end up slower than the outer wall.
- [Min print speed]({{L12}}) is reached sooner, so small layers are more likely to finish faster than the Layer time.
- Overhang walls are still slowed down, as they are a different feature from the outer wall.

Using the [previous example]({{L13}}) with a Layer time of 22 s (12 s missing):

| Feature | Without the option | With the option |
| --- | --- | --- |
| Outer wall | 95.2 mm/s | 100 mm/s |
| Inner wall | 95.2 mm/s | 94.7 mm/s |
| Sparse infill | 95.2 mm/s | 94.7 mm/s |

Without the option, the cap reaches the outer wall and all three print at $\frac{2000}{9 + 12} \approx 95.2$ mm/s.  
With it, the outer wall keeps its 100 mm/s and the inner wall and infill drop to $\frac{1800}{7 + 12} \approx 94.7$ mm/s.

This keeps the outer surface consistent between layers at the cost of less cooling time on small layers.

### Min print speed

{{M8}}
The minimum print speed to which the printer slows down to maintain the minimum layer time defined above when the slowdown for better layer cooling is enabled.  
See [How the slowdown is calculated]({{L14}}).

### Force cooling for overhangs and bridges

{{M9}}
Enable this option to allow adjustment of the part cooling fan speed for specifically for overhangs, internal and external bridges. Setting the fan speed specifically for these features can improve overall print quality and reduce warping.

### Overhang cooling activation threshold

{{M10}}
When the overhang exceeds this specified threshold, force the cooling fan to run at the 'Overhang Fan Speed' set below. This threshold is expressed as a percentage, indicating the portion of each line's width that is unsupported by the layer beneath it. Setting this value to 0% forces the cooling fan to run for all outer walls, regardless of the overhang degree.

### Overhangs and external bridges fan speed

{{M11}}
Use this part cooling fan speed when printing bridges or overhang walls with an overhang threshold that exceeds the value set in the 'Overhangs cooling threshold' parameter above. Increasing the cooling specifically for overhangs and bridges can improve the overall print quality of these features.

Please note, this fan speed is clamped on the lower end by the minimum fan speed threshold set above. It is also adjusted upwards up to the maximum fan speed threshold when the minimum layer time threshold is not met.

### Internal bridges fan speed

{{M12}}
The part cooling fan speed used for all internal bridges. Set to -1 to use the overhang fan speed settings instead.

Reducing the internal bridges fan speed, compared to your regular fan speed, can help reduce part warping due to excessive cooling applied over a large surface for a prolonged period of time.

### Support interface fan speed

{{M13}}
This part cooling fan speed is applied when printing support interfaces. Setting this parameter to a higher than regular speed reduces the layer binding strength between supports and the supported part, making them easier to separate.  
Set to -1 to disable it.  
This setting is overridden by disable_fan_first_layers.

### Ironing fan speed

{{M14}}
This part cooling fan speed is applied when ironing. Setting this parameter to a lower than regular speed reduces possible nozzle clogging due to the low volumetric flow rate, making the interface smoother.  
Set to -1 to disable it.

### Auxiliary part cooling fan

{{M15}}
Set the speed for the auxiliary part-cooling fan if your printer provides one (see [auxiliary part-cooling fan]({{L15}})). The auxiliary fan runs during printing but is disabled for the initial layers defined by [No cooling for the first]({{L16}}).

G-code command: `M106 P2 S(0-255)`

### Exhaust fan

#### Activate air filtration

{{M16}}
Activate for better air filtration.

G-code command: `M106 P3 S(0-255)`

#### During print

{{M17}}
Speed of exhaust fan during printing. This speed will override the speed in filament custom G-code.

#### Complete print

{{M18}}
Speed of exhaust fan after printing completes.
