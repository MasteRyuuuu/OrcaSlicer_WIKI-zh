# Tree Support

This section contains specific settings for tree support structures.

[Tip Diameter]({{L1}}), [Branch Density]({{L2}}), [Branch Diameter Angle]({{L3}}) and [Preferred Branch Angle]({{L4}}) apply only to the [Organic]({{L5}}) style. [Branch Distance]({{L6}}), [Branch Diameter]({{L7}}) and [Branch Angle]({{L8}}) have separate values for the Organic style and for the Tree Slim, Tree Strong and Tree Hybrid styles. [Auto brim width]({{L9}}) and [Tree support brim width]({{L10}}) apply only to the Tree Slim, Tree Strong and Tree Hybrid styles.

## Tip Diameter

{{M1}}
Branch tip diameter for organic supports.

## Branch Distance

{{M2}}
This setting determines the distance between neighboring tree support nodes.

## Branch Density

{{M3}}
Adjusts the density of the support structure used to generate the tips of the branches. A higher value results in better overhangs, but the supports are harder to remove. It is therefore recommended to enable top support interfaces instead of using a high branch density value if dense interfaces are needed.

## Branch Diameter

{{M4}}
This setting determines the initial diameter of support nodes.

## Branch Diameter Angle

{{M5}}
The angle of the branches' diameter as they gradually become thicker towards the bottom. An angle of 0 will cause the branches to have uniform thickness over their length. A bit of an angle can increase the stability of the organic support.

## Branch Angle

{{M6}}
This setting determines the maximum overhang angle that the branches of tree support are allowed to make. If the angle is increased, the branches can be printed more horizontally, allowing them to reach farther.

### Preferred Branch Angle

{{M7}}
The preferred angle of the branches, when they do not have to avoid the model. Use a lower angle to make them more vertical and more stable. Use a higher angle for branches to merge faster.

## Auto brim width

{{M8}}
On the first layer, each branch is widened by a brim that helps it stick to the build plate. When this is enabled, the brim width is calculated per branch as half the branch height divided by its radius at the plate, so tall, thin branches get a wider brim: a 40 mm tall branch with a 2 mm radius gets a 10 mm brim. It is never less than 2 mm, and is otherwise capped so that a branch and its brim stay within 12 mm of the branch center.

The brim is only added when there is no raft. With the Tree Hybrid style, it is added to the branches only; the parts printed as normal support use [Initial layer expansion]({{L11}}) instead.

### Tree support brim width

{{M9}}
The brim width used when [Auto brim width]({{L12}}) is disabled: the distance from the edge of each branch to the outer edge of its brim. `0` disables the brim.
