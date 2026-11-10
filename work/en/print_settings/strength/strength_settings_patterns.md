# Patterns

Patterns determine how material is distributed within a print. Different patterns can affect strength, flexibility and print speed using the same density setting.  
The infill pattern also impacts the uniformity of the layer times, since the patterns may be constant, or present significant variations between adjacent layers.

There is no one-size-fits-all solution, as the best pattern depends on the specific print and its requirements.

Many patterns may look similar and have similar overall specifications, but they can behave very differently in practice.  
As with most settings in 3D printing, experience is the best way to determine which pattern works best for your specific needs.

> [!TIP]
> Quickly compare patterns with the [Patterns Quick Reference Table]({{L1}}).

## Analysis parameters

The ratings are the mean of a 100 mm cube, a 3DBenchy and the Stanford bunny, sliced on a Qidi Q2 with a 0.4 mm nozzle, the 0.20mm Standard profile and QIDI PLA Rapido at 5, 15, 30 and 50% sparse infill density, measuring only the sparse infill and the travel in the layers that print it, and compared with each other on the same model and density. The patterns that only print solid infill are measured on their internal solid infill at 100% and rated against the other solid infill patterns. See the [Patterns Quick Reference]({{L2}}) for how the analysis was made.

### Strength

- **X-Y Direction**: The strength of the print in the "Horizontal" X-Y plane. Affected by the pattern's connections between walls, contact between layers, and path.
- **Z Direction**: The strength of the print in the "Vertical" Z direction. Affected by contact between layers.

### Material Usage

Not all patterns use the same amount of material due to their **Density Calculations** and adjustments to the paths.  
This leads to patterns that do not use the specified percentage but rather variations of it.

### Print Time

Print time can vary significantly between patterns due to differences in their pathing and infill strategies.  
Some patterns may complete faster due to more efficient use of the print head's movement, while others may take longer due to more complex paths.

> [!NOTE]
> These are OrcaSlicer's own time estimates, the ones its preview shows.  
> A printer's real times can differ, especially with complex patterns.

### Layer Time Variability

Layer time variability refers to the differences in time it takes to print each layer of a pattern. Some patterns may have consistent layer times, while others may experience significant fluctuations. These variations can potentially impact the outer appearance of the print due to differences in cooling and material flow between layers.  
It is measured on the cube alone, whose layers all have the same shape, so that the changes come from the pattern and not from the model.

{{I1}}

### Slicing Time

How long OrcaSlicer takes to slice each run and write its G-code, from the command line and one run at a time. Patterns with more and shorter lines take longer to generate, order and write.  
It depends on the computer, so only the comparison between patterns applies.

### G-code Size

The size of each run's G-code file. Patterns made of many short moves give larger files, which take longer to send to the printer.

### Multiline

The patterns that support [Fill Multiline]({{L3}}) are also rated with 2 and 3 lines. **Print Time** is rated like the pattern's own, against the other patterns printed with one line, followed by how much faster or slower it is than the same pattern printed with one line on the same model and density.

## Monotonic

[Rectilinear]({{L4}}) in a uniform direction for a smoother visual surface.

- **Strength**
    - **Horizontal (X-Y):** Normal {{I2}}
    - **Vertical (Z):** Normal {{I3}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I4}}
    - **Print Time:** Low {{I5}}
        - **Material/Time (Higher better):** Normal-High {{I6}}
        - **Layer time Variability:** None
    - **Slicing Time:** Low {{I7}}
    - **G-code Size:** Extra-Low {{I8}}
- **Extra:**
    - **[Multiline]({{L5}}):** N/A
    - **[Symmetric infill Y axis]({{L6}}):** N/A
    - **[Smooth Factor]({{L7}}):** N/A
- **Applies to:**
    - **[Solid Infill]({{L8}})**
    - **[Surface]({{L9}})**

{{I9}}

## Monotonic line

[Monotonic]({{L10}}) but avoids overlapping with the perimeter, reducing excess material at joints. May introduce visible seams and increase print time.

- **Strength**
    - **Horizontal (X-Y):** Normal {{I10}}
    - **Vertical (Z):** Normal {{I11}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I12}}
    - **Print Time:** Normal-Low {{I13}}
        - **Material/Time (Higher better):** Normal-High {{I14}}
        - **Layer time Variability:** None
    - **Slicing Time:** Low {{I15}}
    - **G-code Size:** Extra-Low {{I16}}
- **Extra:**
    - **[Multiline]({{L11}}):** N/A
    - **[Symmetric infill Y axis]({{L12}}):** N/A
    - **[Smooth Factor]({{L13}}):** N/A
- **Applies to:**
    - **[Solid Infill]({{L14}})**
    - **[Surface]({{L15}})**

{{I17}}

## Rectilinear

Parallel lines spaced according to infill density. Each layer is printed perpendicular to the previous, resulting in low vertical bonding. Consider using [Zig Zag]({{L16}}) infill instead.

