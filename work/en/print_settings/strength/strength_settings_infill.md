# Infill

Infill is the internal structure of a 3D print, providing strength and support. It can be adjusted to balance material usage, print time, and part strength.

{{T1}}

## Sparse infill density

{{M1}}
Infill density determines the amount of material used to fill the interior of a 3D print. It is usually expressed as a percentage, with 100% being completely solid.

- Higher density increases
    - Strength
    - Material usage
    - Print time.

> [!NOTE]
> Density is usually calculated as a percentage of the total infill volume, not the total print volume.  
> Nevertheless, **not all patterns interpret density the same way**, so the actual material usage may vary.  
> You can see each pattern's material usage in the [Patterns section]({{L1}}).

## Fill Multiline

{{M2}}
This setting allows the selected [infill pattern]({{L2}}) to be generated using up to 10 parallel extrusion lines per path, while preserving both the defined [infill density]({{L3}}) and the overall material usage.

To check which patterns support multiline infill, see the Patterns Quick Reference table in the [Infill Patterns Wiki List]({{L4}}) or each pattern's specifics in the [Patterns section]({{L5}}).

{{I1}}

> [!NOTE]
> Orca's approach is different from other slicers that simply multiply the number of lines and material usage, generating a denser infill than expected.  
> Orca Slicer keeps the cross-section constant for the set density.
>
>| Infill   Density % | Infill Lines | Orca Density | Other Slicers Density |
>|--------------------|--------------|--------------|-----------------------|
>| 10%                | 2            | 10%          | 20%                   |
>| 25%                | 2            | 25%          | 50%                   |
>| 40%                | 2            | 40%          | 80%                   |
>| 10%                | 3            | 10%          | 30%                   |
>| 25%                | 3            | 25%          | 75%                   |
>| 40%                | 3            | 40%          | 100%                  |
>| 10%                | 5            | 10%          | 50%                   |
>| 25%                | 5            | 25%          | 100%                  |
>| 40%                | 5            | 40%          | 100%                  |

### Use cases

- Increasing the number of lines (e.g., 2 or 3) can **improve part strength** and **print speed** without increasing material usage.
- **Fire-retardant applications:** Some flame-resistant materials (like PolyMax PC-FR) require a minimum printed wall/infill thickness—often 1.5–3 mm—to comply with standards. Since infill contributes to overall part thickness, using multiple lines helps achieve the necessary thickness without switching to a large nozzle or printing with 100% infill. This is especially useful for high-temperature materials like PC, which are prone to warping when fully solid.
- Creating **aesthetic** infill patterns (like [Grid]({{L6}}) or [Honeycomb]({{L7}})) with multiple line widths—without relying on CAD modeling or being limited to a single extrusion width.
- Increasing stability for weak infill patterns like [Lightning]({{L8}}).  
- Printing gears and other mechanisms, because multiline infill transfers torque better.  

{{I2}}

### Print time

With more lines, the pattern is laid out that many times larger and each of its lines is printed as that many parallel lines, so the same density prints the same length of line. That length has fewer corners and gentler curves, where the nozzle has to slow down, and the lines of a group end next to each other, where they are joined instead of traveling between them.

In the [infill analysis]({{L9}}), more lines usually printed faster:

- Curved and angular patterns gain the most: [Gyroid]({{L10}}), [TPMS-D]({{L11}}), [TPMS-FK]({{L12}}), [Honeycomb]({{L13}}), [3D Honeycomb]({{L14}}) and [Hilbert Curve]({{L15}}) printed 15-21% faster with 2 lines and 23-32% faster with 3.
- The other patterns whose lines do not cross printed 3-26% faster.
- Patterns whose lines cross take longer: the [Non-Crossing]({{L16}}) paths of [Grid]({{L17}}), [Triangles]({{L18}}), [Tri-hexagon]({{L19}}), [Cubic]({{L20}}), [Quarter Cubic]({{L21}}), [Adaptive Cubic]({{L22}}) and [Support Cubic]({{L23}}) turn at every crossing instead of running straight across. They took 21-87% longer than with 1 line, and [Concentric]({{L24}}) 16-22% longer.

Each pattern's 2 and 3 lines entries in the [Patterns section]({{L25}}) show its own print time over a single line.

