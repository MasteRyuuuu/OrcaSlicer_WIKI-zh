# V2.5.0 Beta

This is the OrcaSlicer V2.5.0 Beta. It builds on the alpha with new features, faster prints and slicing, and fixes for many of the problems reported since the alpha. **Toolhead collision volumes** let a printer profile mark bed clips, tool docks and other obstacles above the bed, so Arrange, brims, most supports and travel moves keep clear of them. Travel moves are **shorter** on every print, usually saving print time with nothing to turn on, **evenly rounded infill corners** make smoothed sparse infill print faster, and **slicing runs up to twice as fast** on detailed models and many times faster on objects with thousands of parts. **Translucent filaments** now look see-through in Preview, and the beta fixes Mesh Boolean on Windows, random crashes on Apple silicon Macs and hangs on exit.

**Note:** This is a beta build for testing. Back up projects and profiles you care about, and please report any problems on GitHub.

# 🌊 New Features & Improvements

## Slicing & Print Quality

* **Toolhead collision volumes** by @Harry-Loud in [13777]({{L1}})
    Printers can now describe obstacles above the bed, such as low bed clips, raised tool docks or camera arms, as 3D volumes. The new **Toolhead collision volumes** setting sits below **Excluded bed area** in Printer settings > Basic information > Printable space (Advanced mode) and takes one or more polygonal prisms, either full height or limited to a Z range.

    Objects that touch a volume are flagged, with the overlap shown in red. Arrange and Fill Bed keep objects clear of the volumes, taking their height into account, so an object can still sit under a raised one. Brims and normal supports are clipped around the volumes, **Organic** tree supports steer their branches around them, and travel moves are rerouted where a safe path exists; **Tree Slim**, **Tree Strong** and **Tree Hybrid** supports don't avoid them yet. As a final check, OrcaSlicer scans the G-code and warns about any move that still crosses a volume, though it can't see moves hidden inside firmware macros.

    On multi-extruder printers, **Collision volume behavior** chooses whether the volumes are shared, follow each nozzle's offset or are set per extruder, and **View > Show all collision volumes** shows them at full height. **Excluded bed area** works as before, and printers without collision volumes slice exactly as before. Fixes #5922 and #10579.

    {{I1}}

    | Shared | Toolhead-relative (nozzle offsets) | Individual per extruder |
    |--------|------------------------------------|-------------------------|
    | {{I2}} | {{I3}} | {{I4}} |

* **Shorter travel moves on every print** by @ianalexis and @gloth-3ds in [16492]({{L2}}) and [16743]({{L3}})
    OrcaSlicer now plans a shorter route through each layer, with nothing to turn on. On a benchmark plate, travel dropped by 6–26% and estimated print time by 1–6.5%, or 6 to 45 minutes on 10- to 13-hour prints, while slicing took at most 2.1% longer. Infill, ironing and support paths print in a shorter order, objects and islands are visited along a shorter tour when **Intra-layer order** is Default, and infill lines are joined into longer continuous paths.

    Gap fill on Monotonic and other fixed-order surfaces prints as the nozzle passes it instead of at the end; with **Apply gap fill** set to Everywhere or Top and bottom surfaces, this saved 538 retractions on a 15-hour print. Less travel usually means a faster print, but not always: on one dense plate of Benchy copies with a 0.2 mm nozzle, more short hops crossed the retraction threshold, and the estimate rose by 3.6% despite 6.5% less travel. Expect every print's G-code to change.

    | Before | After |
    |--------|-------|
    | {{I5}} | {{I6}} |

* **Faster sparse infill from evenly rounded corners** by @ianalexis and @RF47 in [16694]({{L4}}) and [16707]({{L5}})
    Sparse infill with rounded corners prints faster. With **Sparse infill smooth factor** at 100%, it prints up to 29% faster than with smoothing off (Octagram Spiral), and a Hilbert Curve print on a Snapmaker U1 took 16% less time than with the previous rounding. Each rounded corner is now split into segments that all turn by the same angle, with as few segments as the G-code resolution allows. Klipper and Marlin 2 slow down at each junction by how sharply it turns, so the toolhead keeps more of its speed through the curves.

    The extra lines of multiline infill (**Fill Multiline** above 1) have sharp corners, which need fewer G-code points, and the smooth factor alone controls their rounding. With the smooth factor at 0, single-line infill is unchanged.

    | Multiline before | Sharp corners | With 5% smooth factor |
    |------------------|---------------|-----------------------|
    | {{I7}} | {{I8}} | {{I9}} |

* **Arc fitting for sparse infill only** by @ianalexis in [16747]({{L6}})
    **Arc fitting** (Quality > Precision, Advanced mode) is now a dropdown with **Disabled**, **Enabled** and **Sparse infill only**. The new mode turns only the sparse infill into G2/G3 arcs, shrinking the G-code of curved infill such as Gyroid, TPMS or smoothed infill, while walls, surfaces, supports and the wipe tower stay as straight moves. Existing profiles and projects keep their setting, and the tooltip still recommends Disabled for Klipper printers, where arcs can print more slowly.

    {{I10}}

* **Top and bottom paint penetration layers** by @ianalexis in [16818]({{L7}})
    Two new settings, **Top paint penetration layers** and **Bottom paint penetration layers** (Strength > Top/bottom shells, Advanced mode, also per object), set how many layers below a painted top surface, or above a painted bottom surface, take the painted color. Previously, that was always the number of shell layers. A thick shell can color fewer of its layers, saving a filament change and purge on every layer it no longer colors, or color deeper for translucent filaments; values above the shell count also color the sparse infill. At the default of 0, the shell layer count is used as before.

    Bambu Lab, Qidi and OpenEYE presets and Bambu Studio projects already set these values and now use them, so painted prints with those presets may color a different number of layers than in the alpha.

    {{I11}}

* **High precision G-code (experimental)** by @valerii-bokhan in [16568]({{L8}})
    A new process option, **High precision G-code (experimental)**, can steady extrusion with small nozzles and very thin layers, where each move extrudes very little: on the author's test cylinder, flow variation on the outer wall fell from 1.2% to 0.09%. It writes positions with 4 decimals instead of 3 and extrusion with 6 instead of 5, and with relative extrusion it carries each move's rounding error into the next. Find it in Others > G-code output (Expert mode, off by default). The G-code grows by about 10%, which may slow printers that parse G-code slowly; with the option off, output is unchanged.

    | Standard precision | High precision |
    |--------------------|----------------|
    | {{I12}} | {{I13}} |

## G-code & Placeholders

