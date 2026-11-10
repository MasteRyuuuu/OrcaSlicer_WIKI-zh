# Adaptive Bed Mesh

OrcaSlicer introduces comprehensive support for adaptive bed meshing across a variety of firmware, including Marlin, Klipper, and RepRapFirmware (RRF).  
This feature allows users to seamlessly integrate adaptive bed mesh commands within the Machine Start G-code.  
The implementation is designed to be straightforward, requiring no additional plugins or alterations to firmware settings, thereby enhancing user experience and print quality directly from OrcaSlicer.  
{{I1}}

{{T1}}

## Bed mesh

{{M1}}
This option sets the min and max point for the allowed bed mesh area. Due to the probe's XY offset, most printers are unable to probe the entire bed. To ensure the probe point does not go outside the bed area, the minimum and maximum points of the bed mesh should be set appropriately.  
OrcaSlicer ensures that adaptive_bed_mesh_min/adaptive_bed_mesh_max values do not exceed these min/max points. This information can usually be obtained from your printer manufacturer.  
The default setting is (-99999, -99999), which means there are no limits, thus allowing probing across the entire bed.

## Probe point distance

{{M2}}
This option sets the preferred distance between probe points (grid size) for the X and Y directions, with the default being 50mm for both X and Y.

## Mesh margin

{{M3}}
This option determines the additional distance by which the adaptive bed mesh area should be expanded in the XY directions.

> [!NOTE]
> Klipper users: OrcaSlicer will adjust adaptive bed mesh area according to the margin. It is recommended to set the margin to 0 in Klipper config or pass 0 when calling BED_MESH_CALIBRATE command(please refer to the example below).

## Available g-code variables for Adaptive Bed Mesh Command

`bed_mesh_probe_count`: Represents the probe count in the X and Y directions. This value is calculated based on the size of the adaptive bed mesh area and the distance between probe points.

`adaptive_bed_mesh_min`: Specifies the minimum coordinates of the adaptive bed mesh area, defining the starting point of the mesh.

`adaptive_bed_mesh_max`: Determines the maximum coordinates of the adaptive bed mesh area, indicating the endpoint of the mesh.

`ALGORITHM`: Identifies the algorithm used for adaptive bed mesh interpolation. This variable is useful for Klipper users. If bed_mesh_probe_count is less than 4, the algorithm is set to `lagrange`. Otherwise, it is set to `bicubic`.

## Example of Adaptive Bed Mesh usage in OrcaSlicer

### Marlin

{{C1}}

### Klipper

{{C2}}

### RRF

{{C3}}

{{I2}}