> [!TIP]
> Three other settings cut the time of the sparse infill, with or without multiline:
>
> - [Reduce Infill Retraction]({{L26}}) skips the retraction, wipe and Z-hop of travels that stay inside the infill, where oozing can't be seen. Each skipped retraction saves tens of milliseconds, which add up over the thousands of infill travels of a large print.
> - [Infill Combination]({{L27}}) prints the sparse infill of several layers as one thicker layer, while the walls keep the original layer height. Fewer, thicker layers mean fewer infill moves for the same volume.
> - [Sparse Infill Smooth Factor]({{L28}}) rounds the corners of the sparse infill path, so the toolhead keeps more of its speed through the turns. At `100%` it shortened the infill print time of the patterns that support it by 4-25% (see [how much for each pattern]({{L29}})), at the cost of a larger G-code file, which its [vertex budget]({{L30}}) keeps in check.

### Strategy

The way multiple lines are generated depends on the selected infill pattern.  
The following describes possible strategies for infill generation.

#### Classic Strategy

For most self-intersecting infills (e.g. [Gyroid]({{L31}})) multiline will generate closed loops to avoid overlapping lines. This may lead to some increased print time.  

In this example of a pattern of crossing lines and the [Gyroid]({{L32}}) pattern, you can see (in purple) the closed loops generated to avoid overlapping lines.

{{I3}}

#### Non-Crossing Strategy

[Grid]({{L33}}), [Triangles]({{L34}}), [Tri-hexagon]({{L35}}), [Cubic]({{L36}}), [Quarter Cubic]({{L37}}), [Adaptive Cubic]({{L38}}) & [Support Cubic]({{L39}}) patterns use a Non-crossing multiline strategy.
For these infill patterns, an alternative approach is used, generating trapezoidal trajectories designed to avoid self-intersections of the infill lines. In each layer, the pattern rotates to ensure isotropic strength.  
This strategy improves printing times by avoiding closed loops in favor of continuous printing paths.  
[3D Honeycomb]({{L40}}) is also non-crossing: it draws its multiline copies itself as parallel waves that never cross.  

> [!IMPORTANT]
> NEW FEATURE: **Non-Crossing Quarter Cubic**  
> Available in: [Nightly builds]({{L41}}) or Releases greater than **2.5.0**.

- [Cubic]({{L42}}) paths follow the same lines as its single-line pattern, so they still shift with the layer height: most layers look like [Tri-hexagon]({{L43}}), and the layers where the three line directions meet look like [Triangles]({{L44}}).
- [Quarter Cubic]({{L45}}) paths also follow the same lines as its single-line pattern. Parallel lines still come together until their walls touch, and where they are too close for a path to turn, it runs straight from one to the other.
- [Adaptive Cubic]({{L46}}) and [Support Cubic]({{L47}}) paths follow their lines of every cube size. Where a finer line ends on a coarser one, its path stops against the path of the coarser line.

{{I4}}

## Direction and Rotation

These settings control the orientation of the sparse and solid infill lines to optimize strength and material usage.

### Direction

{{M3}}
Controls the direction of the infill lines to optimize or strengthen the print.

[Adaptive Cubic]({{L48}}) and [Support Cubic]({{L49}}) do not support rotation, so the sparse infill direction and the sparse infill [rotation template]({{L50}}) are disabled for them. The solid infill direction and rotation template are not affected.

{{I5}}

> [!TIP]
> Enable [Align directions to model]({{L51}}) to make this direction follow the model's orientation on the build plate.

### Rotation

This parameter sets the sparse (or solid) infill direction for each layer according to the specified template. When a template is set, the matching [Direction]({{L52}}) setting is ignored.  
The template is a comma-separated list of angles in degrees.

For example:

{{C1}}

{{I6}}

The first layer uses 0°, the second uses 90°, and the pattern repeats for subsequent layers.

Other examples:

{{C2}}

{{C3}}

> [!NOTE]
> If there are more layers than angles, the sequence repeats.

> [!TIP]
> You can use [Template Metalanguage for infill rotation]({{L53}}) to create more complex patterns.

> [!IMPORTANT]
> Not all sparse [patterns]({{L54}}) support rotation.

### Symmetric infill Y axis

{{M4}}
When enabled, the infill pattern is mirrored about an axis parallel to the Y axis that passes through the center of the object. This can help achieve more uniform strength distribution in certain geometries.

