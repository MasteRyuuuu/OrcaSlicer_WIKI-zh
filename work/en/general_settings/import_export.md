# Import and Export

OrcaSlicer offers various export options to import and export 3D models, projects and configurations.

{{T1}}

## Model

Models are the basic objects that you work with in OrcaSlicer. They represent the basic feature that you want to slice and print.

### Import Model

You can import 3D models from [different file formats]({{L1}}) into OrcaSlicer using one of the following methods:

- **File Menu:** Go to `File` > `Import` and select the desired 3D model file.
- **[Prepare Toolbar Add Button]({{L2}}):** Click on the `Add` button in the toolbar to open the file dialog and select your 3D model file.
- **Drag and Drop:** Simply drag and drop the 3D model file into the OrcaSlicer window.

### Export Model

Use the `Export Model` (under `File` > `Export` > `...`) option to export 3D models or assemblies in various file formats. This is useful for sharing specific models or assemblies without including the entire project.

The available export formats are:

- **[STL]({{L3}}):** Export the current model as an STL file.
- **[DRC]({{L4}}):** Export the current model as a Draco-compressed file.
- **[Generic 3MF]({{L5}}):** Export the current model as a generic 3MF file without printer, material, or process information.

## Project

Projects are a convenient way to save and manage your work in OrcaSlicer, allowing you to keep in a single file all the objects, print settings, and configurations related to a specific project.

### Import Project

Use the `Import Project` (under `File` > `Open Project...`) option to open a previously saved project file. This will load all the objects, print settings, and configurations associated with that project, allowing you to continue working on it or review its details.

### Export Project

Use the `Export Project` (under `File` > `Save Project...`) option to save your entire project, including all objects, print settings, and configurations, into a single file that can be easily shared or backed up.

This is very useful for saving your work in progress or sharing your project with others while preserving all the details and settings.

## Sliced

After slicing a model, you can export the sliced result for printing.

### Export Sliced

- **G-code:** Export the sliced model as a G-code file that can be directly sent to a 3D printer for printing.
- **Gcode.3MF:** Export the sliced model as a Gcode.3MF file that includes the resulting G-code file along with printer, material, and process information. This is useful for sharing the sliced model with all the necessary information for printing.
- **Toolpaths as OBJ:** Export the sliced model 3D preview as an OBJ file.

{{I1}}

### Export Statistics

With **Export statistics with G-code** enabled in the Preferences (`Developer` > `Settings`), exporting a G-code file also writes `<name>.statistics.json` next to it, and an exported sliced 3MF file holds them inside, as `Metadata/plate_N.statistics.json` next to each plate's G-code. The CLI writes the same files with [`--export-statistics`]({{L6}}).

The file holds the estimates the preview shows, for scripts and spreadsheets that compare prints or settings. Times are in seconds, in the normal time mode, lengths in mm, volumes in mm³ and weights in g, as its `units` say.

`version` goes up only when a key is removed, renamed or changes meaning. New keys can appear without it, so a script should check `version` and ignore the keys it doesn't know.

- `summary`: the whole plate.
    - `time`: the estimated print time, and `prepare_time` the part of it the start G-code takes.
    - `travel_time` and `travel_distance`.
    - `layer_count`.
    - `volume`, `weight` and `filament_cost` of all the filament the plate uses, the flush included, as in the preview's filament table. The cost of the print time is not included.
    - `filament_changes`.
    - `filaments`: one entry per filament used, with its `id` (from 1), `length`, `volume`, `weight` and `cost`, and the `volume` and `weight` it uses for the `model`, `support`, `prime_tower` and `flush`.
    - `features`: the `time`, `volume` and `weight` of each feature, by its name in the preview's legend, such as `Outer wall`, `Sparse infill`, or `Custom` for the start and end G-code. Features and layers count only what is extruded, so they leave the flush out.
- `layers`: one entry per layer, from the first: its `z`, the `time` of all its moves, its `travel_time`, `volume` and `weight`, and its `features` as in the summary. The first layer also holds the start G-code, and the last one the end G-code.
- `objects`: one entry per object instance, with its `name`, its `instance` number among the object's copies (from 0), and the `volume` and `weight` of its extrusions and of its supports (`support_volume`, `support_weight`). The skirt, brim, prime tower and custom G-code belong to no object.

An example, with its layers and features cut short:

{{C1}}

### Import Sliced

OrcaSlicer also allows you to import sliced files in G-code. This can help you visualize the toolpaths of a G-code file, which can be useful for analyzing the slicing results or for comparing different slicing configurations.

> [!TIP]
> G-code files will only contain the toolpaths and will not include any printer, material, or process information.  
> If you want to import a sliced file with all the necessary information for printing, it's recommended to use the Gcode.3MF format.

## Presets

Presets are a convenient way to save and manage specific settings and configurations in OrcaSlicer, allowing you to easily apply them to different models or projects.

### Export Preset Bundle

This tool allows you to export a bundle of presets that you can use to share specific settings and configurations with others or to back up your presets for future use.

- **Printer config bundle:** Export Printer and all the filament and process presets that belongs to the printer in a `.orca_printer` format.
- **Filament bundle:** Export user's filamnets presets set in a `.orca_filaments` format.
- **Printer presets:** Export user's printer presets set in a `.zip` file.
- **Filament presets:** Export user's filament presets set in a `.zip` file.
- **Process presets:** Export user's process presets set in a `.zip` file.

