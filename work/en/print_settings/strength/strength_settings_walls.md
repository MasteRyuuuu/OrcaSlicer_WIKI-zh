# Walls

In 3D printing, "walls" refer to the outer layers of a printed object that provide its shape and structural integrity.  
Adjusting wall settings can significantly affect layer adhesion, strength, appearance and print time of your model.

{{I2}}

{{T1}}

> [!TIP]
> <strong class="orca-video-title">Recommended</strong>
>
> <span class="orca-video-description">Advanced tips on improving strength.</span>
>
> <div class="orca-video-embed">
>   <a class="orca-video-poster-link" href="{{L4}}" aria-label="Watch advanced strength tips video by Maker's Muse">
>     {{I1}}
>   </a>
> </div>
>
> <span class="orca-video-credit">Video by <strong>Maker's Muse</strong>, with consent.</span>

## Wall loops

{{M1}}
"Wall loops" is the number of walls printed on each layer.  
Increasing the wall loops will:

- Enhance:
    - Layer adhesion
    - Strength
    - Rigidity
- Reduce infill ghosting
- Increase print time

## Alternate extra wall

{{M2}}
This setting adds an extra wall to every other layer. This way the infill gets wedged vertically between the walls, resulting in stronger prints.  
This option doesn't work well when Ensure vertical shell thickness is set to **All**; when both are enabled, OrcaSlicer offers to change it to **Moderate**.  

> [!WARNING]
> It's not recommended to use this option with:
>
> - [Lightning infill]({{L1}}) as there is limited infill to anchor the extra perimeters to.
> - **[Ensure vertical shell thickness: All]({{L2}})**

## Detect thin wall

{{M3}}
By default, walls are printed as closed loops. When a wall is too thin to contain two line widths, enabling "Detect thin walls" prints it as a single extrusion line.  
Thin walls printed this way may have reduced surface quality and strength because they are not closed loops.

> [!TIP]
> It is usually recommended to use the [Arachne wall generator]({{L3}}), which disables "Detect thin walls" because it uses a different approach to wall generation.

- In small details, it can generate features that wouldn't be possible with traditional wall generation methods.  
  {{I3}}
  {{I4}}
- In large prints, it can generate defects more easily due to the reduced wall thickness.
  {{I5}}