- **Strength**
    - **Horizontal (X-Y):** Normal-Low {{I18}}
    - **Vertical (Z):** Low {{I19}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I20}}
    - **Print Time:** Normal-Low {{I21}}
        - **Material/Time (Higher better):** Normal-High {{I22}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I23}}
    - **G-code Size:** Extra-Low {{I24}}
- **Extra:**
    - **[Multiline]({{L17}}):** [Classic]({{L18}})
        - **2 lines:** Print Time Normal-Low {{I25}} (4% Faster over single line)
        - **3 lines:** Print Time Normal-Low {{I26}} (6% Faster over single line)
    - **[Symmetric infill Y axis]({{L19}}):** No
    - **[Smooth Factor]({{L20}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L21}})**
    - **[Solid Infill]({{L22}})**
    - **[Surface]({{L23}})**
    - **[Ironing]({{L24}})**
    - **[Support Base]({{L25}})**
    - **[Support Interface]({{L26}})**

{{I27}}

## Aligned Rectilinear

Parallel lines spaced by the infill spacing, each layer printed in the same direction as the previous layer. Good horizontal strength perpendicular to the lines, but very poor in the parallel direction.
Recommended with layer anchoring to improve non-perpendicular strength.

- **Strength**
    - **Horizontal (X-Y):** Normal-Low {{I28}}
    - **Vertical (Z):** Normal {{I29}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I30}}
    - **Print Time:** Normal-Low {{I31}}
        - **Material/Time (Higher better):** Normal-High {{I32}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I33}}
    - **G-code Size:** Extra-Low {{I34}}
- **Extra:**
    - **[Multiline]({{L27}}):** [Classic]({{L28}})
        - **2 lines:** Print Time Normal-Low {{I35}} (4% Faster over single line)
        - **3 lines:** Print Time Normal-Low {{I36}} (6% Faster over single line)
    - **[Symmetric infill Y axis]({{L29}}):** No
    - **[Smooth Factor]({{L30}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L31}})**
    - **[Solid Infill]({{L32}})**
    - **[Surface]({{L33}})**

{{I37}}

## Zig Zag

Similar to [rectilinear]({{L34}}), with a consistent pattern between layers.

- **Strength**
    - **Horizontal (X-Y):** Normal-Low {{I38}}
    - **Vertical (Z):** Low {{I39}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I40}}
    - **Print Time:** Normal-Low {{I41}}
        - **Material/Time (Higher better):** Normal-High {{I42}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I43}}
    - **G-code Size:** Extra-Low {{I44}}
- **Extra:**
    - **[Multiline]({{L35}}):** No
    - **[Symmetric infill Y axis]({{L36}}):** Yes
    - **[Smooth Factor]({{L37}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L38}})**

{{I45}}

## Cross Zag

{{M1}}
Similar to [Zig Zag]({{L39}}), but each layer is shifted by the **Infill shift step** parameter.

- **Strength**
    - **Horizontal (X-Y):** Normal {{I46}}
    - **Vertical (Z):** Low {{I47}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I48}}
    - **Print Time:** Normal-Low {{I49}}
        - **Material/Time (Higher better):** Normal-High {{I50}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I51}}
    - **G-code Size:** Extra-Low {{I52}}
- **Extra:**
    - **[Multiline]({{L40}}):** No
    - **[Symmetric infill Y axis]({{L41}}):** Yes
    - **[Smooth Factor]({{L42}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L43}})**

{{I53}}

## Locked Zag

{{M2}}
Version of [Zig Zag]({{L44}}) that adds extra skin.
When using this fill, you can individually modify the density of the skeleton and skin, as well as the size of the skin and how much interconnection there is between the skin and the skeleton (a lock depth of 50% of the skin depth is recommended).  
**Skin line width** and **Skeleton line width** set the line width of the skin and skeleton paths. If expressed as a %, they are computed over the nozzle diameter.  
The **Infill shift step** of [Cross Zag]({{L45}}) also applies to Locked Zag, but it only shifts the skin. The skeleton is not shifted.

- **Strength**
    - **Horizontal (X-Y):** Normal-Low {{I54}}
    - **Vertical (Z):** Normal-Low {{I55}}
- **Density Calculation:** Similar to [Zig Zag]({{L46}}).
Skeleton density * (Infill area - Skin area + Lock depth area) + (Skin density * Skin area).
    - **Material Usage:** Ultra-High {{I56}}
    - **Print Time:** Extra-High {{I57}}
        - **Material/Time (Higher better):** Normal {{I58}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal {{I59}}
    - **G-code Size:** Normal-High {{I60}}
- **Extra:**
    - **[Multiline]({{L47}}):** No
    - **[Symmetric infill Y axis]({{L48}}):** Yes
    - **[Smooth Factor]({{L49}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L50}})**

{{I61}}

## Line

Similar to [rectilinear]({{L51}}), but each line is slightly rotated to improve print speed.

- **Strength**
    - **Horizontal (X-Y):** Low {{I62}}
    - **Vertical (Z):** Low {{I63}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I64}}
    - **Print Time:** Normal-Low {{I65}}
        - **Material/Time (Higher better):** High {{I66}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I67}}
    - **G-code Size:** Extra-Low {{I68}}
