# G-Code Output

These settings control how G-code is generated and formatted. They impact readability, file size, print behavior, and compatibility with firmware and post-processing tools.

{{T1}}

## Reduce Infill Retraction

{{M1}}
When enabled, the slicer will skip retractions for travel moves that occur entirely inside infill regions. This reduces the number of retractions and can speed up printing for complex models, but it may increase oozing or stringing inside infill. Slicing time may also increase slightly.

Each retraction adds moves that print nothing, and a travel that skips it skips all of them, keeping only the travel itself:

- The [retraction]({{L1}}) pulls the filament back at the [Retraction speed]({{L2}}) before the travel, and the [deretraction]({{L3}}) pushes it back, plus any [Extra length on restart]({{L4}}), before the next line starts. With the default 0.8 mm at 30 mm/s, each of the two takes about 27 ms.
- With [Wipe while retracting]({{L5}}), the nozzle also moves back along the last line for the [Wipe distance]({{L6}}) while it retracts.
- With a [Z-hop]({{L7}}), the nozzle lifts before the travel and lowers after it, on the Z axis, which on most printers is much slower than X and Y.

Tens of milliseconds per travel can add up to minutes over the thousands of infill travels of a large print.

Travels shorter than the [Travel distance threshold]({{L8}}) never retract, with or without this option. Infill lines whose ends are next to each other are joined into one path (see [Anchor]({{L9}})), so there is no travel to retract for between them.

**Recommended** when internal cosmetic quality is not critical and you want fewer retractions.

## Add line number

{{M2}}
Prefix each G-code line with a sequential line number (N1, N2, ...). Useful for debugging or tools that expect numbered G-code.

## Verbose G-code

{{M3}}
Include descriptive comments for G-code lines and blocks to make the file human-readable and easier to debug.  
Verbose mode produces much larger files and may slow down SD-card printing on some printers.

## High precision G-code

{{M4}}

Writes the X, Y, Z, I and J coordinates with 4 decimal places instead of 3, and E with 6 instead of 5, to reduce rounding errors in the G-code. Feedrates keep 3 decimal places.  
With [relative E distances]({{L10}}), the rounding error of each move is also carried over to the next one, so short moves of about the same length don't all round the flow in the same direction.

This may help stabilize extrusion with small nozzles (e.g. 0.2 mm) and thin layers (e.g. 0.08 mm or less), where each move extrudes so little material that rounding errors matter most. The effect depends strongly on how well the rest of the settings are tuned and may be hard to notice unless the filament and print profiles are well [calibrated]({{L11}}).

- **Supports** are removed after printing, so they keep the standard precision. Support ironing keeps the higher precision, as it smooths the surface the object is printed on.
- **File size:** the G-code becomes about 10% larger, which may slow down printers that parse G-code slowly.
- **Off:** the G-code is the same as before this option existed.

## Label Objects

{{M5}}
Insert comments that label moves with the object they belong to (object index or name). This is useful for integrations such as OctoPrint's Cancel Object plugin and for human inspection of the G-code.

## Exclude Objects

{{M6}}
Add commands to the G-code that define each object and mark where it starts and ends, so the printer firmware can skip (cancel) individual objects during the print: `EXCLUDE_OBJECT_DEFINE`, `EXCLUDE_OBJECT_START` and `EXCLUDE_OBJECT_END` for Klipper, and `M486` for Marlin and RepRapFirmware.

### Outline Tolerance

{{M7}}

Controls the precision of the exclude-object outlines simplified via the Douglas-Peucker algorithm. This setting only applies to **Klipper** firmware (`EXCLUDE_OBJECT_DEFINE` lines), as Marlin and RepRapFirmware use `M486` commands without polygon definitions.

* **Default:** `0.1 mm`.
* **When to adjust:** If your printer has a limited CPU capacity and you are printing a full plate with many objects, highly detailed outlines can generate very large arrays. Processing these lines or running macros that iterate over them (such as KAMP adaptive meshing) can cause Klipper to trigger a `Timer too close` error.
* **Recommendation:** Raising this value to `0.2 mm` - `0.4 mm` significantly reduces the total number of points and prevents printer timeouts, with a negligible impact on outline precision. Setting it to `0` retains every point of the convex hull.

## Filename Format

{{M8}}
Define a filename template for exported G-code. Templates may include tokens like project name, date, or other metadata to produce consistent and informative filenames on export.

For example:

{{C1}}

This can be used to generate filenames like `OrcaCube_PLA_1h15m.gcode`.

> [!TIP]
> Check [File Name Template]({{L12}}) for available tokens and their meanings.

## Change extrusion role G-code

{{M9}}
This G-code is inserted when the [extrusion role]({{L13}}) is changed.  
This is the process version of the **Change extrusion role G-code** that is also available in the [Material settings]({{L14}}) and [Printer settings]({{L15}}), and it runs after both of them.

> [!TIP]
> Read the [Printer settings]({{L16}}) for more details and examples.