> [!IMPORTANT]
> This setting is only available for the [Zig Zag]({{L55}}), [Cross Zag]({{L56}}) and [Locked Zag]({{L57}}) patterns.

You can apply this setting with multiple objects or using modifiers to control infill orientation for different parts of your print.  
For example, you might want to mirror the infill pattern of symmetric components, like airplane wings or boat hulls, to enhance their structural integrity without needing a 45° rotation.

{{I7}}

## Infill Wall Overlap

{{M5}}
Infill area is enlarged slightly to overlap with wall for better bonding. The percentage value is approximately relative to the inner wall line width. More precisely, it is relative to half the inner wall line spacing plus half the internal solid infill line spacing with the [Classic]({{L58}}) wall generator, and to the inner wall line spacing with [Arachne]({{L59}}) (the outer wall line spacing in both cases where only one wall is printed). Set this value to ~10-15% to minimize potential over-extrusion and accumulation of material resulting in rough surfaces.

- **Infill Wall Overlap Off**

{{I8}}

- **Infill Wall Overlap On**

{{I9}}

## Apply gap fill

{{M6}}
Enables gap fill for the selected solid surfaces.  
The minimum gap length that will be filled can be controlled with the [Filter out tiny gaps]({{L60}}) option.

1. **Everywhere:** Applies gap fill to top, bottom and internal solid surfaces for maximum strength.
2. **Top and bottom surfaces:** Applies gap fill to top and bottom surfaces only, balancing print speed, reducing potential over-extrusion in the solid infill and making sure the top and bottom surfaces have no pinhole gaps.
3. **Nowhere:** Disables gap fill for all solid infill areas.

Note that if using the [classic perimeter generator]({{L61}}), gap fill may also be generated between perimeters, if a full width line cannot fit between them.
That perimeter gap fill is not controlled by this setting.

If you would like all gap fill, including the classic perimeter generated one, removed, set the Filter out tiny gaps value to a large number, like 999999.

However, this is not advised, as gap fill between perimeters contributes to the model's strength. For models where excessive gap fill is generated between perimeters, a better option would be to switch to the [Arachne wall generator]({{L62}}) and use this option to control whether the cosmetic top and bottom surface gap fill is generated.

## Filter out tiny gaps

{{M7}}
Don't print gap fill with a length smaller than the specified threshold (in mm).  
This setting applies to top, bottom and solid infill and, if using the [classic perimeter generator]({{L63}}), to wall gap fill.

## Anchor

{{M8}}
Connect an infill line to an internal perimeter with a short segment of an additional perimeter. If expressed as a percentage (example: 15%), it is calculated over the infill extrusion width.
OrcaSlicer tries to connect two close infill lines to a short perimeter segment. If no such perimeter segment shorter than the Maximum length of the infill anchor is found, the infill line is connected to a perimeter segment at just one side and the length of the perimeter segment taken is limited to the Sparse infill anchor length, but no longer than the Maximum length of the infill anchor. If the Maximum length of the infill anchor is set to 0, the old algorithm for infill connection is used, which should create the same result as 1000 & 0.

When a line end cannot be connected to its neighbor, its anchor runs along the wall toward the nearest free line end, where the next infill path usually starts. Two line ends whose anchors would meet are connected instead. With [multiline]({{L64}}) infill, an anchor stops short of the other lines of its group instead of printing over them.

Line ends left next to each other, about two line widths apart or closer, are joined with a short straight segment so they print as one path, also when the Maximum length of the infill anchor is `0`.

[Concentric]({{L65}}) loops follow the outline of the infill area instead of ending at the walls, so there is nothing to anchor and both settings are hidden for that pattern.  
With the [Line]({{L66}}) pattern both settings are disabled, and the Sparse infill anchor length is also disabled whenever the Maximum length of the infill anchor is `0`.

- **Anchor Off**

{{I10}}

- **Anchor On**

{{I11}}

## Internal Solid Infill

{{M9}}
Line pattern of internal solid infill. If [Detect narrow internal solid infill]({{L67}}) is enabled, the [Concentric pattern]({{L68}}) will be used for small areas.

## Extra Solid Infill