* **Print time estimates that follow Klipper's motion planner** by @Gabriel-Hiss in [15545]({{L9}})
    On Klipper printers, print time estimates now plan moves the way Klipper does, including its minimum cruise ratio, square corner velocity and handling of `SET_VELOCITY_LIMIT` and `M204`. Replayed against Klipper, estimates matched within about 0.1 s per file. A QIDI print that took 9h08m was estimated at 7h44m before; the new estimate is 8h34m with the profile's square corner velocity of 9, and 9h02m once that is set to 5 to match its printer.cfg.

    For accurate estimates, set the printer's jerk limits to match `square_corner_velocity` in your printer.cfg; on Klipper, OrcaSlicer reads the square corner velocity from them. With **Enable accel_to_decel** on (the default), OrcaSlicer also writes `MINIMUM_CRUISE_RATIO` along with `ACCEL_TO_DECEL`, which overrides `minimum_cruise_ratio` in printer.cfg on current Klipper; turn the option off to keep your printer.cfg value.

* **Print statistics placeholders work in custom G-code** by @PanJany, @raistlin7447 and @downtime0 in [16348]({{L10}}), [16597]({{L11}}), [16680]({{L12}}) and [16272]({{L13}})
    The print statistics placeholders `total_weight`, `used_filament`, `total_cost`, `print_time`, `normal_print_time`, `silent_print_time`, `total_wipe_tower_cost` and `total_wipe_tower_filament` now work in any custom G-code, including the file header, with the same values as the slicing statistics. They were offered in every custom G-code field but only worked in the output filename; anywhere else, slicing stopped with "Not a variable name".

    Like the `print_time_*` parts, these values are filled in after the G-code is generated, so they can be printed but not used in calculations or comparisons. Trying to do so stops slicing with a clear error instead of silently giving a wrong result. Placeholders that failed in some places, such as `{max_layer_z}` in Layer change G-code, work too, and the Edit Custom G-code dialog lists about 40 placeholders that the slicer already provided but the editor didn't offer. Fixes #7870 and #15320.

* **Outline tolerance for exclude-object outlines** by @ghzserg in [16503]({{L14}})
    A new process setting, **Outline tolerance** (Others > G-code output, Expert mode, Klipper only), sets how much the object outlines written for `EXCLUDE_OBJECT_DEFINE` may be simplified. Larger values write fewer points, which helps slower Klipper controllers, such as the Flashforge AD5X, that hit `Timer too close` on crowded plates: at 0.2 mm, the AD5X handled 9 objects instead of 6. The default of 0.1 mm keeps output unchanged.

## Performance

* **Faster slicing of detailed, painted and many-part models** by @SoftFever and @ExPikaPaka in [16741]({{L15}}), [16733]({{L16}}) and [15985]({{L17}})
    The models that took longest to slice now slice much faster, with identical G-code on every project tested. On finely detailed models such as HueForge reliefs, two single-core steps dominated the slice: G-code export spent most of its time working out which object each extrusion belongs to, and internal bridge detection could stall for tens of seconds on layers printed over fully dense infill. That lookup is much quicker, and bridge detection settles most layers with a cheaper check before falling back to the full one, so these models slice up to twice as fast.

    On objects made of thousands of parts, nearly all the slicing time went into working out which parts touch each other for the brim. That step was far slower on macOS, where a Mac took 2.5 times as long as a Windows desktop on the same model, and with the fix the whole slice takes about 20 s on both. Layers cut into tens of thousands of pieces, as with fine relief, dense color painting or heavily fragmented models, slice faster too: infill, vertical shells and bridging over infill look only at the nearby part of the layer instead of the whole layer, more of the work runs in parallel, and polygons are no longer copied needlessly. In every comparison, including 179 outputs across 11 models and 17 configurations, the G-code was byte-identical to before.

    | Model | Before | After |
    |-------|-------:|------:|
    | HueForge relief "Mensch oder Gott 2", Mac | 108 s | 54 s |
    | The same relief, Windows | 116 s | 65 s |
    | City map, one object with 6,948 parts, Mac | 265 s | 18 s |
    | The same city map, Windows | 102 s | 20 s |
    | Painted plate at 0.1 mm layers | 24 min | under 10 min |

    The Mac is an Apple M5 Max and the Windows desktop an Intel Core Ultra 7 270K Plus.

* **Faster startup** by @yw4z and @raistlin7447 in [16642]({{L18}}), [16645]({{L19}}) and [16670]({{L20}})
    The main window opens sooner when you're signed in to Orca Cloud: in tests on Windows, it appeared in 1.6 s instead of 3.6–4.2 s. OrcaSlicer no longer waits for your cloud plugins' status before showing it, and the check runs in the background in about half the time. On Windows, checking for a 3D mouse at startup also takes under a millisecond instead of up to 0.2 s.

## Interface & Usability

