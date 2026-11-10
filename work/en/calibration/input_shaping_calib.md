# Input Shaping

This Calibration guide will help you to calibrate the [Input Shaping]({{L1}}) feature in your printer firmware.

> [!NOTE]
> Some Printers have built-in accelerometers that can be used to **automatically** measure the resonant frequencies of the printer.  
> If your printer has one, consider using it as it can provide more accurate results in less time and usually is autosaved into the printer firmware.

> [!TIP]
> Follow the recommended calibration order in the [Calibration Guide]({{L2}}).

> [!TIP]
> It's usually recommended to perform Input Shaping calibration once a year or after any mechanical or structural changes such as relocation, changing the support surface, new belts, motors, frame, etc.

{{T1}}

## Calibration

Pre-requisites:

- Use an opaque, high-gloss filament to make the ringing more visible.
- In OrcaSlicer, set:
    - Acceleration high enough to trigger ringing (e.g., 20000 mm/s²).
    - Speed high enough to trigger ringing (e.g., 200 mm/s).

> [!IMPORTANT]
> It's recommended to use the fastest [acceleration]({{L3}}), [speed]({{L4}}) and [Jerk/Junction Deviation]({{L5}}) your printer can handle without losing steps.  
> This test **will set the values to high values** limited by your printer's motion ability and the filament's max volumetric speed (avoid materials below 10 mm³/s).

1. Select the Test Model ´Ringing Tower´ (Recommended) or ´Fast Tower´ (Reduced version useful for printers with high ringing).
2. Select the [Input Shaper Type]({{L6}}) you want to test. Each firmware has different types available and each type has different performance.
3. Select a range of frequencies to test. The Default 15hz to 110hz range is usually a good start.
4. Select your damping. Usually, a value between 0.1 and 0.2 is a good start but you can change it to 0 and your printer will use the firmware default value (if available).  
   {{I1}}
    1. **Measure the X and Y heights** and read the frequency set at that point in OrcaSlicer.  
    {{I2}}
        - Marlin:  
          {{I3}}
        - Klipper:  
          {{I4}}
    2. If not a clear result, you can measure a X and Y min and max acceptable heights and repeat the test with that min and max value.
5. **Print the Damping test** setting your X and Y frequency to the value you found in the previous step.  
   {{I5}}
    1. Measure the X and Y heights and read the damping set at that point in OrcaSlicer.  
       {{I6}}
        - Marlin:  
        {{I7}}
        - Klipper:  
        {{I8}}
6. **Restore your 3D Printer settings to avoid keep using high acceleration and jerk values.**
7. **Save the settings**
    - Into your printer firmware settings save the values you found (Type, frequency/cies and damp)
    - Save it into Orca's printer profile settings:
        - Motion ability → Resonance Compensation (**Marlin**/**RepRap**):
            1. [Go to Printer settings → Motion ability → Resonance Compensation]({{L7}}):
            2. Set your Type, Frequencies and Damping values.  
            {{I9}}
        - Machine start G-code:
            - Klipper:
                - Skeleton:

                {{C1}}

                - Example:

                {{C2}}

            - Marlin:
                - Skeleton:

                {{C3}}

                - Example

                {{C4}}

            - RepRap:
                - Skeleton: for RepRap 3.3 and later

                {{C5}}

                - Example RepRap 3.4 and later

                {{C6}}

                - Skeleton: for RepRap 3.2 and earlier

                {{C7}}

                - Example Legacy (RepRap 3.2 and earlier)

                {{C8}}

## Credits

- **Input Shaping Calibration:** [@IanAlexis]({{L8}}) and [@RF47]({{L9}})
- **Klipper testing:** [@ShaneDelmore]({{L10}})