{{M10}}
Insert extra solid infills at specific layers to add strength at critical points in your print. This feature allows you to strategically reinforce your part without changing the overall sparse infill density.

{{I12}}

The pattern supports two formats:

### Interval Pattern

- **Simple interval**: `N` - Insert 1 solid layer every N layers, equal to `N#1`
- **Multiple layers**: `N#K` - Insert K consecutive solid layers every N layers
- **Optional K**: `N#` - Shorthand for `N#1`

Examples:

{{C4}}

### Explicit Layer List

Specify exact layer numbers (1-based) using comma-separated values. Each entry may be a single layer `N` or a range `N#K` to insert K consecutive solid layers starting at layer N:

{{C5}}

> [!NOTE]
>
> - Layer numbers are 1-based (first layer is layer 1)
> - `#K` is optional in both interval and explicit list entries (`N#` equals `N#1`)
> - Solid infill replaces the sparse infill only on the selected layers; all other layers keep the normal sparse infill pattern

> [!TIP]
> Use this feature to:
>
> - Add strength at stress concentration points
> - Reinforce mounting holes or attachment points
> - Create internal structure for functional parts
> - Add periodic reinforcement for tall prints
> - Insert a single solid layer at a specific height by using an explicit list with a leading 0, which will be ignored because layer indices are 1-based. Example: `0,15` inserts a solid layer only at layer 15.

> [!WARNING]
> Layers that include solid infill can take significantly longer than surrounding layers. This time differential may lead to z-banding-like bulges. Consider adjusting cooling or speeds if you observe artifacts.

## Sparse Infill Pattern

{{M11}}
> [!TIP]
> See [Infill Patterns Wiki List]({{L69}}) with **detailed specifications**, including their strengths and weaknesses.

## Sparse Infill Smooth Factor

{{M12}}

Rounds the corners of the sparse infill path, replacing each sharp direction change with a curve that joins the two straight legs meeting at it. The curvature of the curve grows from zero at both legs, so the nozzle eases into and out of the turn instead of snapping into it.  
`0%` keeps the original sharp path, while `100%` produces the largest possible curves between adjacent infill lines. A curve never consumes more than half of the shorter leg on each side of a corner, so the curves of two neighboring corners meet at most at the midpoint of the segment they share and never overlap.

Smoothing the corners reduces plastic shrinkage at each turn and helps keep the nozzle from scratching the infill during travel moves made with little or no Z-hop. It also lets the toolhead keep more of its speed through the turns instead of decelerating into every corner.

Example with the [Octagram Spiral]({{L70}}) pattern:

- **0%:** the original sharp path.

{{I13}}

- **50%:** each curve reaches a quarter of the shorter leg on both sides of the corner.

{{I14}}

- **100%:** the curves of two neighboring corners meet at the midpoint of the segment they share, leaving no straight section between them.

{{I15}}

### How rounded corners are printed

A curve is printed as straight moves, and the printer slows down at each junction between two moves by how much it turns there. A rounded corner is therefore printed as the polygon of the curve's tangents taken at equal steps of direction, so every one of its vertices turns by the same angle.

How many vertices a corner gets follows the [G-code resolution]({{L71}}), like every other path: the fewest that keep the polygon within the resolution of the curve. It depends only on the shape of the corner and the resolution, not on the printer, and a larger curve takes more vertices.

The vertices are what make a rounded corner fast: each one is a slowdown, and the gentler its turn, the less it slows the toolhead. A curve split into a few vertices saves little, and can even print slower than the sharp corner, as the short moves between its vertices leave no room to accelerate.

A curve is only as fast as its sharpest vertex. On a Klipper printer with a square corner velocity of 9 mm/s and 10,000 mm/s² acceleration, a vertex turning by 13.6 degrees allows about 69 mm/s, and one turning by 9 degrees about 104 mm/s. At `100%` the curves of neighboring corners meet on patterns like [Hilbert Curve]({{L72}}), so the whole infill path is curves and runs at that speed rather than at the sparse infill speed. That is why the [G-code resolution]({{L73}}), which sets how finely a curve is split, matters most on those patterns.

### Print time and material

Rounded corners let the toolhead keep more of its speed through the turns, so the infill prints faster. This is how much shorter the print time of the sparse infill was than with `0%`, counting the travel between its lines, in the setup of the [infill analysis]({{L74}}) (the mean of a 100 mm cube, a 3DBenchy and the Stanford bunny at 5, 15, 30 and 50% density, on a Klipper printer):

