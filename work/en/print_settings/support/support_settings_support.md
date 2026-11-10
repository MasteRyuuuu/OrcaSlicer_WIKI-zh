# Support

{{M1}}
Support structures are used in 3D printing to provide stability to overhangs and complex geometries.

{{T1}}

## Type

{{M2}}
There are several support types, each suited for different printing needs:

### Normal

Normal support structures are projected straight down from the overhangs, providing a stable base for overhangs and complex geometries.

### Tree

Tree-like support structures are designed to minimize material usage while still providing adequate support. They branch out from a central trunk, allowing for more efficient printing.

#### Support critical regions only

{{M3}}
Only creates support for critical regions, such as sharp tails and cantilevers. Available only with `Tree (auto)`.

### Auto

Automatically generates support wherever the model's overhangs need it, as well as where support enforcers are placed in the Prepare view.

### Manual

Only generates support where support enforcers are placed in the Prepare view.

## Style

{{M4}}
Style and shape of the support.  
Grid and Snug apply to normal supports, while Organic, Tree Slim, Tree Strong and Tree Hybrid apply to tree supports. `Default (Grid/Organic)` uses Grid for normal supports and Organic for tree supports.

### Grid

Default for normal supports. Projecting the supports into a regular grid creates more stable supports.

### Snug

Snug support towers save material and reduce object scarring.

### Organic

Default style for tree supports. Like Tree Slim, it merges branches more aggressively and saves a lot of material.

### Tree Slim

Slim tree support branches are designed to be more delicate and use less material while still providing adequate support.

### Tree Strong

Strong tree support branches are designed to be more robust and provide additional support for heavier overhangs.

### Tree Hybrid

Creates a structure similar to normal support under large flat overhangs.

## Threshold angle

{{M5}}
Support will be generated for overhangs whose slope angle is below the threshold. The smaller this value is, the steeper the overhang that can be printed without support.  
If set to `0`, normal supports use the [Threshold overlap]({{L1}}) instead, while tree supports use 30°.

## Threshold overlap

{{M6}}
If [Threshold angle]({{L2}}) is zero, support will be generated for overhangs whose overlap with the layer below is below the threshold. A percentage is relative to the outer wall line width.
The smaller this value is, the steeper the overhang that can be printed without support.  
Tree supports don't use this setting, so it is hidden for them.

## Initial layer density

{{M7}}
Density of the first raft or support layer.

## Initial layer expansion

{{M8}}
Expands the first raft or support layer to improve build plate adhesion. It is disabled for the Tree Slim and Tree Strong styles unless a raft is used.

## On build plate only

{{M9}}
Don't create support on the model surface, only on the build plate.

## Ignore small overhangs

{{M10}}
With this setting, small overhangs that possibly don't need support are ignored by support generation.
