# Getting Started

Plugins add extra features to OrcaSlicer. They are managed from the Plugins window.

- [Local Plugins]({{L1}})
- [Cloud Plugins]({{L2}})
- [Plugin Types]({{L3}})
- [Managing Plugins]({{L4}})

## Open the Plugins Window

1. Open the main menu.
2. Click **Plugins**.

{{I1}}

The Plugins window shows installed and available plugins. The upper table lists plugins, and the lower section shows details for the selected plugin.

The details section includes these tabs:

- **Plugin Info** — source, author, version, capabilities, and status.
- **Description** — information supplied by the plugin author.
- **Config** — configuration for the selected plugin's capabilities.
- **Changelog** — available version history.
- **Diagnostics** — loading and error information.

Every capability has a configuration. OrcaSlicer provides a JSON editor by default; a plugin can
provide a custom configuration page instead. See [Plugin configuration]({{L5}})
for the plugin-author API.

{{I2}}

Use the split **Browse plugins** button to choose how you want to add plugins:

- **Browse plugins** opens the cloud plugin browser.
- **Install local plugin** installs a plugin file from your computer.

{{I3}}

> [!NOTE]
> Only install plugins from sources you trust. Plugins can interact with your files and print workflow.
