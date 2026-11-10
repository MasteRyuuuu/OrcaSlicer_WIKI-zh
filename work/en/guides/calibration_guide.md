# Calibration Guide

This guide offers a structured and comprehensive overview of the calibration process for OrcaSlicer.

It covers key aspects such as flow ratio, pressure advance, temperature towers, retraction tests, and advanced calibration techniques. Each section includes step-by-step instructions and visuals to help you better understand and carry out each calibration effectively.

To access the calibration features, you can find them in the **Calibration** section of the OrcaSlicer interface.

{{I12}}

> [!IMPORTANT]
> After completing the calibration process, remember to create a new project in order to exit the calibration mode.

> [!TIP]
> <strong class="orca-video-title">Recommended</strong>
>
> <span class="orca-video-description">Filament Calibration Masterclass</span>
>
> <div class="orca-video-embed">
>   <a class="orca-video-poster-link" href="{{L20}}" aria-label="Watch Filament Calibration Masterclass video by Factorian Designs">
>     {{I1}}
>   </a>
> </div>
>
> <span class="orca-video-credit">Video by <strong>Factorian Designs</strong>, with consent.</span>

The calibrations are split into two groups. Follow them in the order shown, as each test builds on the results of the ones before it.

> [!NOTE]
> These tests assume the extruder itself is already calibrated in the printer firmware (E-steps or rotation distance). Most modern printers ship with this set correctly. Small differences between filaments are corrected later in the [Flow Ratio]({{L1}}) step.

## Filament Calibration

Repeat these tests for each new filament.

1. **[Temperature]({{L2}}):** Start by calibrating the nozzle temperature. This is crucial as it affects the viscosity of the filament, which in turn influences how well it flows through the nozzle and adheres to the print bed, so every following test depends on it. The test is quick, easy to read and works with any material on any printer. It is especially important for materials with a narrow temperature range.  
   {{I2}}
2. **[Max Volumetric Speed]({{L3}}):** With the temperature set, find the maximum volumetric speed the hotend can reach with this filament. This sets a safe limit so the following tests don't under-extrude or clog the nozzle. Some manufacturers overstate this value, so don't rely on the one on the spool. Use a value 10–20% below the result as a safety margin.  
   {{I3}}
3. **[Pressure Advance]({{L4}}):** Calibrate the pressure advance settings to improve print quality and reduce artifacts caused by pressure fluctuations in the nozzle. It is done before Flow Ratio because it is the value most often wrong (or never calibrated at all), while the flow ratio in most filament profiles is already close. A tuned pressure advance also gives cleaner line ends and corners, which makes the Flow Ratio test easier to read.  
   {{I4}}
4. **[Flow Ratio]({{L5}}):** Calibrate the flow ratio to ensure that the correct amount of filament is being extruded. This is important for achieving accurate dimensions and good layer adhesion. The test starts from the flow ratio of the selected filament profile, so it is usually a small correction.  
   {{I5}}
5. **[Retraction]({{L6}}):** Calibrate the retraction settings to minimize stringing and improve print quality. The default values usually work well, but if you calibrate them, do it after Pressure Advance and Flow Ratio, as both change the pressure in the nozzle. Retraction doesn't depend on the advanced tests below, so it is part of the filament calibration.  
   {{I6}}

> [!TIP]
> Pressure advance and flow ratio affect each other slightly, so either can be calibrated first. If the flow ratio changed a lot in the Flow Ratio step, run a quick Pressure Advance test again.

## Advanced Calibration

These tests are optional. Most of them tune the printer rather than the filament, so they only need to be repeated after hardware changes. Do them after the filament calibration, as a badly tuned filament affects their results.

1. **[Cornering]({{L7}}):** Calibrate the Jerk/Junction Deviation settings to improve print quality and reduce artifacts caused by sharp corners and changes in direction. It is mainly used to raise cornering speed. Most printers don't need it, as their firmware already limits cornering: above that limit (especially in Klipper) a higher value doesn't make real prints any faster, and OrcaSlicer has no way to check it.  
   {{I7}}
2. **[Input Shaping]({{L8}}):** Reduce ringing and improve print quality by compensating for mechanical vibrations in the printer. Most recent printers have their own automatic input shaping calibration, which is usually more accurate than this manual test, so use it when available.  
   {{I8}}
3. **[VFA]({{L9}}):** A VFA speed test is available to find resonance speeds. Do it after Input Shaping to find the Vertical Fine Artifacts that input shaping didn't remove.  
   {{I9}}
4. **[Adaptive Pressure Advance]({{L10}}):** Adjusts the pressure advance value for different flow rates and accelerations. It needs a calibrated Pressure Advance and Flow Ratio, and its tests [should not go above the acceleration limit found with Input Shaping]({{L11}}).  
   {{I10}}

---

**[Tolerance]({{L12}}):** Calibrate the tolerances of your printer to ensure that it can accurately reproduce the dimensions of the model being printed. This is important for achieving a good fit between parts and for ensuring that the final print meets the desired specifications. Do it last, as the result depends on every calibration above.  
{{I11}}

---

_Credits:_

- _The Flow test and retraction test is inspired by [SuperSlicer]({{L13}})._
- _The PA Line method is inspired by [K-factor Calibration Pattern]({{L14}})._
- _The PA Tower method is inspired by [Klipper]({{L15}})._
- _The temp tower model is remixed from [Smart compact temperature calibration tower]({{L16}})._
- _The max flowrate test was inspired by Stefan (CNC Kitchen), and the model used in the test is a remix of his [Extrusion Test Structure]({{L17}})._
- _ZV Input Shaping is inspired by [Marlin Input Shaping]({{L18}}) and [Ringing Tower 3D STL]({{L19}})._
