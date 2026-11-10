# 宿主 UI

`orca.host.ui` 让插件可以显示由宿主管理的界面：原生消息框、原生进度对话框、模态 HTML 对话框、非模态交互窗口、停靠在 3D 视图旁的面板，以及 3D 视图中的通知。如果要添加一整个主窗口选项卡，请参见[页面]({{L1}})。

插件绝不能导入自己的 GUI 工具包（PyQt/wxPython/tkinter）：`script` 插件与宿主共用 UI 线程，第二个工具包的事件循环会与 wxWidgets 冲突；而 `gcode` / `printer-agent` 插件可能在非主线程上运行，在那里调用工具包会导致崩溃。这些宿主调用会替你在主线程上运行，并阻塞调用代码直到返回。

## 对话框和窗口

{{C1}}

`message` 的参数：`buttons` 为 `"ok"|"ok_cancel"|"yes_no"|"yes_no_cancel"`；`icon` 为 `"info"|"warning"|"error"|"question"`。

## 停靠面板

`create_dock_panel()` 把你的页面放进与侧边栏同一停靠区域中的一个窗格里，而不是单独的窗口。用户可以把它拖到另一侧边缘、让它浮动、调整大小或关闭它。再次打开时，它会回到上次保存窗口布局时的位置和大小——布局在新建项目时保存，而不是在退出时保存。

{{C2}}

`dock` 为 `"left"`、`"right"`、`"bottom"` 或 `"float"`；`width` 和 `height` 以 DIP 为单位，所以在每种显示器上代表相同的尺寸。在 Wayland 上无法浮动，要求浮动的面板会改为以停靠状态启动。

页面与插件通信的方式与窗口完全相同——参见下文的[页面消息]({{L2}})和[主题]({{L3}})——只有 `orca.submit()` 例外，它只适用于模态对话框。

面板特有的注意事项：

- 面板属于**"准备"和"预览"选项卡**：用户切换到设备、项目或校准时它会隐藏，回到 3D 视图时重新出现。
- 在 `execute()` 或 `on_load()` 中打开它；插件被卸载、重新加载、切换应用语言或应用退出时，宿主会关闭插件的面板，与窗口相同。只有在用户或页面主动要求关闭时才会运行 `on_close`，上述情况不会。
- 在 `create_dock_panel()` 之后立即发出的 `post()`，可能会在页面仍在加载时被丢弃。请让页面主动索取它的初始数据（在加载时调用 `orca.postMessage(...)`），这样重新打开的面板也能保持同步——重新加载的面板也是如此：用户可以从右键菜单重新加载页面，回来的是一个重新载入你的 HTML 的全新文档，页面在脚本状态中保存的任何内容都会丢失。请把权威状态保存在插件中。
- 再次运行同一功能会打开第二个面板；如果只想要一个，请保存句柄并对它调用 `show()`（或者先 `close()` 它）。
- 用户在面板中输入时，全局快捷键仍然会被应用接收——Ctrl/Cmd 加 R、G、J、N、O、S、F、P、I、Shift+G、Shift+S 或 Shift+E。请避免在页面中绑定这些组合；Ctrl+A/C/V/X/Z 则可以自由使用。

## 盘面通知

`push_notification()` 在 3D 视图中显示一条通知，与 OrcaSlicer 自身消息所用的通知是同一类。它不会阻塞等待用户。

{{C3}}

`notification_level` 是一个 `orca.host.ui.NotificationLevel`：`RegularNotificationLevel`、`HintNotificationLevel`、`ProgressBarNotificationLevel`、`PrintInfoNotificationLevel`、`PrintInfoShortNotificationLevel`、`ImportantNotificationLevel`、`WarningNotificationLevel`、`SeriousWarningNotificationLevel` 或 `ErrorNotificationLevel`。级别决定通知的样式以及显示多长时间。`on_click` 中抛出的异常会被记录到日志，通知保持打开；插件被卸载后，回调会被禁用。

## 进度对话框

使用 `create_progress_dialog()` 显示由宿主管理的原生进度对话框。它返回一个 `ProgressDialog` 句柄，也可以作为上下文管理器使用，退出时会自动调用 `close()`。默认样式为 `PD_APP_MODAL | PD_AUTO_HIDE`；如果允许用户取消，请加上 `PD_CAN_ABORT`。`maximum` 默认为 `100`（`<= 0` 的值按 `100` 处理）。