| Pattern | 25% | 50% | 75% | 100% |
| :-- | --: | --: | --: | --: |
| [Octagram Spiral]({{L75}}) | 9% | 17% | 23% | 29% |
| [3D Honeycomb]({{L76}}) | 3% | 10% | 14% | 21% |
| [Honeycomb]({{L77}}) | 2% | 9% | 13% | 19% |
| [Hilbert Curve]({{L78}}) | 1% | 5% | 9% | 18% |
| [Tri-hexagon]({{L79}}), 3 lines | 4% | 8% | 12% | 16% |
| [Tri-hexagon]({{L80}}), 2 lines | 6% | 11% | 11% | 16% |
| [Cubic]({{L81}}), 3 lines | 3% | 6% | 10% | 13% |
| [Cubic]({{L82}}), 2 lines | 4% | 8% | 9% | 13% |
| [Cross Hatch]({{L83}}) | 2% | 5% | 8% | 12% |
| [Grid]({{L84}}), 3 lines | 1% | 5% | 5% | 10% |
| [Quarter Cubic]({{L85}}), 3 lines | 1% | 5% | 7% | 10% |
| [Quarter Cubic]({{L86}}), 2 lines | 2% | 5% | 8% | 9% |
| [Grid]({{L87}}), 2 lines | 2% | 3% | 9% | 8% |
| [Triangles]({{L88}}), 2 lines | 0% | 1% | 2% | 5% |
| [Concentric]({{L89}}) | 1% | 2% | 3% | 4% |
| [Lightning]({{L90}}) | 1% | 2% | 2% | 3% |
| [Triangles]({{L91}}), 3 lines | -1% | 0% | 3% | 2% |

[Octagram Spiral]({{L92}}), [Hilbert Curve]({{L93}}) and [Honeycomb]({{L94}}) cut their corners deeply enough to print 29%, 15% and 7% less material at `100%`, which is part of their time saving. The other patterns keep their material within 4%, so their saving comes from speed.

> [!NOTE]
> A rounded corner takes several moves instead of one, so the G-code file gets larger as the smooth factor goes up. At `100%` the infill G-code is about 1.5 to 3 times that of the sharp path for most patterns, about 5 times for [Honeycomb]({{L95}}), 6 times for [Hilbert Curve]({{L96}}) and 8 times for [Octagram Spiral]({{L97}}), whose sharp path has very few vertices.

### Best smooth factor for speed

- **`100%` prints fastest** for almost every pattern and density in the analysis: the largest curves get the most vertices and the gentlest turns. The exceptions are close: [Grid]({{L98}}) with 2 lines and [Triangles]({{L99}}) with 3 lines print about one point faster at `75%`.
- **Lower factors save less.** On average `50%` saves about half of what `100%` saves, and [Triangles]({{L100}}) saves almost nothing below `75%`. Use them for the look of the infill, not for speed.
- **A finer [G-code resolution]({{L101}}) prints faster.** It splits every corner into more and gentler turns: on the 100 mm cube at `100%`, going from 0.012 to 0.006 mm raised the mean saving from 16% to 22%, for about 1.5 times the infill G-code. The resolution applies to the whole print, walls included.

### Supported patterns

The setting only affects **sparse infill**, and only the [patterns]({{L102}}) that implement it. It is hidden in the GUI when the selected pattern is not one of them.

- [Hilbert Curve]({{L103}})
- [Octagram Spiral]({{L104}})
- [Lightning]({{L105}})
- [Honeycomb]({{L106}})
- [3D Honeycomb]({{L107}})
- [Concentric]({{L108}})
- [Cross Hatch]({{L109}})
- With [Fill Multiline]({{L110}}) set to more than one line only:
    - [Grid]({{L111}})
    - [Triangles]({{L112}})
    - [Tri-hexagon]({{L113}})
    - [Cubic]({{L114}})
    - [Quarter Cubic]({{L115}})

> [!NOTE]
> [Grid]({{L116}}), [Triangles]({{L117}}), [Tri-hexagon]({{L118}}), [Cubic]({{L119}}) and [Quarter Cubic]({{L120}}) are only rounded in their trapezoidal, [Non-Crossing]({{L121}}) form, which needs more than one line per infill wall. With a single line they are plain crossing lines with no corner to round.

