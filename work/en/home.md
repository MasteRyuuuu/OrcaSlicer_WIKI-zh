# Welcome to the OrcaSlicer Wiki

OrcaSlicer is a powerful open source slicer for FFF (FDM) 3D Printers. This wiki page aims to provide an detailed explanation of the slicer settings, how to get the most out of them as well as how to calibrate and setup your printer.

{{T1}}

> [!NOTE]
> Please consider contributing to the wiki following the [How to contribute to the wiki]({{L1}}) guide.

## Printer Settings

{{I119}}  
{{I1}} Settings related to the 3D printer hardware and its configuration.

- Basic Information
    - [{{I2}} Printable space]({{L2}})
    - [{{I3}} Advanced]({{L3}})
    - [{{I4}} Belt printer]({{L4}})
    - [{{I5}} Machine frame transforms]({{L5}})
    - [{{I6}} Cooling Fan]({{L6}})
    - [{{I7}} Extruder Clearance]({{L7}})
    - [{{I8}} Adaptive bed mesh]({{L8}})
    - [{{I9}} Accessory]({{L9}})
- [{{I10}} Machine G_Code]({{L10}})
- Multimaterial
    - [{{I11}} Multimaterial setup]({{L11}})
    - [{{I12}} Wipe tower]({{L12}})
    - [{{I13}} Single extruder multi_material parameters]({{L13}})
    - [{{I14}} Advanced]({{L14}})
    - [{{I15}} IDEX/IQEX Configuration]({{L15}})
- Extruder
    - [{{I16}} Basic Information]({{L16}})
    - [{{I17}} Retraction]({{L17}})
        - [{{I18}} Retraction when switching materials]({{L18}})
    - [{{I19}} Z_Hop]({{L19}})
- [{{I20}} Motion ability]({{L20}})

## Material Settings

{{I120}}  
{{I21}} Settings related to the 3D printing material.

- Material settings
    - [{{I22}} Basic Information]({{L21}})
    - [{{I23}} Flow Ratio and Pressure Advance]({{L22}})
    - [{{I24}} Material temperatures]({{L23}})
        - [{{I25}} Print Chamber temperature]({{L24}})
        - [{{I26}} Print temperature]({{L25}})
        - [{{I27}} Bed temperature]({{L26}})
    - [{{I28}} Volumetric Speed limitation]({{L27}})
- [{{I29}} Material Cooling]({{L28}})
- [{{I30}} Setting Overrides]({{L29}})
- [{{I31}} Advanced]({{L30}})
- [{{I32}} Multimaterial]({{L31}})
- [{{I33}} Dependencies]({{L32}})

## Process Settings

{{I121}}  
{{I34}} Settings related to the 3D printing process.

### Quality Settings

{{I122}}  
{{I35}} Settings related to print quality and aesthetics.

- [{{I36}} Layer Height Settings]({{L33}})
- [{{I37}} Line Width Settings]({{L34}})
- [{{I38}} Seam Settings]({{L35}})
- [{{I39}} Precision]({{L36}})
- [{{I40}} Ironing]({{L37}})
- [{{I41}} Z Contouring]({{L38}})
- [{{I42}} Wall generator]({{L39}})
- [{{I43}} Walls and surfaces]({{L40}})
- [{{I44}} Bridging]({{L41}})
- [{{I45}} Overhangs]({{L42}})

### Strength Settings

{{I123}}  
{{I46}} Settings related to print strength and durability.

- [{{I47}} Walls]({{L43}})
- [{{I48}} Top and Bottom Shells]({{L44}})
- [{{I49}} Infill]({{L45}})
    - [{{I50}} Fill Patterns]({{L46}})
        - [Patterns Quick Reference Table Guide]({{L47}})
    - [{{I51}} Template Metalanguage for infill rotation]({{L48}})
- [{{I52}} Advanced]({{L49}})

### Speed Settings

{{I124}}  
{{I53}} Settings related to print speed and movement.

