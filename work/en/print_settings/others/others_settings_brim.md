# Brim

Brim is a flat layer printed around a model's base to improve adhesion to the print bed. It is useful for models with small footprints or those prone to warping.

{{I1}}

{{T1}}

## Type

{{M1}}
Controls how the brim is generated on a model's outer and/or inner sides.

### Auto

The Auto brim feature computes an optimal brim width by evaluating material properties, part geometry, printing speed, and thermal characteristics.

- Model geometry
    - Uses the model's height and the shape of its first layer.
    - Height-to-area ratio: computed from the model's height and the second moment of area of its first layer.
- Printing speed
    - Higher maximum printing speeds generally increase the recommended brim width.
- Thermal length
    - Defined as the diagonal of the model's base.
    - Reference thermal lengths (material-specific):
        - ABS, PA-CF, PET-CF: 100
        - PC: 40
        - TPU: 1000
- Material adhesion coefficient
    - Default: 1
    - PETG/PCTG: 2
    - TPU: 0.5

The computed brim width is capped at 18 mm and at 1.5× the thermal length. If the final width is under 5 mm and also less than 1.5× the thermal length, no brim will be generated (width = 0).

### Painted

Generates a brim only on areas that [have been painted in the Prepare tab]({{L1}}).

### Outer

Creates a brim around the model's outer perimeter.  
Easier to remove than an inner brim, but may affect the model's appearance if not removed cleanly.

{{I2}}

### Inner

Creates a brim around inner perimeters.  
It is more difficult to remove and less effective than an outer brim, and it may obscure fine inner details, but it can hide the brim removal seam.

{{I3}}

### Outer and Inner

Creates a brim around both the outer and inner perimeters of the model.  
This approach combines the **disadvantages** of both brim types: it is more difficult to remove and may obscure fine details, but it improves overall adhesion.

{{I4}}

> [!TIP]
> Consider using a [raft]({{L2}}) on complex models/materials.

### Mouse Ears

Mouse ears are small, local brim extensions (typically placed near corners and sharp features) that improve bed adhesion and reduce warping while using less material than a full brim.  
The geometry analysis routine selects candidate locations based on the configured angle threshold and detection radius.

{{I5}}

#### Ear max angle

{{M2}}
Angle threshold (degrees) used to decide where mouse ears may be placed:

- 0° — disabled; no mouse ears are generated.
- Between 0° and 180° — ears are created at features with local angles sharper (smaller) than the threshold.
- 180° — ears are allowed on almost any non-straight feature.

#### Ear detection radius

{{M3}}
The geometry is decimated before sharp angles are detected.  
This parameter sets the minimum deviation length used for the decimation.  
Set to 0 to disable.

### No-brim

No brim is printed around the model. The brims of neighboring objects are still kept one brim line away from it, so they don't touch it.  
Useful as a per-object setting to skip the brim on parts that don't need one. The other brim settings are disabled while it is selected.

### Leading edge only

Available only on [belt printers]({{L3}}). Generates a brim at and ahead of the object's first contact with the belt, without extending along the rest of the object.

Use it with [Leading length]({{L4}}) to anchor the leading edge without printing a brim along the entire part. The extension gives the brim material more time to adhere to the belt before the object begins printing. On printers without a belt, this type is printed as an [Outer]({{L5}}) brim.

## Brim ears outer only

{{M4}}

When enabled, brim ears are generated only on the model's outer contour. Ears that would otherwise be placed in holes or other enclosed sections are excluded.

This setting is available for both the **Mouse Ears** and **Painted** brim types. In Mouse Ears mode, it filters automatically detected ears. In Painted mode, it filters painted ears when the model is sliced.

## Width

{{M5}}
Distance between the model and the outermost brim line.  
Increasing this value widens the brim, which can improve adhesion but increases material usage.

On a [belt printer]({{L6}}), the width is measured on the belt surface and applies to every brim type.