### Import Preset Bundle

To import a preset bundle, use the `Import Configs` (under `File` > `Import` > `Preset Configs`) option and select the desired preset bundle file. This will import the presets contained in the bundle and make them available for use in your projects.

## Supported File Formats

OrcaSlicer supports the following 3D model file formats for import:

### STL

[STL]({{L7}}) is a widely used file format for 3D printing that represents the surface geometry of a 3D object using triangular facets.

> [!NOTE]
> This is the basic file format used for the slicing process in OrcaSlicer. Any other supported file formats (e.g., STEP, 3MF, OBJ) are converted to STL during the import process.

It's main advantage is its simplicity and wide compatibility with various 3D modeling software and slicers.   However, STL files can have limitations in terms of mesh quality and may not capture intricate details accurately.  
If the original model was designed in a Mesh-based software, such as Blender or ZBrush, the STL file will likely be a good representation of the original design.  
However, if the original model was created in a CAD software, such as SolidWorks or Fusion 360, the STL file may not capture all the details and features of the original design accurately and will depend on the CAD's export settings.

### 3MF

3MF is a modern file format designed for 3D printing that provides a more efficient and comprehensive way to represent 3D models, including support for colors, materials, and multiple objects within a single file.

Some 3MF files may contain Printer, Material, and Process information that can be used to automatically configure print settings in OrcaSlicer.  
When importing a 3MF file, OrcaSlicer will attempt to extract this information and apply it to the imported model.  
If the 3MF information is not compatible with OrcaSlicer, it will be ignored and the model will be imported with default settings.

> [!TIP]
> You can open 3MF files as a ZIP archive to inspect the included information and files.

### STEP

[STEP]({{L8}}) is a comprehensive file format that represents 3D models using a more detailed and accurate representation of the original design. It is commonly used in engineering and manufacturing applications.

#### Importing STEP files

This setting determines how STEP files are converted into STL files and is displayed during the STEP file import process.

{{I2}}

##### Parameters

The transformation uses [Linear Deflection and Angular Deflection]({{L9}}) parameters to control the mesh quality.
A finer mesh will result in a more accurate representation of the original surface, but it will also increase the file size and processing time.

{{I3}}

- **Linear Deflection:** Specifies the maximum distance allowed between the original surface and its polygonal approximation. Lower values produce a mesh that more accurately follows the original curvature.
- **Angular Deflection:** Defines the maximum allowable angle difference between the actual surface and its tessellated counterpart. Smaller angular deflection values yield a more precise mesh.

##### Split compound and compsolid into multiple objects

Enabling this option will split the imported 3D file into separate [parts of the same object]({{L10}}). This is especially useful for adjusting individual part positions, tweaking print settings, or optimizing the model through simplification while maintaining the original design [assembly]({{L11}}).

Each solid becomes a part, and so does each shell outside a solid, as found in surface models. Faces that belong to no shell stay together as one part.

{{I4}}

##### Don't show again

This option will hide the STL transformation dialog when opening a STEP file.
To restore the dialog, go to "Preferences" (Ctrl + P) > "Show the STEP mesh parameter setting dialog".

{{I5}}

### DRC

[Draco (DRC)]({{L12}}) is a compression library developed by Google that is designed to compress and decompress 3D geometric meshes.  
Its main advantage is its ability to significantly reduce the file size of 3D models while maintaining a high level of visual fidelity.

#### Draco Compression

Draco uses several compression techniques to achieve high compression ratios, like file compression (used at maximum level in OrcaSlicer), duplicated vertex removal, and Quantization Bits.

##### Draco Quantization Bits

This technique reduces the precision of the vertex attributes (such as position, normal, and texture coordinates) to further decrease the file size.  
By default, OrcaSlicer disables quantization by setting the quantization bits to 0, which means that the original precision of the vertex attributes is preserved. This will create a almost Lossless compression (~15% of the original size) but it can be adjusted to achieve a smaller file size at the cost of some loss in visual fidelity.

Using a quantization bit value of 25 will result in a even smaller file size (around 5% of the original size) while still maintaining a good level of visual fidelity and dimensional accuracy for most models.
Using a quantization bit value of 16 or lower may result in a significant loss of visual fidelity, especially for models with fine details. For some artistic models where precision is not important, lower values can be used to achieve a very small file size (around 1% of the original size).

### OBJ

Similar to STL, OBJ is a widely used file format for 3D models that represents the geometry of a 3D object using vertices, edges, and faces. It also supports texture mapping and material properties.

### AMF

AMF (Additive Manufacturing File Format) is an XML-based file format designed for 3D printing that provides a more flexible and comprehensive way to represent 3D models, including support for colors, materials, and multiple objects within a single file.

### SVG

SVG (Scalable Vector Graphics) is a file format used for 2D vector graphics. It can be imported into OrcaSlicer to create 3D models by extruding the 2D shapes defined in the SVG file.

### ZIP

OrcaSlicer also supports importing ZIP files that contain one of the supported 3D model file formats (e.g., STL, 3MF, OBJ). When you import a ZIP file, OrcaSlicer will extract the contents and look for supported 3D model files to import.