- [{{I54}} Initial Layer Speed]({{L50}})
- [{{I55}} Other Layers Speed]({{L51}})
- [{{I56}} Overhang Speed]({{L52}})
- [{{I57}} Travel Speed]({{L53}})
- [{{I58}} Acceleration]({{L54}})
- [{{I59}} Jerk (XY)]({{L55}})
- [{{I60}} Advanced / Extrusion rate smoothing]({{L56}})

### Support Settings

{{I125}}  
{{I61}} Settings related to support structures and their properties.

- [{{I62}} Support]({{L57}})
- [{{I63}} Raft]({{L58}})
- [{{I64}} Support Filament]({{L59}})
- [{{I65}} Support Ironing]({{L60}})
- [{{I66}} Advanced]({{L61}})
- [{{I67}} Tree Supports]({{L62}})

### Multimaterial Settings

{{I126}}  
{{I68}} Settings related to multimaterial printing.

- [{{I69}} Prime Tower]({{L63}})
- [{{I70}} Filament for Features]({{L64}})
- [{{I71}} Ooze Prevention]({{L65}})
- [{{I72}} Flush Options]({{L66}})
- [{{I73}} Advanced]({{L67}})

### Others Settings

{{I127}}  
{{I74}} Settings related to various other print settings.

- [{{I75}} Skirt]({{L68}})
- [{{I76}} Brim]({{L69}})
- [{{I77}} Special Mode]({{L70}})
- [{{I78}} Fuzzy Skin]({{L71}})
- [{{I79}} G-Code Output]({{L72}})
- [{{I80}} Post Processing Scripts]({{L73}})
- [{{I81}} Notes]({{L74}})

## Design

{{I82}} Parametric CAD inside the slicer: sketch, constrain, build solids and send them to the plate. Experimental, and switched on in [Preferences]({{L75}}).

- [Design Tab]({{L76}})
    - [Sketching]({{L77}})
    - [Modeling Tools]({{L78}})
    - [Design Keyboard Shortcuts]({{L79}})

## Prepare

{{I83}} First steps to prepare your model/s for printing.

- Right-Click Menu
    - [STL Transformation]({{L80}})
        - [Simplify model]({{L81}})
        - [Fix model]({{L82}})
    - [Precise Seam]({{L83}})
    - Work In Progress...
- Toolbar
    - [Basic]({{L84}})
        - [{{I84}} Add Objects]({{L85}})
        - [{{I85}} Add Plate]({{L86}})
        - [{{I86}} Measure Tool]({{L87}})
    - [{{I87}} Auto Orient]({{L88}})
    - [{{I88}} Auto Arrange]({{L89}})
    - [{{I89}} Object Set]({{L90}})
        - [{{I90}} Add/Remove Instances]({{L91}})
        - [{{I91}} Split to Objects]({{L92}})
        - [{{I92}} Split to Parts]({{L93}})
    - [{{I93}} Variable Layer Height]({{L94}})
    - [Object Manipulation]({{L95}})
        - [{{I94}} Move]({{L96}})
        - [{{I95}} Rotate]({{L97}})
        - [{{I96}} Scale]({{L98}})
        - [{{I97}} Lay on Face]({{L99}})
    - [{{I98}} Cutting Tool]({{L100}})
    - [{{I99}} Mesh Boolean]({{L101}})
    - Painting/Marking Tools
        - [{{I100}} Support Painting]({{L102}})
        - [{{I101}} Seam Painting]({{L103}})
        - [{{I102}} Paint-on fuzzy skin]({{L104}})
        - [{{I103}} Color Painting]({{L105}})
        - [Texture Displacement]({{L106}})
            - [UV Editor]({{L107}})
            - [Pro Mode]({{L108}})
        - [Image]({{L109}})
        - [{{I104}} Emboss]({{L110}})
        - [{{I105}} Brim Ears Painting]({{L111}})
    - [Assembly Tools]({{L112}})
        - [{{I106}} Assemble]({{L113}})
        - [{{I107}} Assembly View]({{L114}})

## Calibrations

{{I108}} The [Calibration Guide]({{L115}}) outlines Orca’s key calibration tests and their suggested order of execution.