- **Extra:**
    - **[Multiline]({{L52}}):** No
    - **[Symmetric infill Y axis]({{L53}}):** No
    - **[Smooth Factor]({{L54}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L55}})**

{{I69}}

## Grid

Two sets of perpendicular lines on every layer, forming a grid. Overlapping points may cause noise or artifacts.

- **Strength**
    - **Horizontal (X-Y):** High {{I70}}
    - **Vertical (Z):** High {{I71}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I72}}
    - **Print Time:** Normal-Low {{I73}}
        - **Material/Time (Higher better):** Normal-High {{I74}}
        - **Layer time Variability:** Unnoticeable
    - **Slicing Time:** Normal-Low {{I75}}
    - **G-code Size:** Extra-Low {{I76}}
- **Extra:**
    - **[Multiline]({{L56}}):** [Non-Crossing]({{L57}})
        - **2 lines:** Print Time High {{I77}} (78% Slower over single line)
        - **3 lines:** Print Time Normal-High {{I78}} (57% Slower over single line)
    - **[Symmetric infill Y axis]({{L58}}):** No
    - **[Smooth Factor]({{L59}}):** [Multiline]({{L60}}) only
- **Applies to:**
    - **[Sparse Infill]({{L61}})**
    - **[Support Interface]({{L62}})**

{{I79}}

## Triangles

Triangle-based grid, offering strong X-Y strength but with triple overlaps at intersections.

- **Strength**
    - **Horizontal (X-Y):** High {{I80}}
    - **Vertical (Z):** Normal {{I81}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I82}}
    - **Print Time:** Normal-Low {{I83}}
        - **Material/Time (Higher better):** Normal-High {{I84}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I85}}
    - **G-code Size:** Extra-Low {{I86}}
- **Extra:**
    - **[Multiline]({{L63}}):** [Non-Crossing]({{L64}})
        - **2 lines:** Print Time Normal {{I87}} (32% Slower over single line)
        - **3 lines:** Print Time Normal-Low {{I88}} (21% Slower over single line)
    - **[Symmetric infill Y axis]({{L65}}):** No
    - **[Smooth Factor]({{L66}}):** [Multiline]({{L67}}) only
- **Applies to:**
    - **[Sparse Infill]({{L68}})**

{{I89}}

## Tri-hexagon

Similar to the [triangles]({{L69}}) pattern but offset to prevent triple overlaps at intersections. This design combines triangles and hexagons, providing excellent X-Y strength.

- **Strength**
    - **Horizontal (X-Y):** High {{I90}}
    - **Vertical (Z):** Normal-High {{I91}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I92}}
    - **Print Time:** Low {{I93}}
        - **Material/Time (Higher better):** Normal-High {{I94}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I95}}
    - **G-code Size:** Extra-Low {{I96}}
- **Extra:**
    - **[Multiline]({{L70}}):** [Non-Crossing]({{L71}})
        - **2 lines:** Print Time High {{I97}} (87% Slower over single line)
        - **3 lines:** Print Time Normal-High {{I98}} (61% Slower over single line)
    - **[Symmetric infill Y axis]({{L72}}):** No
    - **[Smooth Factor]({{L73}}):** [Multiline]({{L74}}) only
- **Applies to:**
    - **[Sparse Infill]({{L75}})**

{{I99}}

## Cubic

3D cube pattern with corners facing down, distributing force in all directions. Triangles in the horizontal plane provide good X-Y strength.

- **Strength**
    - **Horizontal (X-Y):** High {{I100}}
    - **Vertical (Z):** High {{I101}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I102}}
    - **Print Time:** Normal-Low {{I103}}
        - **Material/Time (Higher better):** Normal-High {{I104}}
        - **Layer time Variability:** Unnoticeable
    - **Slicing Time:** Normal-Low {{I105}}
    - **G-code Size:** Extra-Low {{I106}}
- **Extra:**
    - **[Multiline]({{L76}}):** [Non-Crossing]({{L77}})
        - **2 lines:** Print Time Normal-High {{I107}} (68% Slower over single line)
        - **3 lines:** Print Time Normal-High {{I108}} (51% Slower over single line)
    - **[Symmetric infill Y axis]({{L78}}):** No
    - **[Smooth Factor]({{L79}}):** [Multiline]({{L80}}) only
- **Applies to:**
    - **[Sparse Infill]({{L81}})**

{{I109}}

## Adaptive Cubic

[Cubic]({{L82}}) pattern with adaptive density: denser near walls, sparser in the center. Saves material and time while maintaining strength, ideal for large prints.

- **Strength**
    - **Horizontal (X-Y):** Normal-High {{I110}}
    - **Vertical (Z):** Normal-High {{I111}}
- **Density Calculation:** Same as [Cubic]({{L83}}) but reduced in the center
    - **Material Usage:** Low {{I112}}
    - **Print Time:** Low {{I113}}
        - **Material/Time (Higher better):** Normal-Low {{I114}}
        - **Layer time Variability:** Possibly Noticeable
    - **Slicing Time:** Normal {{I115}}
    - **G-code Size:** Extra-Low {{I116}}