对于脚本插件，请把对话框放在 `execute(self)` 内部，并在各段工作之间更新它。不要先创建对话框，然后执行一个长时间不间断的操作，例如单次 `time.sleep(...)` 或阻塞的网络调用；只有在你调用 `update()` 或 `pulse()` 时，对话框才有机会重绘和检查是否取消。

{{C4}}

对于无法确定进度的工作，请让对话框脉动，而不是设置数值：

{{C5}}

句柄方法：

| Python 调用 | 效果 |
|---|---|
| `progress.update(value, message="")` | 设置确定的进度值；如果已关闭/取消则返回 `False` |
| `progress.pulse(message="")` | 推进一步不确定进度；如果已关闭/取消则返回 `False` |
| `progress.start_pulse(interval_ms=100, message="")` | 在 UI 线程上启动由定时器驱动的脉动 |
| `progress.stop_pulse()` | 停止由定时器驱动的脉动 |
| `progress.close()` | 关闭对话框 |
| `progress.is_open()` | 返回宿主是否仍登记着该对话框 |

由于 `start_pulse()` 没有返回值，如果对话框包含 `PD_CAN_ABORT`，请在适合取消的位置显式调用 `update()` 或 `pulse()`。

`orca.host.ui` 提供的样式常量与 `wxProgressDialog` 对应：`PD_APP_MODAL`、`PD_AUTO_HIDE`、`PD_CAN_ABORT`、`PD_CAN_SKIP`、`PD_ELAPSED_TIME`、`PD_ESTIMATED_TIME` 和 `PD_REMAINING_TIME`。`PD_CAN_SKIP` 是为了保持样式一致而提供的，但当前的 Python 句柄并不提供单独的"跳过"状态。

## 页面消息

页面通过自动注入的 `window.orca` 回传消息。页面提供原始的、自包含的 HTML/CSS/JS。

| JS 调用 | 效果 |
|---|---|
| `orca.postMessage(obj)` | 把 `obj` 传给插件的 `on_message(obj)` |
| `orca.onMessage(cb)` | 每次 `win.post(data)`（以及模态推送）时运行 `cb(data)` |
| `orca.submit(obj)` | （模态）关闭并从 `show_dialog` 返回 `obj` |
| `orca.close()` | 关闭对话框 / 窗口 |

## 主题

宿主会在你的页面渲染之前注入一份与 OrcaSlicer **当前主题**（当前的浅色/深色模式、字体、背景/前景色、强调色和边框颜色）相匹配的样式表。即使不写任何样式，页面看起来也已经很原生：`<body>`、标题、`button`、`input` / `select` / `textarea`、`table`、链接和滚动条都有合理的主题化默认样式；主题还以 CSS 变量的形式提供，方便你与界面的其他部分保持一致：

| 变量 | 含义 |
|---|---|
| `--orca-bg` | 窗口/背景颜色 |
| `--orca-fg` | 主要文字颜色 |
| `--orca-muted` | 次要 / 标签文字颜色 |
| `--orca-accent` | 强调色（按钮、链接、焦点） |
| `--orca-accent-fg` | 强调色上的文字颜色 |
| `--orca-border` | 细边框 / 分隔线 / 行悬停颜色 |
| `--orca-font` | 界面字体栈 |

注入的规则只使用低优先级的选择器，从不使用 `!important`，所以**页面自带的任何 CSS 都会覆盖它们**。请优先使用这些变量（例如 `border:1px solid var(--orca-border)`），而不是写死颜色，这样对话框就能自动适配浅色和深色模式。UI 示例（`host_ui_panel.py`）就依赖于此，没有使用任何固定颜色。

## 线程与生命周期

- 宿主 UI 调用在主线程上运行，并**阻塞调用代码**直到返回（`message` / `show_dialog` 在对话框关闭时返回；`create_window` / `create_progress_dialog` 在窗口/对话框显示出来后立即返回；进度更新在宿主应用之后返回）。在本来就在 UI 线程上的 `script` 插件中，它们直接内联运行；在后台线程插件（`gcode` / `printer-agent`）中，它们会先被调度到主线程。
- `on_message(data)` 在 **UI 线程**上运行；请保持简短，把繁重的工作交给 `threading.Thread`，再用 `win.post(...)` 把结果推送回来。
- **模态**对话框（`show_dialog`）适合一次性的 `execute()`。**常驻**面板（`create_window`）最好在 `on_load()` 中打开，使其在插件的整个生命周期内存在；插件被卸载/重新加载或应用退出时，宿主会自动关闭插件的窗口。
- 内容以原始 HTML 形式加载；请尽量使用**自包含**的页面（内联 CSS/JS）。没有 CSP，开发者工具也被禁用。
