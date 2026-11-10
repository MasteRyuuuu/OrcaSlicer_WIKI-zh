# Top and Bottom Shells

Controls how the top and bottom solid layers (shells) are generated.

{{I1}}

{{T1}}

## Shell Layers

{{M1}}
This is the number of solid shell layers, including the surface layer.  
When the thickness calculated from this value is less than [shell thickness]({{L1}}), the shell layers will be increased.

These layers are printed over the [sparse infill]({{L2}}), so increasing **shell layers** will increase overall part strength and top surface quality.
It's usually recommended to have at least 3 shell layers for most prints.

## Shell Thickness

{{M2}}
The number of solid layers is increased during slicing if the thickness calculated from shell layers is thinner than this value. This avoids having too thin a shell when layer height is small.  
0 means this setting is disabled and shell thickness is determined entirely by [shell layers]({{L3}}).

## Paint Penetration Layers

{{M3}}

When a top or bottom surface is painted with [Color Painting]({{L4}}), its color is also printed in the layers under a painted top surface and over a painted bottom surface, so the filament behind the paint doesn't show through. This is the number of layers that take the color, including the surface layer.  
Each layer further from the surface is colored about two line widths narrower than the one before, so the color tapers into the model instead of reaching its walls.

- **0:** uses the [Shell Layers]({{L5}}) count. This is the default, and how painted surfaces were always printed before this setting existed.
- **Lower values:** keep a thick shell for strength while printing fewer layers in the painted color, saving a filament change and its purge on each layer left out.
- **Higher values:** give a deeper, more saturated color, which helps with translucent or light filaments that let the layers behind them show through.

> [!WARNING]
> Keep the value within the shell, which is the larger of [Shell Layers]({{L6}}) and the layers needed to reach [Shell Thickness]({{L7}}). A larger value also colors the [sparse infill]({{L8}}) under or over the painted area, adding filament changes where they can't be seen.

## Surface Density

{{M4}}
This setting controls the density of the top and bottom surfaces. A value of 100% means a solid surface, while lower values create a sparse surface.  
This can be used for aesthetic purposes, improving grip or creating interfaces.

## Infill/Wall Overlap

{{M5}}
The top solid infill area is slightly enlarged to overlap with walls for better bonding and to minimize pinholes where the infill meets the walls.  
A value of 25-30% is a good starting point. The percentage value is approximately relative to the inner wall line width. More precisely, it is relative to half the inner wall line spacing plus half the internal solid infill line spacing with the [Classic]({{L9}}) wall generator, and to the inner wall line spacing with [Arachne]({{L10}}) (the outer wall line spacing in both cases where only one wall is printed).

> [!TIP]
> Check [Monotonic line]({{L11}}) to learn about its overlap differences with [Monotonic]({{L12}}) and [Rectilinear]({{L13}}).

## Surface Pattern

{{M6}}
This setting controls the pattern of the surfaces.  
If [Shell Layers]({{L14}}) is greater than 1, the surface pattern will be applied to the outermost shell layer only and the rest will use [Internal Solid Infill Pattern]({{L15}}).

> [!TIP]
> See [Infill Patterns Wiki List]({{L16}}) with **detailed specifications**, including their strengths and weaknesses.

The surface patterns are:

- **[Concentric]({{L17}})**
- **[Rectilinear]({{L18}})**
- **[Monotonic]({{L19}})**
- **[Monotonic line]({{L20}})**: usually recommended for top surfaces.
- **[Aligned Rectilinear]({{L21}})**
- **[Spiral Inset]({{L22}})**
- **[Hilbert Curve]({{L23}})**
- **[Archimedean Chords]({{L24}})**
- **[Octagram Spiral]({{L25}})**

> [!TIP]
> Enable [Align directions to model]({{L26}}) to make the top/bottom surface fill direction follow the model's orientation on the build plate.

## Surface Expansion

{{M7}}

Expands the top surfaces by this distance (in mm) to connect distinct top surfaces and fill the gaps left where a feature rises through them.  
This is useful when the top surface is interrupted by a raised feature, such as text or a boss on a plane, or when overlapping objects would otherwise split it: expanding the surface removes the holes beneath these features, keeps the top-surface pattern uninterrupted, and anchors the solid infill for a cleaner finish when printing on top. It also improves [concentric]({{L27}}) top surfaces, whose pattern would otherwise be broken up by those small holes.  
The expansion is applied to the original top surface, before any other processing such as bridging or overhang detection. Set to `0` to disable it.