- **Extra:**
    - **[Multiline]({{L84}}):** [Non-Crossing]({{L85}})
        - **2 lines:** Print Time Normal-Low {{I117}} (50% Slower over single line)
        - **3 lines:** Print Time Normal-Low {{I118}} (46% Slower over single line)
    - **[Symmetric infill Y axis]({{L86}}):** No
    - **[Smooth Factor]({{L87}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L88}})**

{{I119}}

## Quarter Cubic

[Cubic]({{L89}}) pattern with extra internal divisions, improving X-Y strength.

- **Strength**
    - **Horizontal (X-Y):** High {{I120}}
    - **Vertical (Z):** High {{I121}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I122}}
    - **Print Time:** Normal-Low {{I123}}
        - **Material/Time (Higher better):** Normal-High {{I124}}
        - **Layer time Variability:** Unnoticeable
    - **Slicing Time:** Normal {{I125}}
    - **G-code Size:** Extra-Low {{I126}}
- **Extra:**
    - **[Multiline]({{L90}}):** [Non-Crossing]({{L91}})
        - **2 lines:** Print Time Normal-High {{I127}} (65% Slower over single line)
        - **3 lines:** Print Time Normal {{I128}} (45% Slower over single line)
    - **[Symmetric infill Y axis]({{L92}}):** No
    - **[Smooth Factor]({{L93}}):** [Multiline]({{L94}}) only
- **Applies to:**
    - **[Sparse Infill]({{L95}})**

{{I129}}

## Support Cubic

Support Cubic is a variation of the [Cubic]({{L96}}) infill pattern that is specifically designed to support top layers. It uses more material than Lightning infill but provides better strength. Nevertheless, it is still a low-density infill pattern.

- **Strength**
    - **Horizontal (X-Y):** Low {{I130}}
    - **Vertical (Z):** Low {{I131}}
- **Density Calculation:** % of layer before top shell layers
    - **Material Usage:** Low {{I132}}
    - **Print Time:** Low {{I133}}
        - **Material/Time (Higher better):** Normal-Low {{I134}}
        - **Layer time Variability:** Likely Noticeable
    - **Slicing Time:** Normal-Low {{I135}}
    - **G-code Size:** Extra-Low {{I136}}
- **Extra:**
    - **[Multiline]({{L97}}):** [Non-Crossing]({{L98}})
        - **2 lines:** Print Time Low {{I137}} (55% Slower over single line)
        - **3 lines:** Print Time Low {{I138}} (71% Slower over single line)
    - **[Symmetric infill Y axis]({{L99}}):** No
    - **[Smooth Factor]({{L100}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L101}})**

{{I139}}

## Lightning

{{M3}}
Ultra-fast, ultra-low material infill. Designed for speed and efficiency, ideal for quick prints or non-structural prototypes.

### Overhang Angle

Similar to the [overhang]({{L102}}) angle used for support generation, but specifically for Lightning infill.  
It determines how far the infill can extend from walls before needing support.

### Prune Angle

Controls how aggressively short/unsupported branches of the Lightning infill are pruned.  
A higher angle will result in more pruning, while a lower angle will keep longer branches.

### Straightening Angle

Limits how far junctions in the Lightning infill can be moved to straighten lines.  
Using a low value will result in a low lateral distortion between layers, but may cause more pruning.  
A higher value will allow for more straightening, improving strength but increasing lateral distortion.

{{I140}}  
{{I141}}  
{{I142}}

- **Strength**
    - **Horizontal (X-Y):** Low {{I143}}
    - **Vertical (Z):** Low {{I144}}
- **Density Calculation:** % of layer before top shell layers
    - **Material Usage:** Ultra-Low {{I145}}
    - **Print Time:** Extra-Low {{I146}}
        - **Material/Time (Higher better):** Extra-Low {{I147}}
        - **Layer time Variability:** Likely Noticeable
    - **Slicing Time:** Normal {{I148}}
    - **G-code Size:** Extra-Low {{I149}}
- **Extra:**
    - **[Multiline]({{L103}}):** [Classic]({{L104}})
        - **2 lines:** Print Time Extra-Low {{I150}} (21% Faster over single line)
        - **3 lines:** Print Time Extra-Low {{I151}} (25% Faster over single line)
    - **[Symmetric infill Y axis]({{L105}}):** No
    - **[Smooth Factor]({{L106}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L107}})**
    - **[Support Base]({{L108}})**

{{I152}}

## Honeycomb

Hexagonal pattern balancing strength and material use. Double walls in each hexagon increase material consumption.