When **Brim type** is set to **Mouse ear**, this setting is labeled **Brim ear radius**. Its value sets the radius of each automatically generated ear. When **Brim type** is set to **Painted**, the size of brim ears is controlled in the [Brim ears Painting tool]({{L7}}).

## Leading length

{{M6}}

Available only on belt printers. Extends the brim along the belt ahead of every leading edge of the object's contact area. This includes the object's first contact with the belt and any separate island that contacts the belt later in the print.

This extension, called an apron, is printed before the object's leading edge, providing an anchor already attached to the belt.

The length is measured on the belt surface and is added to the [Width]({{L8}}): the brim extends `Brim-object gap + Leading length + Width` ahead of the object. Set the [Brim-Object Gap]({{L9}}) to 0 so the apron touches the edge it anchors.

> [!NOTE]
> On a tilted belt, each layer contributes one strip of the brim. The resulting sheet's thickness is determined by flow rather than layer height. Use the [Brim Flow Ratio]({{L10}}) to adjust this thickness.

> [!WARNING]
> [Auto arrange]({{L11}}) does not reserve space for the leading brim. Leave enough room between objects along the belt for this extension.

Set to 0 to disable.

## Extra width

{{M7}}

Available only on belt printers. Widens the brim across the belt without extending it farther ahead of or behind the object. Use it when a part needs more adhesion along its length than the [Width]({{L12}}) setting alone provides.

The value is measured on the belt surface and is added to the [Width]({{L13}}): the brim extends `Brim-object gap + Width + Extra width` to each side of the object. To extend the brim ahead of the object instead, use [Leading length]({{L14}}).

Set to 0 to disable.

## Brim-Object Gap

{{M8}}
Gap between the innermost brim line and the object.  
Increasing the gap makes the brim easier to remove but reduces its adhesion benefit; very large gaps may eliminate contact and negate the brim's purpose.

### Brim Flow Ratio

{{M9}}
This factor affects the amount of material for [brims]({{L15}}).
Setting this value slightly above 1.0 can help the brim hold the print on the plate, but it can also make brims harder to remove.
The actual brim [flow]({{L16}}) used is calculated by multiplying this value by the [filament flow ratio]({{L17}}), and if set, the object's flow ratio.

> [!NOTE]
> The resulting value will not be affected by the [first-layer flow ratio]({{L18}}).

### Brim use EFC outline

{{M10}}
When enabled, the brim is aligned with the first-layer perimeter geometry after [Elephant Foot Compensation]({{L19}}) is applied.  
This option is intended for cases where [Elephant Foot Compensation]({{L20}}) significantly alters the first-layer footprint.

If your current setup already works well, enabling it may be unnecessary and can cause the brim to fuse with upper layers.

{{I6}}

## Combine brims

{{M11}}
Combine adjacent brims into a single continuous brim when they touch.

- Disable: Each object's brim is generated and printed separately; each brim is completed before its object is printed.
- Enable: Brims that touch are merged and printed together as longer continuous loops, which can improve adhesion for small or closely spaced objects.

### Combined

{{I7}}

### Uncombined

{{I8}}

## Brim on belt printers

On a [belt printer]({{L21}}), an object touches the belt along a narrow strip in each layer, so the entire brim cannot be printed in the first layer. Instead, the brim is printed on the tilted belt surface one strip at a time, across all layers that reach the belt.

This changes how the settings on this page behave:

- [Outer]({{L22}}), [Inner]({{L23}}), [Outer and Inner]({{L24}}) and [Leading edge only]({{L25}}) work as described.
- [Auto]({{L26}}), [Mouse Ears]({{L27}}) and [Painted]({{L28}}) are printed as an Outer brim using the [Width]({{L29}}) setting.
- [Leading length]({{L30}}) and [Extra width]({{L31}}) become available.
- [Brim use EFC outline]({{L32}}) and [Combine brims]({{L33}}) are disabled because both apply only to a flat first layer.
- A brim cannot be combined with [Spiral vase]({{L34}}).

A brim is only generated when the [belt tilt]({{L35}}) is between 1° and 85°.