- **Original**

{{I2}}

- **Expanded by 5 mm**

{{I3}}

- Improved [concentric]({{L28}}) top surface.
    - Before:{{I4}}
    - After:{{I5}}

> [!NOTE]
> Surface expansion needs a top solid surface to grow. It does nothing when [Shell Layers]({{L29}}) is `0` (the top surfaces are then treated as internal) or when [Surface Density]({{L30}}) is `0%` (the top surface is left unfilled).

### Surface Expansion Margin

{{M8}}
Using [Surface Expansion]({{L31}}) may cause a surface that did not previously touch the model's outer walls to now reach them, which can create contraction marks (such as a hull line) on the outer walls.  
Adding a margin (in mm) keeps the expansion away from the walls where possible, so no hull line is created. The example below uses a 5 mm expansion with a 2 mm margin — compare it with the 5 mm expansion above, which reaches the walls.

The margin is the real clearance left between the expanded top surface and the walls, so it is measured from the band the walls occupy. When [Only one wall]({{L32}}) on top surfaces is enabled, that band is a single wall, since that is all that remains over a top surface.

{{I6}}

### Surface Expansion Direction

{{M9}}
Direction in which the [Surface Expansion]({{L33}}) grows:

- **Inward:** grows into the holes and gaps left by features rising from the middle of a top surface.
  {{I7}}
- **Outward:** grows the outer edge of the surface, connecting surfaces separated by features that can divide a surface, such as a lattice pattern.
  {{I8}}
- **Inward and Outward:** does both. This is the default.
  {{I9}}

### Surface Expansion and Only One Wall

[Only one wall]({{L34}}) on top surfaces keeps a single wall where a top surface is detected. With more than one [wall loop]({{L35}}), the remaining inner walls are rerouted around the top surface, which can ring a feature with walls that are not needed, and cut up — or overlap with — an expanded top surface.

When **Surface Expansion** is in use, those inner walls are removed over the top surface instead, so the expanded surface stays continuous and the pattern is not interrupted:

- **[Classic]({{L36}})** wall generator: the inner walls running over the top are dropped whole. The space they leave is taken by the expanded top surface, and whatever it does not cover becomes [internal solid infill]({{L37}}) with [Ensure vertical shell thickness]({{L38}}) set to **All** (the default), or sparse infill with the other options.
- **[Arachne]({{L39}})** wall generator: the inner walls are cut instead of dropped, so only the part running over the top surface is removed and the rest is kept where the geometry continues upward.

> [!NOTE]
> This behavior needs a top fill that can actually take that space. With **Surface Expansion** at `0` or [Surface Density]({{L40}}) at `0%`, the inner walls are still rerouted around the top surface, preserving the internal support.

## Center Surface Pattern On

{{M10}}

Chooses where the centering point of centered top/bottom surface patterns ([Archimedean Chords]({{L41}}), [Octagram Spiral]({{L42}})) is placed.  
By default these patterns are centered individually on each surface, which does not keep the pattern continuous across a whole product — a drawback for some artistic prints where the surfaces should read as one piece. This setting widens the scope of the shared center:

- **Each Surface:** centers the pattern on every individual surface region, so each island is symmetric on its own. This is the default.

{{I10}}

- **Each Model:** combines all the surfaces of one model — or each shape in the assembly — under a single center. Parts that touch or overlap share one center; parts detached from the rest each get their own.

{{I11}}

- **Each Assembly:** all the surfaces of the assembly fall under a single shared center. Well suited for articulated models that should keep one continuous pattern across their parts.

{{I12}}

## Fill Order

{{M11}}

Direction in which the top and bottom surfaces are filled when using a center-based pattern ([Concentric]({{L43}}), [Spiral Inset]({{L44}}), [Archimedean Chords]({{L45}}), [Octagram Spiral]({{L46}})). The spirals/rings are then deposited consistently inward or outward instead of following the default shortest path.

{{I13}}

- **Default:** uses shortest-path ordering, which may run in either direction.
- **Outward:** starts at the center of the surface, so any excess material is pushed towards the edge where it is least visible. Preferred for **top** surfaces, as it hides small imperfections better.
- **Inward:** starts at the edge and ends with the tight curves at the center. Preferred for **bottom** surfaces, as starting each surface with the wider outer curves improves first layer adhesion on build plates where the tight curves at the center may not stick.