- **Strength**
    - **Horizontal (X-Y):** High {{I153}}
    - **Vertical (Z):** High {{I154}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal-High {{I155}}
    - **Print Time:** Ultra-High {{I156}}
        - **Material/Time (Higher better):** Low {{I157}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-High {{I158}}
    - **G-code Size:** Extra-High {{I159}}
- **Extra:**
    - **[Multiline]({{L109}}):** [Classic]({{L110}})
        - **2 lines:** Print Time Extra-High {{I160}} (19% Faster over single line)
        - **3 lines:** Print Time High {{I161}} (30% Faster over single line)
    - **[Symmetric infill Y axis]({{L111}}):** No
    - **[Smooth Factor]({{L112}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L113}})**
    - **[Support Base]({{L114}})**

{{I162}}

## 3D Honeycomb

This infill tries to generate a printable honeycomb structure by printing squares and octagons maintaining a vertical angle high enough to maintain contact with the previous layer.

### Fill pattern tops

{{M4}}

The square at the top of each cell is left open by default. This option covers those squares.

Whenever the pattern changes its print direction, extra lines are bridged across the squares of the previous layer. This is added on top of the normal pattern, which keeps its structural stability.

- **Disabled (default):** the squares are left open.
- **Enabled:** the squares are covered.

The option is only shown when the [Sparse infill pattern]({{L115}}) is **3D Honeycomb** and the [Sparse infill density]({{L116}}) is above 0%.

Useful for:

- **Functional parts**, for example keeping two channels (air and water) separate.
- **Artistic prints** where the upper surface of the pattern should be filled in.

> [!NOTE]
> It is disabled by default because the direction reversals and non-extrusion moves needed to cover the squares substantially slow down the print.

Behavior with other settings:

- **[Fill Multiline]({{L117}}):** the cover is not multiplied by the number of lines. It is printed as a single zigzag pass, built up over as many layers as there are lines and changing direction on every layer.
- **Density:** the squares get smaller as the density increases (and larger with more [Fill Multiline]({{L118}}) lines). When a square is too small to fit a cover line, none is generated, so the option has no effect at high densities.
- **Line spacing:** the cover lines are intentionally closer together than the line width, so the squares close without gaps.

> [!NOTE]
> The covers are bridges, and small pinholes can remain in them. Test your print if it must be airtight or watertight.

- **Strength**
    - **Horizontal (X-Y):** Normal-High {{I163}}
    - **Vertical (Z):** Normal-High {{I164}}
- **Density Calculation:** Unknown
    - **Material Usage:** Normal-Low {{I165}}
    - **Print Time:** Ultra-High {{I166}}
        - **Material/Time (Higher better):** Low {{I167}}
        - **Layer time Variability:** Unnoticeable
    - **Slicing Time:** Normal-High {{I168}}
    - **G-code Size:** Ultra-High {{I169}}
- **Extra:**
    - **[Multiline]({{L119}}):** [Non-Crossing]({{L120}})
        - **2 lines:** Print Time High {{I170}} (20% Faster over single line)
        - **3 lines:** Print Time High {{I171}} (30% Faster over single line)
    - **[Symmetric infill Y axis]({{L121}}):** No
    - **[Smooth Factor]({{L122}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L123}})**

{{I172}}

## Lateral Honeycomb

{{M5}}
Vertical honeycomb pattern with acceptable torsional stiffness, developed for low-density structures like wings. An improvement over [Lateral Lattice]({{L124}}), it offers the same performance at lower densities. This infill includes an **Infill overhang angle** parameter to improve the contact between layers and reduce the risk of delamination.

- **Strength**
    - **Horizontal (X-Y):** Normal-Low {{I173}}
    - **Vertical (Z):** Normal-Low {{I174}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I175}}
    - **Print Time:** Normal-Low {{I176}}
        - **Material/Time (Higher better):** Normal-High {{I177}}
        - **Layer time Variability:** Possibly Noticeable
    - **Slicing Time:** Normal-Low {{I178}}
    - **G-code Size:** Extra-Low {{I179}}
- **Extra:**
    - **[Multiline]({{L125}}):** [Classic]({{L126}})
        - **2 lines:** Print Time Low {{I180}} (7% Faster over single line)
        - **3 lines:** Print Time Low {{I181}} (10% Faster over single line)
    - **[Symmetric infill Y axis]({{L127}}):** No
    - **[Smooth Factor]({{L128}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L129}})**

{{I182}}

## Lateral Lattice

{{M6}}
Low-strength pattern with good flexibility. You can adjust **Angle 1** and **Angle 2** to optimize the infill for your specific model. Each angle sets the tilt in the Z direction of one of the two sets of lattice elements. 0° is vertical.

- **Strength**
    - **Horizontal (X-Y):** Normal-Low {{I183}}
    - **Vertical (Z):** Low {{I184}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I185}}
    - **Print Time:** Normal-Low {{I186}}
        - **Material/Time (Higher better):** Normal-High {{I187}}
        - **Layer time Variability:** Unnoticeable
    - **Slicing Time:** Normal-Low {{I188}}
    - **G-code Size:** Extra-Low {{I189}}
- **Extra:**
    - **[Multiline]({{L130}}):** [Classic]({{L131}})
        - **2 lines:** Print Time Low {{I190}} (8% Faster over single line)
        - **3 lines:** Print Time Low {{I191}} (10% Faster over single line)
    - **[Symmetric infill Y axis]({{L132}}):** No
    - **[Smooth Factor]({{L133}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L134}})**

{{I192}}

## Cross Hatch

