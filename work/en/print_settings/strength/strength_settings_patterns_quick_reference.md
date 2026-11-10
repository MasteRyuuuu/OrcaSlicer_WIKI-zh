## Patterns Quick Reference

| - | Pattern | Strength | Material Usage | Print Time | Layer time Variability | Multiline | Multiline 2 / 3 lines<br>Material, Time |
|---|---|---|---|---|---|---|---|
| {{I1}} | [Monotonic]({{L1}}) | X-Y: {{I30}}<br> Z: {{I31}} | {{I32}} | {{I33}} | {{I34}} | N/A | - |
| {{I2}} | [Monotonic line]({{L2}}) | X-Y: {{I35}}<br> Z: {{I36}} | {{I37}} | {{I38}} | {{I39}} | N/A | - |
| {{I3}} | [Rectilinear]({{L3}}) | X-Y: {{I40}}<br> Z: {{I41}} | {{I42}} | {{I43}} | {{I44}} | [Classic]({{L4}}) | 2: {{I45}} {{I46}}<br> 3: {{I47}} {{I48}} |
| {{I4}} | [Aligned Rectilinear]({{L5}}) | X-Y: {{I49}}<br> Z: {{I50}} | {{I51}} | {{I52}} | {{I53}} | [Classic]({{L6}}) | 2: {{I54}} {{I55}}<br> 3: {{I56}} {{I57}} |
| {{I5}} | [Zig Zag]({{L7}}) | X-Y: {{I58}}<br> Z: {{I59}} | {{I60}} | {{I61}} | {{I62}} | No | - |
| {{I6}} | [Cross Zag]({{L8}}) | X-Y: {{I63}}<br> Z: {{I64}} | {{I65}} | {{I66}} | {{I67}} | No | - |
| {{I7}} | [Locked Zag]({{L9}}) | X-Y: {{I68}}<br> Z: {{I69}} | {{I70}} | {{I71}} | {{I72}} | No | - |
| {{I8}} | [Line]({{L10}}) | X-Y: {{I73}}<br> Z: {{I74}} | {{I75}} | {{I76}} | {{I77}} | No | - |
| {{I9}} | [Grid]({{L11}}) | X-Y: {{I78}}<br> Z: {{I79}} | {{I80}} | {{I81}} | {{I82}} | [Non-Crossing]({{L12}}) | 2: {{I83}} {{I84}}<br> 3: {{I85}} {{I86}} |
| {{I10}} | [Triangles]({{L13}}) | X-Y: {{I87}}<br> Z: {{I88}} | {{I89}} | {{I90}} | {{I91}} | [Non-Crossing]({{L14}}) | 2: {{I92}} {{I93}}<br> 3: {{I94}} {{I95}} |
| {{I11}} | [Tri-hexagon]({{L15}}) | X-Y: {{I96}}<br> Z: {{I97}} | {{I98}} | {{I99}} | {{I100}} | [Non-Crossing]({{L16}}) | 2: {{I101}} {{I102}}<br> 3: {{I103}} {{I104}} |
| {{I12}} | [Cubic]({{L17}}) | X-Y: {{I105}}<br> Z: {{I106}} | {{I107}} | {{I108}} | {{I109}} | [Non-Crossing]({{L18}}) | 2: {{I110}} {{I111}}<br> 3: {{I112}} {{I113}} |
| {{I13}} | [Adaptive Cubic]({{L19}}) | X-Y: {{I114}}<br> Z: {{I115}} | {{I116}} | {{I117}} | {{I118}} | [Non-Crossing]({{L20}}) | 2: {{I119}} {{I120}}<br> 3: {{I121}} {{I122}} |
| {{I14}} | [Quarter Cubic]({{L21}}) | X-Y: {{I123}}<br> Z: {{I124}} | {{I125}} | {{I126}} | {{I127}} | [Non-Crossing]({{L22}}) | 2: {{I128}} {{I129}}<br> 3: {{I130}} {{I131}} |
| {{I15}} | [Support Cubic]({{L23}}) | X-Y: {{I132}}<br> Z: {{I133}} | {{I134}} | {{I135}} | {{I136}} | [Non-Crossing]({{L24}}) | 2: {{I137}} {{I138}}<br> 3: {{I139}} {{I140}} |
| {{I16}} | [Lightning]({{L25}}) | X-Y: {{I141}}<br> Z: {{I142}} | {{I143}} | {{I144}} | {{I145}} | [Classic]({{L26}}) | 2: {{I146}} {{I147}}<br> 3: {{I148}} {{I149}} |
| {{I17}} | [Honeycomb]({{L27}}) | X-Y: {{I150}}<br> Z: {{I151}} | {{I152}} | {{I153}} | {{I154}} | [Classic]({{L28}}) | 2: {{I155}} {{I156}}<br> 3: {{I157}} {{I158}} |
| {{I18}} | [3D Honeycomb]({{L29}}) | X-Y: {{I159}}<br> Z: {{I160}} | {{I161}} | {{I162}} | {{I163}} | [Non-Crossing]({{L30}}) | 2: {{I164}} {{I165}}<br> 3: {{I166}} {{I167}} |
| {{I19}} | [Lateral Honeycomb]({{L31}}) | X-Y: {{I168}}<br> Z: {{I169}} | {{I170}} | {{I171}} | {{I172}} | [Classic]({{L32}}) | 2: {{I173}} {{I174}}<br> 3: {{I175}} {{I176}} |
| {{I20}} | [Lateral Lattice]({{L33}}) | X-Y: {{I177}}<br> Z: {{I178}} | {{I179}} | {{I180}} | {{I181}} | [Classic]({{L34}}) | 2: {{I182}} {{I183}}<br> 3: {{I184}} {{I185}} |
| {{I21}} | [Cross Hatch]({{L35}}) | X-Y: {{I186}}<br> Z: {{I187}} | {{I188}} | {{I189}} | {{I190}} | [Classic]({{L36}}) | 2: {{I191}} {{I192}}<br> 3: {{I193}} {{I194}} |
| {{I22}} | [TPMS-D]({{L37}}) | X-Y: {{I195}}<br> Z: {{I196}} | {{I197}} | {{I198}} | {{I199}} | [Classic]({{L38}}) | 2: {{I200}} {{I201}}<br> 3: {{I202}} {{I203}} |
| {{I23}} | [TPMS-FK]({{L39}}) | X-Y: {{I204}}<br> Z: {{I205}} | {{I206}} | {{I207}} | {{I208}} | [Classic]({{L40}}) | 2: {{I209}} {{I210}}<br> 3: {{I211}} {{I212}} |
| {{I24}} | [Gyroid]({{L41}}) | X-Y: {{I213}}<br> Z: {{I214}} | {{I215}} | {{I216}} | {{I217}} | [Classic]({{L42}}) | 2: {{I218}} {{I219}}<br> 3: {{I220}} {{I221}} |
| {{I25}} | [Concentric]({{L43}}) | X-Y: {{I222}}<br> Z: {{I223}} | {{I224}} | {{I225}} | {{I226}} | [Classic]({{L44}}) | 2: {{I227}} {{I228}}<br> 3: {{I229}} {{I230}} |
| {{I26}} | [Spiral Inset]({{L45}}) | X-Y: {{I231}}<br> Z: {{I232}} | {{I233}} | {{I234}} | {{I235}} | N/A | - |
| {{I27}} | [Hilbert Curve]({{L46}}) | X-Y: {{I236}}<br> Z: {{I237}} | {{I238}} | {{I239}} | {{I240}} | [Classic]({{L47}}) | 2: {{I241}} {{I242}}<br> 3: {{I243}} {{I244}} |
| {{I28}} | [Archimedean Chords]({{L48}}) | X-Y: {{I245}}<br> Z: {{I246}} | {{I247}} | {{I248}} | {{I249}} | [Classic]({{L49}}) | 2: {{I250}} {{I251}}<br> 3: {{I252}} {{I253}} |
| {{I29}} | [Octagram Spiral]({{L50}}) | X-Y: {{I254}}<br> Z: {{I255}} | {{I256}} | {{I257}} | {{I258}} | [Classic]({{L51}}) | 2: {{I259}} {{I260}}<br> 3: {{I261}} {{I262}} |

> [!NOTE]
> These estimates are the mean of a 100 mm cube, a 3DBenchy and the Stanford bunny, sliced on a Qidi Q2 with a 0.4 mm nozzle, the 0.20mm Standard profile and QIDI PLA Rapido at 5, 15, 30 and 50% sparse infill density, measuring only the sparse infill and the travel in the layers that print it. The patterns that only print solid infill are measured at 100% on their internal solid infill and compared with the other patterns used as solid infill. Layer time variability comes from the cube alone.  
> They **WILL NOT** be the same for all models and only serve as a standard guideline.

> [!TIP]
> You can see how this analysis was made in [infill-analysis]({{L52}}) folder:
>
> - [infill_analysis.py]({{L53}}) slices a 100 mm cube and OrcaSlicer's 3DBenchy and Stanford bunny with every pattern and density with the OrcaSlicer CLI, changing the profile settings listed in it, and rates the material usage, print time and layer time variability above from its [statistics]({{L54}}).
> - [infill_patterns.csv]({{L55}}) holds the strength ratings, which are set by hand.
> - [infill_analysis_results.csv]({{L56}}) holds the measured values, and [infill_analysis_runs.csv]({{L57}}) those of every slice.
