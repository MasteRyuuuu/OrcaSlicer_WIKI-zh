# Resource Texture

The `orca.resource_texture` module exposes `ResourceTexturePluginCapabilityBase` for plugins that
contribute height-map textures as a resource pack.

| Base class | `get_type()` returns | Required methods | Invoked by |
|---|---|---|---|
| `orca.resource_texture.ResourceTexturePluginCapabilityBase` | `ResourceTexture` | `get_name()`, `get_texture_dir(self) -> str` | OrcaSlicer, when the capability is materialized |

Lifecycle hooks `on_load()` / `on_unload()` are optional and available on every capability
(defaults do nothing).

## Minimal Shape

{{C1}}

`get_name()` is the pack's display name, so it must be unique among the loaded packs of this type
(see [Registry]({{L1}})).

## The texture directory

`get_texture_dir()` returns a directory the host scans for images.

| Rule | Detail |
|---|---|
| Formats | `.png`, `.jpg`, `.jpeg`, `.bmp`, matched case-insensitively |
| Depth | one level, non-recursive; images in a subdirectory are not listed |
| Location | the resolved directory must sit inside the plugin's own folder. A directory outside it is refused, and a symlink inside the pack that resolves outside is skipped |
| File limit | at most 64 images are listed |

`get_texture_dir()` runs once, under the GIL, when the capability is materialized, and the result is
cached. A changed directory takes effect on reload, not while the plugin stays loaded.

A directory that is empty, missing, unreadable, or outside the plugin folder costs the pack its
textures only: the plugin still loads, and the pack is left out. The reason is written to the
session log.

## Packaging

Ship a wheel (`.whl`). An install copies a single entry file, so a `.py` plugin cannot carry sibling
images; a wheel is one file, and the loader extracts it on demand with the images inside the
package's own directory. See [Wheel (`.whl`) plugins]({{L2}}).

## Lifecycle

The host tracks loaded and enabled packs. A pack's textures become available to OrcaSlicer when the
capability loads and is enabled, and are dropped when it is disabled, unloaded, or uninstalled. No
restart is needed. Anything that has already embedded one of a pack's textures keeps it, because it
holds its own copy of the image bytes.

## See Also

- [Registry]({{L3}}) - registration, capability name rules, and `ExecutionResult`.