Similar to [Gyroid]({{L135}}) but with linear patterns, creating weak points at internal corners.
Easier to slice but consider using [TPMS-D]({{L136}}) or [Gyroid]({{L137}}) for better strength and flexibility.

- **Strength**
    - **Horizontal (X-Y):** Normal-High {{I193}}
    - **Vertical (Z):** Normal-High {{I194}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I195}}
    - **Print Time:** Normal-High {{I196}}
        - **Material/Time (Higher better):** Normal-Low {{I197}}
        - **Layer time Variability:** Likely Noticeable
    - **Slicing Time:** Normal {{I198}}
    - **G-code Size:** Normal {{I199}}
- **Extra:**
    - **[Multiline]({{L138}}):** [Classic]({{L139}})
        - **2 lines:** Print Time Normal {{I200}} (12% Faster over single line)
        - **3 lines:** Print Time Normal-Low {{I201}} (18% Faster over single line)
    - **[Symmetric infill Y axis]({{L140}}):** No
    - **[Smooth Factor]({{L141}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L142}})**

{{I202}}

## TPMS-D

Triply Periodic Minimal Surface (Schwarz Diamond). Hybrid between [Cross Hatch]({{L143}}) and [Gyroid]({{L144}}), combining rigidity and smooth transitions. Isotropic and strong in all directions. This geometry is faster to slice than Gyroid, but slower than Cross Hatch.

- **Strength**
    - **Horizontal (X-Y):** High {{I203}}
    - **Vertical (Z):** High {{I204}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I205}}
    - **Print Time:** High {{I206}}
        - **Material/Time (Higher better):** Low {{I207}}
        - **Layer time Variability:** Possibly Noticeable
    - **Slicing Time:** High {{I208}}
    - **G-code Size:** Ultra-High {{I209}}
- **Extra:**
    - **[Multiline]({{L145}}):** [Classic]({{L146}})
        - **2 lines:** Print Time Normal-High {{I210}} (14% Faster over single line)
        - **3 lines:** Print Time Normal {{I211}} (22% Faster over single line)
    - **[Symmetric infill Y axis]({{L147}}):** No
    - **[Smooth Factor]({{L148}}):** No
    - **[Adaptive Density]({{L149}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L150}})**

{{I212}}

## TPMS-FK

Triply Periodic Minimal Surface (Fischer–Koch S) pattern. Its smooth, continuous geometry resembles trabecular bone microstructure, offering a balance between rigidity and energy absorption. Compared to [TPMS-D]({{L151}}), it has more complex curvature, which can improve load distribution and shock absorption in functional parts.

- **Strength**
    - **Horizontal (X-Y):** Normal-High {{I213}}
    - **Vertical (Z):** Normal-High {{I214}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I215}}
    - **Print Time:** Extra-High {{I216}}
        - **Material/Time (Higher better):** Low {{I217}}
        - **Layer time Variability:** Possibly Noticeable
    - **Slicing Time:** High {{I218}}
    - **G-code Size:** Ultra-High {{I219}}
- **Extra:**
    - **[Multiline]({{L152}}):** [Classic]({{L153}})
        - **2 lines:** Print Time High {{I220}} (21% Faster over single line)
        - **3 lines:** Print Time Normal-High {{I221}} (31% Faster over single line)
    - **[Symmetric infill Y axis]({{L154}}):** No
    - **[Smooth Factor]({{L155}}):** No
    - **[Adaptive Density]({{L156}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L157}})**

{{I222}}

## Adaptive TPMS

[Gyroid]({{L158}}), [TPMS-D]({{L159}}) and [TPMS-FK]({{L160}}) can grade their density inside the object: fine cells next to the walls and the top and bottom surfaces, where the infill supports the shells, growing continuously towards the center of the object, where they save material and print time.

### Adaptive Density

{{M7}}
Grades the Gyroid and TPMS infill inside the object: its cells grow from the surface of the object towards its center. The [Sparse infill density]({{L161}}) is used at the surface and the [Interior Density]({{L162}}) at the center.

| Mode | Follows | Use it for |
| --- | --- | --- |
| Disabled | Nothing: the regular pattern at the sparse infill density. | |
| Distance warp | The distance to the nearest surface, with one continuous pattern warped around the lobe centers. | A smooth, connected concentric grading; the pattern is sheared in plates and long parts, and long parts are graded partly along their length. |
| Smooth blend | The distance to the nearest surface, with the patterns of neighboring densities blended into each other. | A concentric grading without steps; small loops where the densities blend. |
| Stepped shells | The distance to the nearest surface, including the top and bottom, like concentric shells: each shell gets the regular pattern at its density, about 1.5 times apart, with its lines joined along the shell. | A concentric grading with an undistorted pattern; the density changes in steps. |
| Lobes | The whole 3D shape of the object, including its top and bottom: every lobe, a part joined to the rest by a narrower neck, towards its own center. | Most objects. |
| Normal Z | Each section of the object normal to Z, so the density does not change with the height. | Profiles extruded along Z, like tall prisms and tubes. |
| Normal Y, Normal X | Each section of the object normal to that axis, so the density does not change along it. | Profiles extruded along X or Y, like beams and bars lying on the bed. |

