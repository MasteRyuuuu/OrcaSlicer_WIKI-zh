# Pages

`orca.pages` lets a plugin add its own **tab to the main window**, next to OrcaSlicer's built-in
tabs (Prepare, Preview, Device, ...). The tab hosts an HTML page supplied by the plugin.
Subclass `orca.pages.PagesPluginCapabilityBase`; its `get_type()` returns `Pages`.

| Method | Required | Purpose |
|---|---|---|
| `get_name()` | yes | the tab label |
| `get_ui()` | yes | return the page's HTML as a string |
| `get_icon()` | no | return the path of an `.svg` / `.png` tab icon; empty (the default) for none |
| `on_message(data)` | no | receives each `orca.postMessage(obj)` from the page, decoded from JSON |
| `post_message(data)` | provided | send a JSON-compatible value to the page's `orca.onMessage` handlers |

{{C1}}

## Behavior

- A tab is added when the capability is loaded and enabled, and removed when it is disabled or
  its plugin is unloaded. The page itself is built the first time the tab is shown, so
  `get_ui()` is not called until then.
- The page gets a `window.orca` bridge with `orca.postMessage(obj)` and `orca.onMessage(cb)`
  (there is no `submit()` or `close()`). It is themed like the [Host UI]({{L1}})
  dialogs, and if the user reloads it the plugin's HTML is loaded again, so keep the
  authoritative state in the plugin and have the page ask for it on load.
- `post_message()` before the page has been built is dropped; the pattern above (the page asks
  for its data when it loads) avoids that.
- A link that would open a new window is loaded in the page itself.
- If `get_ui()` raises, the error is logged and the tab stays empty.
- The number of plugin tabs shown side by side is set in **Preferences > General > Plugins >
  Visible plugin pages** (1-10, default 5). Further pages collapse into a dropdown on the last
  plugin tab.

See [Registry]({{L2}}) for registration and the members every capability inherits.
