# Ooze prevention

{{M1}}
This option will drop the temperature of the inactive extruders to prevent oozing.

## Temperature variation

{{M2}}
Temperature difference to be applied when an extruder is not active. The value is not used when [Idle temperature]({{L1}}) in the filament settings is set to a non-zero value.

## Preheat time

{{M3}}
To reduce the waiting time after tool change, Orca can preheat the next tool while the current tool is still in use. This setting specifies the time in seconds to preheat the next tool. Orca will insert an M104 command to preheat the tool in advance.

## Preheat steps

{{M4}}
Inserts multiple preheat commands (e.g. M104.1). Only useful for the Prusa XL. For other printers, set it to 1.