- [{{I109}} Temperature]({{L116}})
- [{{I110}} Volumetric Speed]({{L117}})
- [{{I111}} Pressure Advance]({{L118}})
- [{{I112}} Flow Ratio]({{L119}})
- [{{I113}} Retraction]({{L120}})
- Advanced:
    - [{{I114}} Cornering (Jerk & Junction Deviation)]({{L121}})
    - [{{I115}} Input Shaping]({{L122}})
        - [VFA]({{L123}})
    - [{{I116}} Adaptive Pressure Advance]({{L124}})
- [{{I117}} Tolerance]({{L125}})

## General Settings

- [Import and Export]({{L126}})
- [Modes]({{L127}})
- [Option Types]({{L128}})
- [Keyboard Shortcuts]({{L129}})
- [Transfer or Discard Changes popup dialog]({{L130}})
- [User Profiles]({{L131}})
- [Troubleshoot Center]({{L132}})

## Command Line Interface

OrcaSlicer can run headless from the command line for automation, batch processing, and CI pipelines.

- [CLI Mode]({{L133}})
- [Actions]({{L134}})
- [Transform]({{L135}})
- [Misc]({{L136}})

## Plugins

- [Getting Started]({{L137}})
- [Local Plugins]({{L138}})
- [Cloud Plugins]({{L139}})
- [Plugin Types]({{L140}})
- [Managing Plugins]({{L141}})

## Speed Dial

- [Speed Dial]({{L142}})

## Publishing 3MF

- [What does Publish 3MF do?]({{L143}})
- [For creators]({{L144}})

## Guides

- How to:
    - [Use mixed with different nozzle sizes]({{L145}})
    - [Calibrate Your Printer]({{L146}})
    - [Print on a Belt Printer]({{L147}})
    - [Print in Parallel on an IDEX/IQEX Printer]({{L148}})
    - [Create Profiles]({{L149}})
    - [Download Pull Requests Artifacts for Testing]({{L150}})

## Release Notes

See the [all releases]({{L151}}) overview, or jump straight to a version:

- [OrcaSlicer V2.5.1]({{L152}})
- [OrcaSlicer V2.5.0]({{L153}})
- [OrcaSlicer V2.5.0 RC]({{L154}})
- [OrcaSlicer V2.5.0 Beta]({{L155}})
- [OrcaSlicer V2.5.0 Alpha]({{L156}})
- [OrcaSlicer V2.4.2]({{L157}})
- [OrcaSlicer V2.4.1]({{L158}})
- [OrcaSlicer V2.4.0]({{L159}})
- [OrcaSlicer V2.4.0 Beta]({{L160}})
- [OrcaSlicer V2.4.0 Alpha]({{L161}})

## Developer Section

{{I118}} This is a documentation from someone exploring the code and is by no means complete or even completely accurate. Please edit the parts you might find inaccurate. This is probably going to be helpful nonetheless.

- [How to contribute]({{L162}})
- [How to build OrcaSlicer]({{L163}})
    - [Windows]({{L164}})
    - [macOS]({{L165}})
    - [Linux]({{L166}})
    - [Compiler caching]({{L167}})
- [How to run tests]({{L168}})
- [How to run the clang-tidy check]({{L169}})
- [Localization and translation guide]({{L170}})
    - [Glossary]({{L171}})
- [How to create profiles]({{L172}})
- [How to contribute to the wiki]({{L173}})
- [Preset, PresetBundle and PresetCollection]({{L174}})
- [Plater, Sidebar, Tab, ComboBox]({{L175}})
- Plugin Development
    - [Plugin System Overview]({{L176}})
    - [Plugin Development]({{L177}})
    - API Reference
        - [Registry]({{L178}})
        - [Host]({{L179}})
        - [Host UI]({{L180}})
        - [Script]({{L181}})
        - [Printer Agent]({{L182}})
        - [Lifecycle Events]({{L183}})
        - [Pages]({{L184}})
        - [Resource Texture]({{L185}})
        - [Slicing Pipeline]({{L186}})
    - [Plugin Audit Hook]({{L187}})
- [Placeholders and Expressions]({{L188}})
- [Slicing Call Hierarchy]({{L189}})