### Corners left sharp

Not every vertex of a supported pattern can be rounded, so some parts of the path stay as they are:

- **Hairpins.** A turn that doubles back on itself (a direction change sharper than about 154 degrees) would collapse into a degenerate loop instead of a curve, so it is left sharp. This is what keeps the tips of the [Lightning]({{L122}}) branches pointed.
- **Straight layers.** Layers where a pattern degenerates into straight lines have no corner to round — the flat layers of [3D Honeycomb]({{L123}}), the repeat layers of [Cross Hatch]({{L124}}) and the straight base lines of the [Triangles]({{L125}}) family.
- **[Concentric]({{L126}}) corners that would leave the fill region.** Its loops are offsets of the region rather than a path clipped to it, and rounding always cuts toward the inside of the turn. Around a hole, at a concave feature or across a thin region that cut falls outside the fill and would put the extrusion over a wall, so those corners keep their original shape. The reach is also capped at half the distance between two loops, since a loop is as long as the object rather than as long as one cell of a pattern.
- **[Lightning]({{L127}}) turns are capped as well.** Cutting a corner moves the whole branch, so the reach is limited to half the distance between two branches — or, with [Fill Multiline]({{L128}}), to half the printed branch width, which keeps the outlines drawn around merging branches from breaking up into separate loops.

## Top-Bottom Direction

{{M13}}

Fixed angle (in degrees) for the top and bottom surface lines.  
{{I16}}

The top angle also applies to ironing lines.  
Set to `-1` to follow the default solid infill [direction]({{L129}}).

## Separated Infills

{{M14}}

Centers the internal infill of each part on itself, as if it were sliced on its own, instead of on the whole assembly.  
By default the entire assembly is treated as a single whole, so a centered or rotated infill pattern is referenced to one common center and rotates around it. When enabled, each part is centered on its own full 3D bounding box — producing the same pattern you would get by slicing that part on its own.

{{I17}}

Parts are grouped by their real geometry when deciding what shares a center:

- **Touching or overlapping parts** are treated as one body and share a single center.
- **Separate parts** with disjoint projections — including distinct 3D objects — each get their own center.
- **Disconnected islands within a single mesh** are centered separately.
- **Interleaved parts that never touch** (chains) each get an independent center.

Useful when an assembly groups several objects that should each keep a consistent, self-centered infill.

> [!NOTE]
> The main disadvantage is that, for complex and large slices, centering each part independently can increase slicing time.

Applies to sparse infill, internal solid infill and bridges. Top and bottom surfaces are not affected; see [Center Surface Pattern On]({{L130}}) for those.  
The option is shown for the [sparse infill patterns]({{L131}}) it can center:

- **Line and grid patterns:** Rectilinear, Aligned Rectilinear, Zig Zag, Cross Zag, Locked Zag, Line, Grid, Triangles, Tri-hexagon, Cubic, Quarter Cubic, Lateral Lattice, Lateral Honeycomb, Hilbert Curve, Archimedean Chords and Octagram Spiral are phased through each part's bounding-box center, and [rotated]({{L132}}) infill turns around it.
- **Patterns laid out from the object origin:** [Honeycomb]({{L133}}), [3D Honeycomb]({{L134}}), [Cross Hatch]({{L135}}), [Gyroid]({{L136}}), [TPMS-D]({{L137}}) and [TPMS-FK]({{L138}}) are moved onto each part's bounding-box center.

[Adaptive Cubic]({{L139}}) and [Support Cubic]({{L140}}) always fill each part on its own, with cubes refined only near that part's surfaces, so the option is not shown for them.  
[Lightning]({{L141}}) is generated for the whole object and is unaffected, and [Concentric]({{L142}}) already follows the outline of each part.

- **Separated Infills Off:** the assembly is treated as a single whole, so the infill of every object is referenced to one common center.

{{I18}}

- **Separated Infills On:** each object in the assembly gets its own self-centered infill pattern.

{{I19}}

## Credits

- **[Fill Multiline]({{L143}}) implementation** - [@RF47]({{L144}})
- **Wiki page:** [IanAlexis]({{L145}}).