* **Reorganized right-click menus** by @yw4z and @colintrachte in [14787]({{L21}}) and [16589]({{L22}})
    The right-click menus for objects, parts, text and SVG parts, cut objects, plates and multiple selections are reorganized so related items sit together, in the same order on every menu. Less-used commands move into submenus: **Transform** (mirror, **Scale to build volume** and unit conversion), **Modify** (split, Mesh boolean, simplify, smooth, Fix model, and **Fix All** on the plate menu) and **More** (Reload from disk, Replace with STL and Export as STL/DRC), and the instance commands go into an **Instances** submenu.

    **Change Filament** moves up the object menu, with **Flush Options** right after it, so a long filament list no longer pushes it off the screen. **Reload from disk** is also available when several objects or parts are selected (Fixes #10349), and **Delete Plate** is greyed out when there is only one plate.

    | Before | After |
    |--------|-------|
    | {{I14}} | {{I15}} |

    | Transform | Modify | More |
    |-----------|--------|------|
    | {{I16}} | {{I17}} | {{I18}} |

* **Order By for plates** by @ianalexis in [16850]({{L23}})
    Right-click a plate, in the object list or the 3D view, for a new **Order By** submenu that sorts its objects by **Name**, **Filament**, **Height** or **Size**. Choosing the same entry again reverses the order, and **All Plates** sorts every plate. Names sort naturally ("Part 2" before "Part 10"), and each sort is a single undo step. Because printing **By object** follows the order of the object list, **Order By > Height** prints the tallest object last, and **Order By > Filament** groups objects that share a filament to save filament changes. Closes #12386.

    {{I19}}

* **Choose a primitive's size when adding it** by @ianalexis in [16848]({{L24}})
    Adding a cube, cylinder, sphere, cone, disc or torus opens a dialog that asks for its dimensions, and the shape is built at that size, so round shapes get a resolution to match: a 200 mm cylinder now has 497 segments, where scaling up the old default kept the 180 of a 25 mm one. **Uniform scale** keeps the ratios between the values as you edit one, **Save these settings as default** remembers the size for that shape, and **Don't show again** adds shapes at their default size without asking. To bring the dialog back, turn on **Show options when adding a primitive** in Preferences > Control > Behavior. The dialog also appears when you add a primitive as a part, negative part or modifier.

    {{I20}}

* **Settings explain why they are hidden or disabled** by @Noisyfox in [16657]({{L25}})
    When another setting greys out or hides a setting, its tooltip now opens with the reason, marked "Disabled: …" or "Hidden: …". A disabled **Support type**, for example, tells you to enable support or add raft layers. The settings search lists hidden settings with the reason on a second line, and the Speed Dial shows it in its details. This covers the process, printer and filament settings and the per-object settings table. Fixes #2170.

    {{I21}}

    {{I22}}

* **Translucent filaments look translucent** by @ianalexis in [16776]({{L26}})
    A filament color with opacity is now drawn the way the print would look. In Preview, toolpaths of a translucent filament are see-through in the Filament, Summary and Tool views, and thin layers stack up like one thick wall. Travel moves and markers stay opaque, and legend swatches show the opacity over a checkerboard. In Prepare, a translucent part looks denser at its edges than face-on. Two new preferences, both on by default, control this: **Translucent filaments** (Preferences > Graphics > G-code Preview) and **Glossy toolpaths** (Preferences > Graphics > Realistic View), which adds a plastic highlight to toolpaths in the realistic view. Fixes #9723.

    {{I23}}

* **Opacity and gradients for custom AMS colors** by @Noisyfox in [16538]({{L27}})
    When you set a custom color for an AMS slot in the Device tab, the color picker now takes an opacity. On printers whose firmware supports multicolor filaments, it also takes a gradient of up to four colors, which is sent to the printer. Translucent colors are drawn over a checkerboard wherever filaments are shown, including the AMS slots, the filament rack, the Change Filament menus and the object list.

    | Gradient with opacity | Translucent colors |
    |-----------------------|--------------------|
    | {{I24}} | {{I25}} |

* **Pick a color from the screen** by @yw4z in [16587]({{L28}})
    The color picker has an eyedropper button, **Pick color from screen**, for taking a color from anywhere on the screen. On Windows it shows a magnifier: hold Shift to slow the cursor for precise picking, and press Esc or right-click to cancel. macOS uses the system color sampler and Linux uses the desktop's color picker (GNOME and KDE, on X11 and Wayland). The button is hidden where no sampler is available.

    {{I26}}

* **Home tab polish** by @yw4z in [15785]({{L29}})
    Recent projects on the Home tab show **Show in folder** and remove buttons when you hover over them, in place of the right-click menu, and **Show in folder** is greyed out for files that no longer exist. The sidebar matches the other tabs and gains a **Wiki** link, model cards highlight on hover, text and icons line up, and the scrollbar is dark in dark mode.

    | Before | After |
    |--------|-------|
    | {{I27}} | {{I28}} |

* **See below the plate in the painting tools** by @lamweilun in [16681]({{L30}})
    In the Support, Seam, Color, Fuzzy skin and Texture displacement painting tools, the part of an object sunk below the plate is drawn as a see-through ghost instead of being cut off. The plate and its grid stay visible, and where the object crosses the plate there is a thin outline instead of an opaque orange cap that hid the model.

    <video controls width="800" src="{{L176}}"></video>

* **Compact Texture Displacement panel** by @yw4z in [16524]({{L31}}) — **Budget**, **Resolution** and **Triangles** move into a collapsible **Quality** section, and **+ Add layer** sits in the layers header, so it stays in place while you add layers.

* **Restyled Import Model dialog** by @yw4z in [16768]({{L32}}) — the dialog for textured and colored models matches the rest of the app, and its dropdowns open on click instead of on hover.

* **3Dconnexion settings in the View menu** by @eoyilmaz in [16345]({{L33}}) — **View > Show 3Dconnexion Settings** opens the 3D mouse settings, which were only reachable by a keyboard shortcut that many macOS users couldn't use. Fixes #5484.

* **Ctrl+Q quits on Linux and Windows** by @lamweilun in [16722]({{L34}}) — just like Cmd+Q on macOS. It is listed in the Keyboard Shortcuts dialog and can be rebound.

* **Display backend in the Troubleshoot dialog** by @yw4z in [16615]({{L35}}) — on Linux, the Package line shows whether OrcaSlicer is drawing through Wayland or X11.

## Plugins

* **Plugins can edit the active presets, and Scripts run in the background** by @peachismomo in [16518]({{L36}})
    Plugins can now change settings in the active process, printer and filament presets, one at a time or as a batch that applies together or not at all (`orca.host.preset`, with `begin_update()` and `commit()` for a batch). Changes go through the same checks as editing in the GUI and stay unsaved until you save the preset, and a plugin that asks for another preset switches to it with the usual unsaved-changes prompt. Script plugins move to the background, so the interface stays responsive while a script works, and a Script's `execute` can be `async`. Started from the Speed Dial, a script says that it started and shows its result as a notification when it finishes.

* **Plugin permissions declared up front and remembered** by @peachismomo and @SoftFever in [16688]({{L37}}), [16690]({{L38}}), [16793]({{L39}}) and [16658]({{L40}})
    Plugins can declare everything they need when they load, with `orca.request_permissions()`: files and folders to read or write, sites to reach, sockets, programs to run and threads. You answer one combined prompt before any of the plugin runs, instead of being interrupted in the middle of a script or a slice. A declared site covers every path and port on that host, and a folder ending in `/*` covers everything inside it.

    Approvals now hold across restarts, where before a URL you had approved asked again in each new session, and an approval no longer carries over to unrelated requests such as a redirect or a second URL. Because Scripts run in the background, a permission a plugin didn't declare is refused the first time it's used while the prompt is still open, and only a later attempt succeeds, so plugin authors should declare permissions up front. Fixes #15724.

## Printer Connectivity

* **Klipper filament sync by filament ID** by @broncosis in [14423]({{L41}}) — when the tool managing your lanes (for example spoolman-lane-sync) writes an OrcaSlicer filament ID into Moonraker's `lane_data`, filament sync picks that exact filament preset instead of guessing from the material type.

* **Select All in the printer's storage** by @Eldenroot in [16716]({{L42}}) — when picking files in the Device tab's timelapse or model list for batch download or deletion, **Select All** selects every file in the list.

# 🛠️ Bug Fixes

## Walls, Seams & Supports

* **Seams stay aligned and inside painted areas** by @DImagine in [16447]({{L43}}) and [16334]({{L44}})
    Aligned seams could skip a layer, jump between neighboring walls such as the inside and outside of a tube, or step sideways on painted surfaces, as on a painted sphere or Benchy's chimney. Seams now follow their own contour from layer to layer and stay inside the painted range, and random seams stay inside the enforced paint, including with a partial **Seam Blocked** modifier.

    On walls that overhang all the way around, such as the underside of a sphere, the seam setting and seam painting are no longer ignored. A seam stops at the paint edge instead of about a line width past it, so extend the blocked paint if you want more margin. Fixes #11248, #16333, #16443 and #16445.

    | Painted seam | Result |
    |--------------|--------|
    | {{I29}} | {{I30}} |

* **Correct wall order for narrow tube walls and outer brims** by @ianalexis in [16421]({{L45}})
    On walls just wide enough for three lines, such as a tube wall 1.5 mm thick printed with 0.5 mm lines, Arachne printed the shared center line last with the default **Inner/Outer** wall order, which left the outer walls nothing to lean on. It now prints first. With **Inner/Outer/Inner**, narrow tube walls print the hole's outer wall, then the contour's, then the middle on every layer after the first, with both wall generators. Classic also prints thin-walled holes before the contour on every layer unless the outer walls go first, as Arachne already did.

    Under an **Outer brim only**, **Outer and inner brim** or **Leading edge only** brim, the first layer prints the outer walls first with both wall generators, so the brim runs straight into the wall. Prints with narrow sections or these brims will slice differently, most of all with Arachne.

* **Arachne wall order at pinched holes and with one wall on top** by @igiannakas in [16894]({{L46}})
    Where a hole comes so close to the outside that the two outer walls touch, Arachne with **Inner/Outer/Inner** printed the hole's outer wall last, after its inner walls. On layers using **Only one wall on top surfaces**, an inner wall along the top surface was ordered as if it touched the outer wall, so every wall order could print it out of sequence, as at the opening of Benchy's cargo hold. Both now follow the chosen wall order. Classic walls are unchanged, and so are Arachne prints without pinched holes or one wall on top.

    | Before | After |
    |--------|-------|
    | {{I31}} | {{I32}} |

* **Tree supports print completely, with extra walls only where needed** by @kisslorand in [16549]({{L47}})
    Parts of tree supports could be missing from the G-code on some layers. With **Support wall loops** at 0 (auto), a branch that needed an extra wall also gave extra walls to unrelated support areas on the same layer, and random double walls appeared inside supports. Extra walls now go only to the branches that need them.

* **Features print with their assigned filament** by @ianalexis in [16805]({{L48}})
    With per-feature filaments (Process > Multimaterial > **Filament for Features**), inner walls that started on an overhang printed with the outer wall filament, and gap fill on top and bottom surfaces printed with the wrong filament. Layers also switched to filaments they printed nothing with, adding 61 idle tool changes on a Benchy. Each feature now prints with its own filament, gap fill follows its surface, and a layer only switches to filaments it uses.

* **Adaptive pressure advance on every layer** by @HanifKoh in [16857]({{L49}}) — a print whose travel speed matched its wall speed kept the first layer's pressure advance for the whole print. Adaptive PA now uses the real extrusion speed on every layer. Fixes #16737.

* **Bed temperature with By Highest Temp** by @SoftFever in [16770]({{L50}}) — a filament that only starts above the first layer, such as a PETG support interface on a PLA part, raised the bed from layer 2 on and softened the part. The bed now follows only the first-layer filaments for the whole print, as in Bambu Studio. Fixes #16644.

## Prime Tower & Multi-Material

* **Improved prime tower placement and sizing** by @HanifKoh in [16728]({{L51}}) and [16726]({{L52}})
    When a project's saved prime tower position fell outside the valid range, loading it moved the tower to the plate edge without checking for objects, so it could land on the model. It now moves to the nearest free spot and tells you so. If no spot on the plate is free, it stays at its usual fallback spot near the plate edge, and you're told that it sits on an object.

    A Type 2 tower with a **Rectangle** or **Rib** wall was sized as if it had the stabilization cone that only a **Cone** wall prints. That caused false path-conflict warnings at Z 0, a skirt around a phantom cone that could fail with "G-code in unprintable area", and a too-large first-layer area for bed mesh and purge placement.

* **Prime tower right on the first slice** by @thelegendtubaguy in [16326]({{L53}}) — after a plate went from one filament to two, for example by adding a filament change at a layer or moving an object to another filament, the first slice could come out without a prime tower, and exporting then quietly re-sliced with one. Removing the change could do the reverse. The tower is now decided from the current model on every slice. Fixes #15991.

* **Valid wipe tower G-code in decimal-comma languages** by @HanifKoh and @lamweilun in [16717]({{L54}}) and [16789]({{L55}})
    With a UI language or system locale that uses a decimal comma, such as Russian, German or French, the Type 1 wipe tower wrote feedrates like `F5400,000000`, which stopped Klipper with "Unable to parse move". Its layer height and line width tags also used commas, so the Preview misread the tower. Both now always use a decimal point. Fixes #16696.

* **Delete filaments down to one on dual-nozzle printers** by @SoftFever in [16856]({{L56}}) — on the Bambu Lab H2D, X2D and other printers whose nozzles share filaments, deleting filaments down to one left an empty second filament that came back after reopening or restarting. You can now go down to one, and projects saved with the empty slot open with one filament again. Fixes #16833.

* **Flow ratio of 0 is refused** by @HanifKoh in [16719]({{L57}}) — a filament with **Flow ratio** 0 sliced without complaint and wrote huge negative extrusion on every move. Slicing now stops with a message naming the filament. Fixes #16712.

* **Repeatable Type 1 prime tower slices** by @anselor in [15183]({{L58}}) — when a config didn't list a value for every filament, slicing the same plate again could give a different tower size and number of tool changes. Missing values now fall back like other settings.

## G-code & Export

* **Post-processing scripts run on G-code inside .gcode.3mf** by @ghzserg in [16464]({{L59}}) — on non-Bambu printers, post-processing scripts and slicing-pipeline plugins didn't run on the G-code packed into a `.gcode.3mf`, whether exported or sent to a print host. They now run on each plate's G-code before it is packed, and a failing script stops the export with its error. Fixes #1248 and #3974.

* **Correct first-layer bounding boxes for every plate in 3MF** by @ghzserg in [16860]({{L60}}) — for every plate except the first, the first-layer bounding boxes saved in a 3MF were offset outside the bed, so tools that read them for an adaptive bed mesh or purge placement got wrong values.

* **`{plate_name}` follows the plate's name** by @vertigo235, @yw4z and @cook0001 in [16715]({{L61}}) and [16900]({{L62}}) — the placeholder could come out empty in the output filename even when the plate had a name. After you rename a sliced plate, G-code that uses `{plate_name}` is marked out of date, and slicing again re-exports it with the new name without re-slicing. Each rename is also its own undo step. Fixes #16126 and #11570.

* **Unindexed placeholders use the current filament** by @tejas-devkar in [16211]({{L63}}) — in custom G-code, a placeholder written without an index, such as `{z_hop}`, could take another filament's or extruder's value, for example filament 2's Z-hop override while printing filament 1. Fixes #12804.

* **Layer pauses on the right layer in Preview** by @HanifKoh in [16718]({{L64}}) — the Preview showed pauses and color changes one or more layers too high, and the layer slider could show extra layers. The G-code was always right. Fixes #16693.

* **Correct layer number in the G-code conflict warning** by @kisslorand in [16588]({{L65}}) — the warning could name a layer that didn't match the height it reported.

## Models, Plates & Tools

* **More dependable Arrange, Scale to build volume and Lay on Face** by @lamweilun and @peachismomo in [16691]({{L66}}) and [16796]({{L67}})
    **Arrange** couldn't place an object that only just fits, such as one scaled to fit, so nothing seemed to happen. It now places it, leaves objects that can't be placed where they were instead of throwing them a plate's width away, and no longer deletes plates you created. Adding a multi-material handy model arranges like the Arrange button, so objects that don't fit go onto new plates instead of outside the plate.

    **Scale to build volume** no longer moves a model from plate 2 back to plate 1. It fits the area every nozzle can reach, so the H2D no longer shows a nozzle-range warning right after fitting, and it keeps clear of bed exclusion areas. **Lay on Face** on a face that already points up flips the part over instead of landing it at a random angle.

    {{I33}}

    Lay on Face on a face that points up:

    <video controls width="800" src="{{L177}}"></video>

    Arrange keeps empty plates:

    <video controls width="800" src="{{L178}}"></video>

* **Select All and Delete All on the current plate** by @fer-marino and @thelegendtubaguy in [15895]({{L68}}) and [16881]({{L69}})
    **Ctrl+A** skipped objects too big for the bed or partly off it, so with one oversized model it seemed to do nothing. It now selects every object copy on or overlapping the current plate, and Select All and **Delete All** work per copy, leaving copies on other plates alone. After a cut or **Delete all connectors**, plates could also count objects from other plates, which gave single-filament plates two-color prime tower previews and made Select All pick up those objects. Removing an object with several copies could also move its other copies onto another object. Fixes #15888 and #16859.

* **Objects with a part off the plate can't be sliced** by @kisslorand in [16564]({{L70}}) — a multipart object still sliced when one of its parts sat entirely outside the plate. It now counts as partly outside, which blocks slicing and highlights the parts. Parts sunk entirely below the bed are still ignored, so you can slice the rest after a failed print.

* **Per-extruder print areas checked before slicing on non-Bambu printers** by @cgarwood82 in [14140]({{L71}}) — on multi-nozzle printers whose extruders have different printable areas, an object placed where its extruder can't reach wasn't flagged in the 3D view and only failed after slicing, with a misleading message. It's now flagged before slicing, as on Bambu Lab printers. A conflict on extruder 3 or higher, which blocked slicing without any message, now explains itself, and these errors no longer offer a "regroup" link that doesn't apply to such printers. Fixes #14070.

* **Cut connector holes at the right depth** by @tejas-devkar and @HanifKoh in [16020]({{L72}}) and [16893]({{L73}})
    A **Dowel** connector's tolerance went entirely to one half of the cut, so with 3 mm depth and 1 mm tolerance one hole was 3 mm deep and the other 4 mm. The tolerance is shared evenly between the two halves instead. Every connector hole also ended 0.05 mm short: Plug and Snap holes now reach the depth plus tolerance, and each Dowel hole the depth plus half the tolerance. Fixes #14299 and #16883.

* **Drop clears sinking, and Auto Drop stays off in 2.4 projects** by @yw4z and @lamweilun in [16501]({{L74}}) and [16633]({{L75}})
    **Drop** on an object pushed below the bed now clears its sinking state, and the object list's sinking icon appears and works even with Auto Drop off. Projects saved by 2.4.x with **Auto Drop** turned off had it turned back on in the alpha, which dropped floating objects onto the bed; in the beta they keep it off. Projects already re-saved by the alpha or a nightly can't be recovered this way. Fixes #16677 and #16624.

* **Move tool alignment follows the selection** by @lamweilun in [16730]({{L76}}) — align and distribute no longer get stuck in Plate mode, and with the **Object** coordinate system they work along the object's own rotated axes. The Move and Scale tools also no longer switch from Object back to World on their own.

* **Texture displacement bakes every painted part** by @ExPikaPaka in [16721]({{L77}}) — only the first part of an object was baked, and paint on the other parts was ignored. All painted parts are now baked together, in one job and one undo step. Fixes #16559.

* **Models with JPEG textures keep them on import** by @RJAudas in [16607]({{L78}}) — GLB and OBJ models textured with JPEG images lost their textures, and matching texture colors to filaments could crash. GLB, glTF and FBX files can now also be dropped onto the window or opened from the OS. Fixes #16606.

* **Chinese, Japanese and Korean input in the Text tool** by @SoftFever in [16824]({{L79}}) — on macOS, input methods didn't work in the Text tool and other text fields in the 3D view. With the interface in Chinese, Japanese or Korean, the Text tool's default text could also show as "????" when the system font lacked those characters; new text now starts in a bundled font that can show it.

* **Hold +/− to keep changing a value** by @yw4z in [16525]({{L80}}) — in the 3D-view tools, such as the Text tool's height and depth, holding the buttons next to a number field changed the value only once.

* **Lay on Face opens without a delay** by @raistlin7447 in [16846]({{L81}}) — with **Smooth normals** on, opening Lay on Face on a newly selected object froze the interface for about half a second.

## Presets, Projects & Command Line

* **Open 2.4 projects with custom filaments** by @raistlin7447 in [16569]({{L82}}) — a project saved by 2.4 with a custom filament based on a system filament could fail with "bad allocation" and load with no geometry. Fixes #16562.

* **Deleting a custom printer keeps presets other printers use** by @SoftFever in [16928]({{L83}})
    Deleting a custom printer also deleted every user filament and process preset that worked with it, including presets with no printer restriction that other printers use. It now deletes only the presets made for that printer alone, keeps any that a kept preset inherits from, and the confirmation dialog counts exactly those. Saving another preset's settings over a synced preset no longer deletes its Orca Cloud profile, which made other devices drop the preset until the saving device restarted.

    Deleting a custom printer also made OrcaSlicer resend cloud deletes for system filaments about once a minute for as long as it ran. A delete now stops once Orca Cloud confirms the profile is gone, failures are retried less often, a delete is only sent with the account that made it, and one still pending at exit goes out at the next start. Checking for subscription changes also no longer downloads the whole list every minute.

* **Disabled filament overrides stay off** by @HanifKoh in [16650]({{L84}}) — an override switched off on the filament's **Setting Overrides** page, such as **Retract amount before wipe**, came back on after a restart whenever the parent preset set it. Fixes #13943.

* **No crash selecting a printer from a vendor that isn't installed** by @HanifKoh in [16579]({{L85}}) — selecting a user printer preset based on such a printer, which you get by saving the printer of another vendor's project, crashed OrcaSlicer, and so did the Create Printer and Create Filament dialogs. Fixes #16554.

* **Invalid preset names are refused** by @yw4z in [15579]({{L86}}) — the Save preset dialog accepted invalid names, including an empty one. **OK** stays greyed out until the name is valid, and preset and physical printer names can no longer contain control characters, use a Windows reserved name such as CON or COM1, or run too long to be saved as a file on every system.

* **No empty "newer 3MF" warning in nightlies** by @HanifKoh in [16791]({{L87}}) — opening a project saved by 2.5.0-alpha in a nightly build warned that the file was from a newer version and listed nothing. When the warning does appear, it now lists the unrecognized settings. Fixes #16771.

* **Command-line fixes** by @thelegendtubaguy, @thereprocase and @andrewgribben in [16703]({{L88}}), [16867]({{L89}}) and [15998]({{L90}}) — projects that don't record which settings differ from the system presets were sliced with the system values instead of their own, for example with supports turned off. Loading two or more filaments with `--load-filaments` and no `--filament-colour` could crash or silently drop layers printed with filament 2 or later. Fixes #16698, #15632, #14181 and #12426.

* **Command line reports values it replaced** by @packerlschupfer in [16305]({{L91}}) and [16303]({{L92}}) — when a preset or 3MF held a value OrcaSlicer can't read, such as an invalid **Ironing type**, the CLI quietly used the default instead, slicing with ironing off in that example. Each replacement is now printed to stderr and listed in `result.json` under `warnings` with the class `config_value_substituted`. Exit codes are unchanged, and `--strict` doesn't fail on these. `result.json` and `--pipe` progress are also written when an object or file name isn't valid UTF-8, where `result.json` used to be missing and a `--pipe` run aborted.

## Calibration

* **Flow ratio calibration works with an automatic default line width** by @HanifKoh in [16725]({{L93}}) — with the process preset's **Default line width** at 0 (auto), the test crashed for every test type. It now works with any line width, and its speed cap uses the line width the test actually prints, so it stays within the filament's max volumetric speed. Fixes #16560 and #15193.

* **Calibrate AMS filaments on either nozzle with a Filament Track Switch** by @HanifKoh in [16632]({{L94}}) — on an H2C, H2D or X2D with a Filament Track Switch, the calibration wizard's Flow Dynamics page listed every AMS under the right nozzle only. Each AMS now appears under both nozzles, as in Bambu Studio, and a filament is calibrated on the nozzle you picked it for.

* **Temperature tower heats the right nozzle** by @HanifKoh in [16898]({{L95}}) — on multi-tool printers, a temperature tower printed with any tool but the first stepped the temperature of the wrong nozzle. Each step now names the tool printing the tower. Fixes #16896.

## Interface Fixes

* **Keyboard shortcuts work again in the 3D view** by @raistlin7447 in [16558]({{L96}}) and [16673]({{L97}})
    In the alpha, typing in a text field drawn in the 3D view, such as the Text tool's, disabled every Global shortcut, so **Ctrl+S** and **Ctrl+P** stopped working there. They work again, while keys that edit text still go to the field. While a field, dropdown or popup in the 3D view is active, keys now go only to it instead of also triggering 3D-view shortcuts. **Esc** closes an open dropdown before it closes the tool, and a modifier key no longer gets stuck after a shortcut opens a dialog.

* **Sidebar sections stay open after closing a dialog** by @yw4z in [16600]({{L98}}) — closing a filament, printer or connection dialog with its button over the Printer or Filament title bar could fold that section.

* **"No available printers" in the send dialogs** by @HanifKoh in [16611]({{L99}}) — with no printer available, the printer box was blank and opened an empty strip.

* **Nozzle card hidden when there's nothing to choose** by @thelegendtubaguy in [16803]({{L100}}) — on non-Bambu multi-tool printers without nozzle flow variants, the sidebar no longer lists every tool with a "Standard"-only dropdown.

* **Official Bambu filament colors** by @bwees in [16706]({{L101}}) — clicking the color of a Bambu filament such as Bambu PLA Basic opened the generic color picker instead of the list of official colors. Fixes #16700.

* **Text fields open with their values** by @kenrap in [15881]({{L102}}) — some fields that should start with a value opened empty, such as the rename box for files attached on the Project page and the Bambu Lab connect-by-IP dialog.

* **Clearer Seam gap tooltip** by @tejas-devkar in [15983]({{L103}}) — it now says that a percentage value is relative to the nozzle diameter. Fixes #10147.

## Plugins

* **Bundled Python leaves the app untouched** by @HanifKoh in [16550]({{L104}}) — on macOS, the first start of the alpha rewrote files inside the app and broke its code signature, so a copy moved to another Mac failed Gatekeeper. Python's compiled files now go in OrcaSlicer's data folder, which also stops read-only installs such as the AppImage and Flatpak from recompiling them on every launch.

* **Plugins can't change their own permissions** by @peachismomo in [16634]({{L105}}) — plugins can no longer read or edit the file that records their granted permissions and enabled state.

* **Plugin threads go through permission checks** by @peachismomo in [16682]({{L106}}) — work a plugin does in its own threads now gets the same prompts and remembered grants as its main code, so a background thread can't get around them.

* **No prompts for Python's standard library** by @peachismomo in [16669]({{L107}}) — importing part of the standard library no longer asks about every file involved.

* **Plugins on Flatpak can use the data folder** by @peachismomo in [16685]({{L108}}) — every file a plugin opened in OrcaSlicer's data folder, its own included, was refused because the Flatpak's path contains a folder named `config`. Fixes #16656.

* **HTTPS works from plugins on macOS** by @SoftFever in [16638]({{L109}}) — every HTTPS request a plugin made failed with `CERTIFICATE_VERIFY_FAILED`. Fixes #16596.

* **Plugins start on more Windows PCs** by @lamweilun in [16888]({{L110}}) — on some computers, activating plugins failed with "Python Interpreter not initialized … The interpreter is already running."

* **Missing-plugin notices follow preset changes** by @lamweilun in [16897]({{L111}}) — the notice offering to install or enable a plugin the selected preset needs now appears or clears whenever presets change, plugins load or unload, or you start a new project.

## Linux, macOS & Windows

* **Mesh Boolean works again on Windows** by @raistlin7447 in [16651]({{L112}})
    In the alpha, every Mesh Boolean union, difference or intersection crashed OrcaSlicer on Windows within seconds. The same build problem could turn other rare errors into crashes on Windows, and both are fixed. macOS and Linux were not affected. Fixes #16581.

* **Random crashes on Apple silicon Macs** by @HanifKoh in [16686]({{L113}})
    On Apple silicon Macs, OrcaSlicer could crash at random in operations that fall back to exact arithmetic: importing textured models, embossed text and SVG cuts, mesh repair, Mesh Boolean and SLA hollowing. The bundled GMP math library is updated to a version that avoids the cause. This crash predates 2.5.0.

* **Linux no longer asks for the discrete GPU by default** by @HanifKoh in [16875]({{L114}})
    On Linux laptops with two GPUs, OrcaSlicer's desktop entry asked to run on the discrete GPU. On some Wayland sessions the 3D views then stayed empty when it was started from the menu or task bar, and on NVK the Flatpak could crash at startup. The Flatpak, AppImage and Desktop Integration entries drop that request. To use the discrete GPU, turn on the new **Preferences > General > Render on the discrete GPU** (Linux only, needs a restart); if OrcaSlicer then fails to open its window, start it once with `DRI_PRIME=0` and turn the option off. Fixes #16847.

* **Wayland dropdowns open and stay open** by @SoftFever in [16799]({{L115}}) and [16813]({{L116}}) — dropdowns open on the first click when a tooltip is showing, and resting on a preset with a truncated name no longer closes the list just as its full-name tooltip appears. Fixes #16595 and #16800.

* **Flatpak starts with any regional format** by @SoftFever in [16801]({{L117}}) — it failed to start when the desktop's currency, date or measurement formats used a language not installed for the Flatpak runtime. Fixes #16617.

* **Built-in web pages work in Linux virtual machines** by @lamweilun in [16598]({{L118}}) — in x86 VirtualBox, VMware and QEMU guests, the Device tab, setup wizard and other web pages were broken. They now work with WebKitGTK 2.44 or newer.

* **Web content at the right size on Windows** by @lamweilun in [16761]({{L119}}) — with the Windows text size above 100%, the web parts of dialogs such as the Color Picker, Plugins and Speed Dial looked zoomed in. They now scale with the monitor's DPI, like the rest of OrcaSlicer.

* **Mouse pointer stays visible after the Speed Dial on Windows** by @thelegendtubaguy and @lamweilun in [16880]({{L120}}) — with recent versions of Microsoft's WebView2, closing the Speed Dial with Enter after typing left the pointer hidden over all of OrcaSlicer until the dial was opened again. Fixes #16868.

* **Preview shows toolpaths on Parallels Desktop** by @SoftFever in [16829]({{L121}}) — Windows in a Parallels virtual machine on Apple silicon showed the legend and seams but no toolpaths.

## Crashes & Closing

* **OrcaSlicer always finishes closing** by @HanifKoh in [16766]({{L122}}), [16762]({{L123}}), [16763]({{L124}}), [16764]({{L125}}) and [16765]({{L126}})
    Closing OrcaSlicer could leave it stuck, frozen with its window still showing or running invisibly in the background. Causes included a plugin waiting on the interface while the app waited on the plugin, a plugin thread left running, and a printer warning dialog shown earlier in the session. These are fixed, and closing, starting a new project or opening another one while a slice is generating walls or infill no longer crashes either.

    As a last resort, if closing hasn't finished 30 seconds after it can no longer be cancelled, OrcaSlicer ends the process. Settings are saved while the app is idle and the project backup is kept, so the next start offers to restore it, but a preset sync or a G-code copy to a slow drive still running at that point is cut off. For plugin authors, `orca.host.ui` calls from a background thread raise `RuntimeError("OrcaSlicer is closing")` once the app is closing.

* **Crash right after starting a multi-filament slice** by @HanifKoh in [16649]({{L127}}) — it was most likely to happen after changing a setting that only affects the prime tower or G-code, such as the cyclic toolchange order.

* **Random crash while slicing in Russian** by @raistlin7447 in [16664]({{L128}}) — one of the daily tips shown while slicing was malformed in Russian and crashed the app whenever it came up. A malformed tip can no longer crash it in any language.

* **Send dialog crash with mixed printers** by @elcolumbio in [16599]({{L129}}) — **Print plate** crashed when the plate was sliced for a single-nozzle printer such as an A1 while the send dialog had a two-extruder printer such as an X2D selected. The dialog now shows the usual incompatible-printer message.

## Printer Connectivity & Cloud

* **Klipper printers no longer hang closing or startup** by @raistlin7447 in [16604]({{L130}}), [16675]({{L131}}) and [16668]({{L132}})
    When a Klipper-based printer connected through Moonraker, including the Snapmaker U1, Qidi and Creality K-series printers, stopped answering, for example after being powered off, closing OrcaSlicer never finished: the window went away but the process kept running, and on Windows the next launch ignored all input until the old process was killed. OrcaSlicer now exits in about a second, even while it is still connecting to a slow printer. With an offline printer selected, startup no longer freezes for about 5 seconds, and after switching quickly between presets for the same printer, filament sync follows the last one selected.

* **Creality fixes for unresponsive printers and K1 prints without a CFS** by @raistlin7447 and @HanifKoh in [16772]({{L133}}) and [16794]({{L134}})
    With a Creality CFS printer that accepted the connection and then stopped answering, opening the Creality send dialog or syncing filaments froze OrcaSlicer for good. Both give up after about 10 seconds instead, and an upload whose start command times out fails with the usual connection error.

    Prints sent to a K1, K1C or K1 SE without a CFS started as an empty multi-color job, so the printer reported "Consumable not detected" and runout monitors stopped the print at layer 0. They now start from the spool holder, as in Creality Print. Fixes #16695.

* **Qidi Box filament sync works with new firmware** by @thelegendtubaguy in [16679]({{L135}}) — after recent firmware updates for the Q2, Q2C, X-Plus 5 and X-Max 4, syncing filaments from the Qidi Box crashed OrcaSlicer. It now works with old and new firmware. Fixes #16660 and #16661.

* **Bambu Lab cloud features that did nothing** by @fer-marino in [15908]({{L136}}) — firmware information on the Device tab's Update page, rating a finished print on MakerWorld, the MakerWorld task list when sending to multiple printers, and the camera in the Part Skip and Send to Printer dialogs now reach the Bambu network plug-in.

* **HMS errors show their message on the X2D, A2L and H2C** by @downtime0 in [16267]({{L137}}) — printer errors showed as "Unknown error." instead of their message and code.

* **No reconnect after a Bambu Lab LAN print** by @downtime0 in [16271]({{L138}}) — sending a print over LAN to the selected printer disconnected and reconnected it, which could crash OrcaSlicer right after the job was sent.

* **H2C nozzle rack recognizes the filament in each hotend** by @HanifKoh in [16612]({{L139}}) — the H2C couldn't tell that a rack hotend already held the requested filament, and the Device tab couldn't name the filament in a rack nozzle.

* **Web Device page keeps its state** by @lamweilun and @SoftFever in [16755]({{L140}}) and [16806]({{L141}}) — switching back to the web Device tab, or reselecting the same printer, reloaded the printer's web interface (Mainsail, Fluidd and so on) and lost its state. On macOS, OrcaSlicer could also crash shortly after startup when the page finished loading while a context menu was open. Fixes #16752.

* **SimplyPrint imports the uploaded file** by @cjavad in [16555]({{L142}}) — with **Switch to Device tab after upload** ticked, the Device tab opened the SimplyPrint panel's home page instead of importing the file.

* **Unexpected Orca Cloud sign-outs** by @andrewsoonqn in [14781]({{L143}}) — on macOS and Linux, two cloud operations refreshing your login at the same moment could sign you out.

# 🧰 Platform & Build

* **Smaller install** by @yw4z in [16665]({{L144}}) — removing two unused Noto Sans KR fonts saves about 12 MB; Korean text has used NanumGothic for a long time. Embossed text set in Noto Sans KR on macOS and Flatpak now shows the "Can't load exactly same font" warning.

* **Image library security updates** by @mosfet80 and @raistlin7447 in [16819]({{L145}}), [16828]({{L146}}) and [16851]({{L147}}) — libpng is updated from 1.6.35 to 1.6.59, which fixes a long list of published vulnerabilities, and OpenCV, updated to 4.14.0, uses it instead of its own older copy for PNG textures in imported models.

* **FreeType removed** by @raistlin7447 in [16852]({{L148}}) — OrcaSlicer no longer builds or ships the unused library.

* **Build against system Boost 1.87 or newer** by @kenrap in [15835]({{L149}}) — for FreeBSD and Linux distribution packagers.

* **Gentoo in `build_linux.sh`** by @MihaiMocanuGit in [16566]({{L150}}) — `./build_linux.sh -u` recognizes Gentoo again and installs its dependencies. Fixes #16567.

# 🖨️ Printer & Filament Profiles

## New Printer Profiles

* **Qidi X-Smart 5** — 180 × 180 × 180 mm Klipper printer with 0.2, 0.4, 0.6 and 0.8 mm nozzles, bed model, 17 process presets and about 57 filament profiles, by @QIDI-Official in [16734]({{L151}})

## New Filament Profiles

* **School House Spools** — Matte PLA, Silk PLA, Marble PLA, TPU 95A, Matte PETG and Transparent PETG in the Orca Filament Library, by @getsmart77 in [16780]({{L152}})

## Profile Updates & Fixes

* **Profile changes reach existing installs** — the Orca Filament Library and the Elegoo, M3D, Meltingplot, OrcaArena, Pragostroj, Qidi, RH3D, Wanhao France and WonderMaker bundles changed without a version bump, so installs that already had them kept the old profiles. Their versions are raised, so changes such as the School House Spools filaments and the Qidi X-Smart 5 install on upgrade, by @HanifKoh in [16919]({{L153}}) and [16924]({{L154}})

* **AnkerMake M5, M5 All-Metal and M5C** — G-code files start with the filament weight and length, layer height and first-layer nozzle temperature, so the printer's touchscreen shows the filament used, by @robertbaker in [16571]({{L155}})

* **Anycubic Kobra 2** — the 0.4 mm profile's layer-change G-code writes its layer line as a comment instead of an invalid command, by @RJAudas in [16381]({{L156}}) (Fixes #16219)

* **Bambu Lab** — the filament **Exhaust fan** settings are back on the X1, X1 Carbon, P1S, P2S, H2D, H2D Pro, H2S and X2D, including in projects saved with the alpha, so filaments that use air filtration run the exhaust fan again as in 2.4.2, by @SoftFever in [16792]({{L157}}) (Fixes #14013)

* **Flashforge** — Adventurer 5M, 5M Pro, AD5X, Adventurer A5, Creator 5 and Creator 5 Pro presets set **Outline tolerance** to 0.2 mm, so crowded plates are less likely to hit "Timer too close", by @ghzserg in [16687]({{L158}})

* **Qidi** — the Q2, Q2C and X-Max 4 get the bed plate type selector, X-Max 4 and X-Plus 5 process presets turn off **Enable accel_to_decel**, and X-Plus 5 presets set the small perimeter threshold to 0, by @QIDI-Official in [16734]({{L159}})

* **re:3D GigabotX 2, GigabotX 2 XLT and TerabotX 2** — **Seam gap** is 10% of the nozzle diameter instead of 10 mm, by @re3Dev in [16739]({{L160}})

* **Snapmaker U1** — the start G-code sets the top cover purifier from the filaments on the plate (strong cooling for PLA and TPU, weak for PETG, keep-warm for ABS and ASA) and follows the rest of Snapmaker's latest start G-code, with U1 filament softening temperatures from Snapmaker. It needs U1 firmware 1.3.0 or later; older firmware reports an unknown command and keeps printing. By @raistlin7447 in [16590]({{L161}})

* **Snapmaker** — process presets use the top and bottom paint penetration values from Snapmaker's own build of OrcaSlicer: some U1 presets color deeper and others shallower, and many A250, A350, Artisan and J1 presets color fewer layers, saving filament changes on painted prints, by @ianalexis in [16821]({{L162}})

# 🗪 Localization

* **Translation gaps filled across all 22 languages** by @ianalexis in [16652]({{L163}}) and [16815]({{L164}})
    The untranslated strings in all 22 languages, mainly color names, align and distribute, statistics export and plugin strings, were filled with AI translations marked for review. Several color names in the color picker are corrected in every language, and RAL 5019 Capri blue now has a blue swatch instead of a purple one. Some strings added later in the beta are not yet translated in every language.

* Simplified Chinese translation revised by @SoftFever in [16865]({{L165}}), fixing about 475 strings for meaning, consistent terms and natural wording, and the new strings translated into Simplified and Traditional Chinese in [16904]({{L166}})
* Japanese translation revised by @SoftFever in [16874]({{L167}}), fixing about 940 strings, including tooltips that said the opposite of the English, and the new strings translated in [16905]({{L168}})
* French translation updates by @Surfoo in [16591]({{L169}}), with about 425 new strings and term fixes, and the new strings translated by @SoftFever in [16908]({{L170}})
* German translation of the new strings by @SoftFever in [16907]({{L171}})
* Brazilian Portuguese color picker translated by @afmenez in [16585]({{L172}}), and about 350 AI translations reviewed in [16749]({{L173}})
* Basque translation updates by @mgoiogana in [16666]({{L174}})
* Consistent spelling of "G-code", "SVG", "GitHub" and "IP" in English messages by @afmenez in [16618]({{L175}})

---

# ❤️ Support OrcaSlicer

> **OrcaSlicer is — and will remain — free and open source.**
>
> Every release represents countless hours of behind-the-scenes work: building features, fixing bugs, validating profiles, and testing across real machines.
>
> If OrcaSlicer helps you bring ideas to life, please consider supporting the project. Donations are used to support the open-source contributors who help build and maintain OrcaSlicer, and to cover project costs such as servers, development tools, test machines, filament, printer parts, and other infrastructure.
>
> Your support helps us keep improving OrcaSlicer for everyone — while keeping the project free, open, and community-driven.
>
> **Thank you for being part of the OrcaSlicer journey.** 🙏

<p align="center">
  <a href="{{L179}}">{{I34}}</a>
</p>
<p align="center">
  <a href="{{L180}}">{{I35}}</a>
</p>
