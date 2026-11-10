# Host UI

`orca.host.ui` lets a plugin show host-owned UI: a native message box, a native progress
dialog, a modal HTML dialog, non-modal interactive windows, a panel docked beside the
3D view, and notifications in the 3D view. To add a whole main-window tab instead, see
[Pages]({{L1}}).

A plugin must never import its own GUI toolkit (PyQt/wxPython/tkinter): a `script` plugin
shares the host's UI thread, so a second toolkit's event loop would clash with wxWidgets, and
a `gcode` / `printer-agent` plugin can run off the main thread where toolkit calls would crash.
These host calls run on the main thread for you and block the calling code until they return.

## Dialogs and Windows

{{C1}}

`message` arguments: `buttons` is `"ok"|"ok_cancel"|"yes_no"|"yes_no_cancel"`; `icon` is
`"info"|"warning"|"error"|"question"`.

## Docked Panels

`create_dock_panel()` puts your page in a pane of the same dock area as the sidebar, instead
of a separate window. The user can drag it to another edge, float it, resize it or close it.
Opened again, it comes back where and how big it was when the window layout was last saved,
which happens when a new project is started, not on exit.

{{C2}}

`dock` is `"left"`, `"right"`, `"bottom"` or `"float"`; `width` and `height` are in DIPs, so
they mean the same size on every display. Floating is unavailable on Wayland, where a panel
asking to float starts docked instead.

The page talks to the plugin exactly as in a window — see [Page Messaging]({{L2}})
and [Theming]({{L3}}) below — except `orca.submit()`, which only applies to modal dialogs.

Panel-specific notes:

- The panel belongs to the **Prepare and Preview tabs**: it is hidden while the user is on
  Device, Project or Calibration, and comes back with the 3D view.
- Open it from `execute()` or `on_load()`; the host closes a plugin's panels when it is
  unloaded, reloaded, the app language is switched or the app exits, the same as its windows.
  `on_close` runs only for a close the user or the page asked for, not for those.
- A `post()` issued immediately after `create_dock_panel()` can be dropped while the page is
  still loading. Have the page ask for its first data instead (`orca.postMessage(...)` on
  load), which also keeps a reopened panel in sync — and a reloaded one: the user can reload
  the page from its context menu, and what comes back is a fresh document with your HTML
  again, so anything the page held in script state is gone. Keep the authoritative state in
  the plugin.
- Running the same capability twice would open a second panel; keep the handle and call
  `show()` on it (or `close()` it first) if you want exactly one.
- Global shortcuts still reach the app while the user types in a panel — Ctrl/Cmd with
  R, G, J, N, O, S, F, P, I, Shift+G, Shift+S or Shift+E. Avoid binding those in your page;
  Ctrl+A/C/V/X/Z are free.

## Plater Notifications

`push_notification()` shows a notification in the 3D view, the same kind OrcaSlicer uses for
its own messages. It does not block waiting for the user.

{{C3}}

`notification_level` is an `orca.host.ui.NotificationLevel`: `RegularNotificationLevel`,
`HintNotificationLevel`, `ProgressBarNotificationLevel`, `PrintInfoNotificationLevel`,
`PrintInfoShortNotificationLevel`, `ImportantNotificationLevel`, `WarningNotificationLevel`,
`SeriousWarningNotificationLevel` or `ErrorNotificationLevel`. The level sets the styling and
how long the notification stays up. An exception raised in `on_click` is logged and leaves the
notification open, and the callback is disabled once the plugin is unloaded.

## Progress Dialogs

Use `create_progress_dialog()` for host-owned native progress. It returns a `ProgressDialog`
handle and also works as a context manager, so `close()` is called on exit. The default style
is `PD_APP_MODAL | PD_AUTO_HIDE`; add `PD_CAN_ABORT` if the user should be able to cancel.
`maximum` defaults to `100` (values `<= 0` are treated as `100`).