- The object is measured from its slices, so holes, negative parts and the union of overlapping parts are taken into account.
- Every separate body of the object, and every lobe of a body joined to the rest by a neck, like two united spheres, is graded towards its own center, its deepest point. The neck between two lobes is graded halfway. With Lobes, the center of a tall object is at its middle height, so the infill is sparsest there and not along its whole height.
- The lines stay continuous: the pattern is scaled around the center, with round cells at the center and cells flattened along the surface near it.
- The parts that the center cannot reach in a straight line, like the far side of the hole of a ring, keep the sparse infill density.
- In Distance warp, Smooth blend and Stepped shells the interior density is at the point farthest from the surface, so a tall object keeps its whole core sparse and a plate is graded through its thickness. On spheres and cubes, Distance warp is the same as Lobes.
- Smooth blend and Stepped shells print more lines than their target where their densities meet, along the shells or where the patterns blend, so they save less material than Lobes for the same densities.
- In the Normal modes every section is graded the same way within its own outline. Along the axis, the cells keep the interior density, so near the surface they are stretched along the axis. With Normal X or Y, the layers next to the sides stay at the sparse infill density.
- The Gyroid [Z-buckling bias optimization]({{L163}}) does not apply to adaptive infill.
- At a [Sparse infill density]({{L164}}) of 100% the sparse infill is printed solid, so the adaptive options are hidden.
- Objects made only of parts thinner than the field grid cells (0.5 mm, up to a few mm for very large objects) use the regular pattern.

### Interior Density

{{M8}}
Density of the adaptive infill at the center of the object.  
It can also be higher than the sparse infill density, to make the core denser than the surface.

### Adaptive Gradient

{{M9}}
How the density changes from the surface (depth `0`) to the center of the object (depth `1`), where `S` is the sparse infill density and `I` the interior density:

| Gradient | Density at depth `t` | Behavior |
| --- | --- | --- |
| Linear | `S + (I - S) × t` | Changes at a constant rate. |
| Quadratic | `S + (I - S) × t²` | Stays close to the sparse infill density near the surface and changes faster towards the center. Uses the most material when the surface is denser. |
| Exponential | `S × (I / S)ᵗ` | Changes quickly just below the surface and levels off towards the center. Uses the least material when the surface is denser. |

## Gyroid

Mathematical, isotropic surface providing equal strength in all directions. Excellent for strong, flexible prints and resin filling due to its interconnected structure. Since it does not contain straight lines over long stretches, it helps reduce warping, as the material's contraction is distributed along its curved lines. This pattern may require more time to slice because of all the points needed to generate each curve. If your model has complex geometry, consider using a simpler infill pattern like [TPMS-D]({{L165}}) or [Cross Hatch]({{L166}}).

### Gyroid Optimized

{{M10}}

Tightens the gyroid wave along the Z (vertical) axis at low infill density to shorten the effective vertical column length and improve Z-axis compression buckling resistance. Filament use is preserved. No effect at ~30% sparse infill density and above. Only applies when Sparse infill pattern is set to Gyroid.

- **Strength**
    - **Horizontal (X-Y):** High {{I223}}
    - **Vertical (Z):** High {{I224}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal-Low {{I225}}
    - **Print Time:** Extra-High {{I226}}
        - **Material/Time (Higher better):** Low {{I227}}
        - **Layer time Variability:** Unnoticeable
    - **Slicing Time:** High {{I228}}
    - **G-code Size:** Ultra-High {{I229}}
- **Extra:**
    - **[Multiline]({{L167}}):** [Classic]({{L168}})
        - **2 lines:** Print Time High {{I230}} (17% Faster over single line)
        - **3 lines:** Print Time Normal-High {{I231}} (29% Faster over single line)
    - **[Symmetric infill Y axis]({{L169}}):** No
    - **[Smooth Factor]({{L170}}):** No
    - **[Adaptive Density]({{L171}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L172}})**

{{I232}}

## Concentric

Fills the area with progressively smaller versions of the outer contour, creating a concentric pattern. Ideal for 100% infill or flexible prints.

