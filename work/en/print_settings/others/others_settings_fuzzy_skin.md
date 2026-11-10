# Fuzzy Skin

Fuzzy skin randomly perturbs the wall path to produce a deliberately rough, matte appearance on the model surface.  
These settings control where the effect is applied, how the noise is generated, and how aggressive the displacement or extrusion modulation is.

Useful for creating textures or hiding surface imperfections, but it increases print time and affects dimensional accuracy.

{{T1}}

## Fuzzy Skin Mode

{{M1}}
Choose which parts of the model receive the fuzzy-skin effect.

### Contour

Apply fuzzy skin only to the outermost contour (external perimeter) of the model.  
Useful for creating a textured edge while keeping the inner surfaces smooth.

### Hole

Apply fuzzy skin only to interior holes and cutouts. This can add grip or visual interest to negative features without affecting the outer surface.

### Contour and Hole

Apply fuzzy skin to both the outer contour and interior holes. Useful when you want the rough texture to appear on negative features as well.

### Painted Only

Apply fuzzy skin only to areas that have been manually painted with the [Fuzzy Skin Paint Tool]({{L1}}).  
This allows for precise control over where the texture is applied, ideal for adding grip to specific areas or creating custom patterns.

### All Walls

Apply fuzzy skin to every wall (external and internal). This gives the strongest overall textured appearance but will increase slicing and print time considerably.

### Disabled

The default. No fuzzy skin is applied, not even on areas painted with the [Fuzzy Skin Paint Tool]({{L2}}), and the other fuzzy skin settings are hidden.  
This is what sets it apart from [Painted Only]({{L3}}), which applies fuzzy skin to the painted areas only. If you paint an object while fuzzy skin is disabled, the paint tool warns that the painting won't take effect and offers to switch that object to Painted Only.

## Fuzzy Skin Generator Mode

{{M2}}
Select the underlying method used to produce the fuzzy effect. Each mode has different trade-offs for strength, speed and mechanical load.

### Displacement

{{I1}}

The classic method, where the pattern on the walls is created by shifting the print head perpendicular to the wall.  
It gives a predictable result, but it reduces the strength of the whole shell and opens pores inside the walls. It also increases the mechanical stress on the printer's kinematics and slows down printing overall.

### Extrusion

{{I2}}

The fuzzy skin effect is created by varying the amount of extruded plastic while the print head follows the original path. There is no extra load on the kinematics, no decrease in print speed, and no pores open, but the pattern is about half as pronounced. It is suitable for creating "loose" walls that reduce internal stress in the extruded plastic, or for masking print defects on the side walls with a matte effect.

> [!CAUTION]
> In this mode, **Fuzzy skin thickness** sets how much the line width varies. A line can't be extruded thinner than about 23% of the layer height, so Orca clamps the thinnest parts to that minimum. Once the thickness exceeds the wall line width, higher values only make the wide parts wider.  
> The [Arachne]({{L4}}) wall generator must also be enabled.

### Combined

{{I3}}

This is a combination of the Displacement and Extrusion modes. The pattern is as sharp as in Displacement mode, but the walls remain strong and tight. The load on the kinematics is halved. Printing is faster than in Displacement mode, but still slower than in Extrusion mode.

> [!WARNING]
> The limits on line thickness and the Arachne requirement are the same as in the Extrusion mode.

## Noise Type

{{M3}}
Select the noise algorithm used to generate the random offsets. Different noise types produce distinct visual textures.

### Classic

Simple uniform random noise. Produces a coarse, irregular texture.

{{I4}}

### Perlin

[Perlin noise]({{L5}}) generates smooth, natural-looking variations with coherent structure.

{{I5}}

### Billow

Billow noise is similar to Perlin noise, but has a clumpier appearance. It can create more pronounced features and is often used for natural textures.

{{I6}}

### Ridged Multifractal

Creates sharp, jagged features and high-contrast detail. Useful for stone- or marble-like textures.

{{I7}}

### Voronoi

[Voronoi noise]({{L6}}) divides the surface into Voronoi cells and displaces each cell independently, creating a patchwork or cellular texture.

{{I8}}

### Ripple

The Ripple noise type creates a regular, wave-like pattern of ripples across the surface.  
This is useful for decorative purposes on models that do not have abrupt changes in geometry or holes that create multiple print islands (closed loops), since the number of ripples is applied to each closed loop and can cause discontinuities between layers.

A clear example is a 3DBenchy, whose windows create small print islands that get the same number of ripples as the hull of the boat, where there is much more space for them.

{{I9}}
{{I10}}

#### Ripples per layer

{{M4}}
Controls how many full cycles of ripples will be added per layer.

#### Ripple offset

{{M5}}
Shifts the ripple phase forward along the print path by the specified percentage of a wavelength each layer period. Values are specified between 0% and 100% (0% = no shift, 100% = a full-wavelength shift).

- 0% keeps every layer identical.
- 50% shifts the pattern by half a wavelength, effectively inverting the phase.
- 100% shifts the pattern by a full wavelength, returning to the original phase.

The shift is applied once every number of layers set by [Layers between ripple offset]({{L7}}), so layers within the same group are printed identically.

#### Layers between ripple offset

{{M6}}
Specifies how many consecutive layers share the same ripple phase before the offset is applied.  
For example, with the default 50% [Ripple offset]({{L8}}):

- 1 = Layer 1 is printed with the base ripple pattern, then layer 2 is shifted by the configured offset, then layer 3 returns to the base pattern, and so on.
- 3 = Layers 1 to 3 are printed with the base ripple pattern, then layers 4 to 6 are shifted by the configured offset, then layers 7 to 9 return to the base pattern, etc.

## Point distance

{{M7}}
Average distance between random sample points along each line segment.  
Smaller values add more detail and increase computation; larger values produce coarser, faster results.

## Skin thickness

{{M8}}
Maximum lateral width (in mm) over which points can be displaced. This defines how far the wall can be jittered.  
Keep this below or near your outer wall line width and within nozzle/flow limits for reliable prints.

## Skin feature size

{{M9}}
Base size of coherent noise features, in mm. Larger values yield bigger, more prominent structures; smaller values give fine-grained texture.

## Skin Noise Octaves

{{M10}}
The number of octaves of coherent noise to use. Higher values increase the detail of the noise, but also increase computation time.

## Skin Noise Persistence

{{M11}}
Controls how amplitude decays across octaves. Lower persistence results in smoother noise; higher persistence keeps finer-scale detail stronger.

## Apply fuzzy skin to first layer

{{M12}}
Enable to apply fuzzy skin to the first layer.

> [!CAUTION]
> Can impact bed adhesion and surface contact.

## Credits

- **Generator Mode author:** [@pi-squared-studio]({{L9}}).