For script plugins, put the dialog inside `execute(self)` and update it between chunks of
work. Do not create the dialog and then run one long uninterrupted operation such as a single
`time.sleep(...)` or blocking network call; the dialog only gets useful repaint/cancel
checkpoints when you call `update()` or `pulse()`.

{{C4}}

For indeterminate work, pulse the dialog instead of setting a numeric value:

{{C5}}

Handle methods:

| Python call | Effect |
|---|---|
| `progress.update(value, message="")` | set the determinate progress value; returns `False` if closed/cancelled |
| `progress.pulse(message="")` | advance an indeterminate progress step; returns `False` if closed/cancelled |
| `progress.start_pulse(interval_ms=100, message="")` | start timer-driven pulsing on the UI thread |
| `progress.stop_pulse()` | stop timer-driven pulsing |
| `progress.close()` | close the dialog |
| `progress.is_open()` | return whether the host still has the dialog registered |

Because `start_pulse()` has no return value, use explicit `update()` or `pulse()` calls at
natural cancellation points if the dialog includes `PD_CAN_ABORT`.

The style constants exposed by `orca.host.ui` mirror `wxProgressDialog`: `PD_APP_MODAL`,
`PD_AUTO_HIDE`, `PD_CAN_ABORT`, `PD_CAN_SKIP`, `PD_ELAPSED_TIME`, `PD_ESTIMATED_TIME`, and
`PD_REMAINING_TIME`. `PD_CAN_SKIP` is available for style parity, but the current Python
handle does not expose a separate "skip" state.

## Page Messaging

The page talks back through `window.orca`, which is injected automatically. The page supplies
raw, self-contained HTML/CSS/JS.

| JS call | Effect |
|---|---|
| `orca.postMessage(obj)` | deliver `obj` to the plugin's `on_message(obj)` |
| `orca.onMessage(cb)` | `cb(data)` runs for each `win.post(data)` (and modal pushes) |
| `orca.submit(obj)` | (modal) close and return `obj` from `show_dialog` |
| `orca.close()` | close the dialog / window |

## Theming

The host injects a stylesheet that matches OrcaSlicer's **current theme** (the active
light/dark mode, fonts, background/foreground, accent and border colors) before your page
renders. An unstyled page already looks native: `<body>`, headings, `button`,
`input` / `select` / `textarea`, `table`, links and scrollbars get sensible themed defaults,
and the theme is also exposed as CSS variables so you can match the rest of the UI:

| Variable | Meaning |
|---|---|
| `--orca-bg` | window/background color |
| `--orca-fg` | primary text color |
| `--orca-muted` | secondary / label text color |
| `--orca-accent` | accent color (buttons, links, focus) |
| `--orca-accent-fg` | text color on the accent |
| `--orca-border` | subtle border / separator / row-hover color |
| `--orca-font` | UI font stack |

The injected rules use only low specificity and never `!important`, so **any CSS your page
ships overrides them**. Prefer the variables (for example,
`border:1px solid var(--orca-border)`) over hardcoded colors so your dialog follows light
and dark mode automatically. The UI sample (`host_ui_panel.py`) relies on this and uses no
fixed colors.

## Threading and Lifecycle

- Host UI calls run on the main thread and **block the calling code** until they return
  (`message` / `show_dialog` when the dialog closes; `create_window` /
  `create_progress_dialog` as soon as the window/dialog is shown; progress updates after the
  host applies them). From a `script` plugin, already on the UI thread, they run inline; from
  a background-thread plugin (`gcode` / `printer-agent`) they marshal to the main thread
  first.
- `on_message(data)` runs on the **UI thread**; keep it quick; offload heavy work to a
  `threading.Thread` and push results back with `win.post(...)`.
- A **modal** dialog (`show_dialog`) fits a one-shot `execute()`. A **persistent** panel
  (`create_window`) is best opened from `on_load()` so it lives for the plugin's lifetime;
  the host closes a plugin's windows automatically when it is unloaded/reloaded or the app
  exits.
- Content is loaded as raw HTML; prefer **self-contained** pages (inline CSS/JS). There is no
  CSP and developer tools are disabled.
