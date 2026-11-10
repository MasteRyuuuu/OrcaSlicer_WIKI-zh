# Cornering

Cornering is a critical aspect of 3D printing that affects print quality and accuracy. It's how the printer handles changes in direction during movement, particularly at corners and curves.  
Proper cornering settings can reduce artifacts such as ringing, ghosting, and overshooting, resulting in cleaner and more precise prints.

> [!IMPORTANT]
> This test will help you find the Maximum Cornering settings your printer can handle without losing print quality.  
> If you are not experiencing issues with corners in your prints and are satisfied with the print speed, you may choose to skip this calibration.

> [!TIP]
> Follow the recommended calibration order in the [Calibration Guide]({{L1}}).

## Types of Cornering Settings

> [!TIP]
> Read more in [Jerk XY]({{L2}}) and check [Cornering Control Types]({{L3}})

## Calibration

This test automatically detects your printer firmware type and adapts the calibration process to it.

- Klipper: [square_corner_velocity]({{L4}})
- Marlin 2:
    - [Junction Deviation]({{L5}}) if `Maximum Junction Deviation` in Printer settings/Motion ability/Jerk limitations is bigger than `0`.
    - [Classic Jerk]({{L6}}) if `Maximum Junction Deviation` is set to `0`.
- Marlin Legacy: [Classic Jerk]({{L7}}).
- RepRap: [Maximum instantaneous speed changes]({{L8}})

> [!WARNING]
> **The firmware limits cornering, and OrcaSlicer can't check that limit.**  
> OrcaSlicer sends the test values to the printer, but it can't read what the firmware actually applies. Above the firmware limit, a higher value doesn't make corners faster in real prints, and the rest of the tower prints the same.
>
> - **Klipper:** the corner speed is also limited by the print speed, the acceleration and the length of the moves, so above a certain `square_corner_velocity` the corners don't get any faster. To see the value in use, send `SET_VELOCITY_LIMIT` without parameters in the console while the test prints.
> - **Marlin 2 (Junction Deviation):** only values between `0.01` and `0.3` mm are accepted. Values outside this range are ignored.
> - **Marlin (Classic Jerk):** firmware built with `LIMITED_JERK_EDITING` caps the jerk values (by default to twice the firmware default). Send `M503` to see the values in use.

> [!NOTE]
> This calibration example uses Junction Deviation as an example. The process is similar for Jerk calibration; just read the Jerk values instead of JD values.  
> JD values are between `0.0` and `0.3` (in mm) while Jerk values are usually between `1` and `20` or higher (in mm/s).

1. Pre-requisites:
    1. If using Marlin 2 firmware, Check if your printer has Junction Deviation enabled. Look for `Junction deviation` in the printer's advanced settings.
    2. In OrcaSlicer, set:
        1. Acceleration high enough to trigger ringing or the speed you want to check out (e.g., 2000 mm/s²).
        2. Speed high enough to trigger ringing (e.g., 100 mm/s).
    3. Use an opaque, high-gloss filament to make ringing more visible.
2. Open the Cornering test.  
   {{I1}}
    1. In this first approximation, set a wide range of Start and End values.
        - If you don't see any loss of quality, increase the End value and retry. If the whole tower still looks the same, you have probably reached the firmware limit (see the warning above), and a higher value won't help.
        - If you do see a loss of quality, measure the maximum height when the corners start losing sharpness and read the Cornering/Jerk/JunctionDeviation value set at that point in OrcaSlicer.  
        {{I2}}  
        {{I3}}
    2. Print a new calibration tower with a maximum set near the point where corners start losing sharpness.  
      **RECOMMENDED:** Use the *Ringing Tower* test model to more easily visualize the jerk limit.
    3. Print the second Cornering test with the new maximum value.  
      {{I4}}
    4. Measure the maximum height when the corners start losing sharpness and read the Cornering/Jerk/JunctionDeviation value set at that point in OrcaSlicer.  
      {{I5}}  
      {{I6}}
3. Save the settings
    - Into your OrcaSlicer printer profile (**RECOMMENDED**):
        1. Go to Printer [settings → Motion ability → Jerk limitation]({{L9}}):
        2. Set your maximum Jerk X and Y or Junction Deviation values.  
        {{I7}}
    - Directly into your printer firmware:
        - Restore your 3D Printer settings to avoid keeping high acceleration and jerk values used for the test.

        - Klipper:
            - Skeleton:

            {{C1}}

            Example:

            {{C2}}

           Note: You can also set `square_corner_velocity` persistently in your `printer.cfg` (restart required).

        - Marlin 2 (Junction Deviation enabled):
            - Skeleton:

            {{C3}}

            - Example:

            {{C4}}

        - To make the change permanent in firmware, set in `Configuration.h` and recompile:

        {{C5}}

        Also ensure classic jerk is disabled if using junction deviation:

        {{C6}}

        - Marlin Classic Jerk / Marlin Legacy:
            - Skeleton: — set the per-axis jerk limits using `M205` (X/Y optional depending on firmware build):

            {{C7}}

            - Example:

            {{C8}}

        - RepRap (Duet / RepRapFirmware):  
            **IMPORTANT:** Set in mm/min so convert from mm/s to mm/min multiply by 60.
            - Skeleton:

            {{C9}}

            - Example (Duet-style):

            {{C10}}

> [!NOTE]
> RepRapFirmware exposes `M566` to set allowable instantaneous speed changes; some boards may persist settings with `M500` or via their web/config files.

## Credits

- **Junction Deviation Machine Limit** [@RF47]({{L10}})
- **Cornering Calibration** [@IanAlexis]({{L11}})
- **Fast tower model** [@RF47]({{L12}})
- **SCV-V2 model** [@chrisheib]({{L13}})