- **Strength**
    - **Horizontal (X-Y):** Low {{I233}}
    - **Vertical (Z):** Normal {{I234}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** High {{I235}}
    - **Print Time:** Normal {{I236}}
        - **Material/Time (Higher better):** High {{I237}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-Low {{I238}}
    - **G-code Size:** High {{I239}}
- **Extra:**
    - **[Multiline]({{L173}}):** [Classic]({{L174}})
        - **2 lines:** Print Time Normal-High {{I240}} (18% Slower over single line)
        - **3 lines:** Print Time High {{I241}} (25% Slower over single line)
    - **[Symmetric infill Y axis]({{L175}}):** No
    - **[Smooth Factor]({{L176}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L177}})**
    - **[Solid Infill]({{L178}})**
    - **[Surface]({{L179}})**
    - **[Ironing]({{L180}})**
    - **[Support Interface]({{L181}})**

{{I242}}

## Spiral Inset

Version of [Concentric]({{L182}}) that joins its loops into one continuous spiral: each loop is cut short and runs straight into the next loop inside it, instead of being printed as a separate closed loop.

The outer end of the spiral is at a convex corner of the outer loop, preferably one close to a right angle, and each loop inside it continues from the point nearest to the end of the loop outside it.  
The step from one loop to the next is extruded, not traveled. When the next loop cannot be reached with a short step inside the surface (it belongs to another island, is more than four loop spacings away, or the step would cross a hole or a notch), the spiral ends and a new one starts.

On solid top and bottom surfaces, the loops use variable line widths, as in the [Arachne]({{L183}}) wall generator, to fill the gaps that fixed-width loops would leave. Internal solid infill, support interfaces and surfaces below 100% density use fixed-width loops, and a short line into the center fills the small hole the innermost loop can leave there.  
On top and bottom surfaces, the direction of the spiral is set by [Fill Order]({{L184}}).

- **Strength**
    - **Horizontal (X-Y):** Low {{I243}}
    - **Vertical (Z):** Normal {{I244}}
- **Density Calculation:** Same as [Concentric]({{L185}}).
    - **Material Usage:** Normal {{I245}}
    - **Print Time:** Normal-Low {{I246}}
        - **Material/Time (Higher better):** Normal {{I247}}
        - **Layer time Variability:** None
    - **Slicing Time:** Low {{I248}}
    - **G-code Size:** Normal-Low {{I249}}
- **Extra:**
    - **[Multiline]({{L186}}):** N/A
    - **[Symmetric infill Y axis]({{L187}}):** N/A
    - **[Smooth Factor]({{L188}}):** N/A
- **Applies to:**
    - **[Solid Infill]({{L189}})**
    - **[Surface]({{L190}})**
    - **[Support Interface]({{L191}})**

## Hilbert Curve

Hilbert Curve is a space-filling curve that can be used to create a continuous infill pattern. It is known for its aesthetic appeal and ability to fill space efficiently.
Print speed is very low due to the complexity of the path, which can lead to longer print times. It is not recommended for structural parts but can be used for aesthetic purposes.

- **Strength**
    - **Horizontal (X-Y):** Low {{I250}}
    - **Vertical (Z):** Normal {{I251}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I252}}
    - **Print Time:** Extra-High {{I253}}
        - **Material/Time (Higher better):** Low {{I254}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-High {{I255}}
    - **G-code Size:** High {{I256}}
- **Extra:**
    - **[Multiline]({{L192}}):** [Classic]({{L193}})
        - **2 lines:** Print Time High {{I257}} (20% Faster over single line)
        - **3 lines:** Print Time Normal-High {{I258}} (31% Faster over single line)
    - **[Symmetric infill Y axis]({{L194}}):** No
    - **[Smooth Factor]({{L195}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L196}})**
    - **[Solid Infill]({{L197}})**
    - **[Surface]({{L198}})**

{{I259}}

## Archimedean Chords

Spiral pattern that fills the area with concentric arcs, creating a smooth and continuous infill. Can be filled with resin thanks to its interconnected hollow structure, which allows the resin to flow through it and cure properly.

- **Strength**
    - **Horizontal (X-Y):** Low {{I260}}
    - **Vertical (Z):** Normal {{I261}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I262}}
    - **Print Time:** Normal-Low {{I263}}
        - **Material/Time (Higher better):** Normal-High {{I264}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal-High {{I265}}
    - **G-code Size:** Extra-High {{I266}}
- **Extra:**
    - **[Multiline]({{L199}}):** [Classic]({{L200}})
        - **2 lines:** Print Time Low {{I267}} (3% Faster over single line)
        - **3 lines:** Print Time Low {{I268}} (7% Faster over single line)
    - **[Symmetric infill Y axis]({{L201}}):** No
    - **[Smooth Factor]({{L202}}):** No
- **Applies to:**
    - **[Sparse Infill]({{L203}})**
    - **[Solid Infill]({{L204}})**
    - **[Surface]({{L205}})**

{{I269}}

## Octagram Spiral

Aesthetic pattern with low strength and high print time.

- **Strength**
    - **Horizontal (X-Y):** Low {{I270}}
    - **Vertical (Z):** Normal {{I271}}
- **Density Calculation:**  % of  total infill volume
    - **Material Usage:** Normal {{I272}}
    - **Print Time:** Normal {{I273}}
        - **Material/Time (Higher better):** Normal-Low {{I274}}
        - **Layer time Variability:** None
    - **Slicing Time:** Normal {{I275}}
    - **G-code Size:** Low {{I276}}
- **Extra:**
    - **[Multiline]({{L206}}):** [Classic]({{L207}})
        - **2 lines:** Print Time Normal {{I277}} (4% Faster over single line)
        - **3 lines:** Print Time Normal-Low {{I278}} (9% Faster over single line)
    - **[Symmetric infill Y axis]({{L208}}):** No
    - **[Smooth Factor]({{L209}}):** Yes
- **Applies to:**
    - **[Sparse Infill]({{L210}})**
    - **[Solid Infill]({{L211}})**
    - **[Surface]({{L212}})**

{{I279}}
