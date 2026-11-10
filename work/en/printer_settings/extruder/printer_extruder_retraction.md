# Retraction

Retraction is the process of pulling the filament back into the nozzle to prevent oozing and stringing during non-print moves.  
If the retraction length is too short, it may not effectively prevent oozing, while if it's too long, it can lead to clogs or under-extrusion.  
Filaments like PETG and TPU are more prone to stringing, so they may require longer retraction lengths compared to PLA or ABS. You can override your printer's default retraction settings for each filament in [Material Setting Overrides]({{L1}}).

> [!TIP]
> Check out the [Retraction Test]({{L2}}) to help determine the optimal retraction settings for your filament.

{{T1}}

## Length

{{M1}}
When retraction is triggered before changing tool, filament is pulled back by the specified amount (the length is measured on raw filament, before it enters the extruder).

## Extra length on restart

{{M2}}
When the retraction is compensated after changing tool, the extruder will push this additional amount of filament.

## Retraction speed

{{M3}}
Speed for retracting filament from the nozzle.

## Deretraction speed

{{M4}}
Speed for reloading filament into the nozzle. Zero means same speed of retraction.

## Travel distance threshold

{{M5}}
Only trigger retraction when the travel distance is longer than this threshold.

## Retract on layer change

{{M6}}
This forces a retraction on layer changes.

## Wipe while retracting

{{M7}}
This moves the nozzle along the last extrusion path when retracting to clean any leaked material on the nozzle. This can minimize blobs when printing a new part after traveling.

## Wipe distance

{{M8}}
Describe how long the nozzle will move along the last path when retracting.  
Depending on how long the wipe operation lasts, how fast and long the extruder/filament retraction settings are, a retraction move may be needed to retract the remaining filament.
Setting a value in the retract amount before wipe setting below will perform any excess retraction before the wipe, else it will be performed after.

## Retract amount before wipe

{{M9}}
This is the length of fast retraction before a wipe, relative to retraction length.

## Retract amount after wipe

{{M10}}

This is the length of fast retraction after a wipe, relative to retraction length.  
Together with [Retract amount before wipe]({{L3}}), this lets you split the retraction across the wipe: some before, some after, and the remainder performed during the wipe move itself. The value is clamped by 100% minus the retract amount before wipe, so the two combined never exceed the total retraction length.  
Moving more of the retraction to after the wipe allows shorter wipe distances while keeping seams clean, which is helpful for high-detail models and stringing-prone filaments.

## Retraction When Switching Materials

{{M11}}
Retraction settings specifically for material changes during tool changes in multi-material prints.

### Long retraction when cut (beta)

{{M12}}
Experimental feature: Retracting and cutting off the filament at a longer distance during changes to minimize purge. While this reduces flush significantly, it may also raise the risk of nozzle clogs or other printing problems.
