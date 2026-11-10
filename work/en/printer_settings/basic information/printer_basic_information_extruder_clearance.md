# Extruder Clearance

Extruder clearance settings define the minimum distances required around the extruder to avoid collisions with the print bed, rods, or lid during printing. These settings are particularly important for printers with complex geometries or when using by-object printing modes.

## Radius

{{M1}}
Clearance radius around extruder: used for collision avoidance in by-object printing.

## Distance to rod

{{M2}}

Horizontal distance from the nozzle tip to the rod's farther edge. Besides by-object printing, it sizes the keep-out band the gantry rod sweeps around a prime tower printed with [no sparse layers]({{L1}}).

## Height to rod

{{M3}}
Distance from the nozzle tip to the lower rod. Used for collision avoidance in by-object printing.

## Height to lid

{{M4}}
Distance from the nozzle tip to the lid. Used for collision avoidance in by-object printing.
