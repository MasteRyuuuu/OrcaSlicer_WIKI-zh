# 打印机代理

`orca.printer_agent` 模块提供 `PrinterAgentBase` 及其数据类型。打印机代理是 OrcaSlicer 在**设备**一侧所有事务的交互层：发现打印机、连接打印机、发送命令、回传状态，以及发送或启动打印任务。OrcaSlicer 自带多个内置代理（拓竹、Moonraker、Qidi、Snapmaker、CrealityPrint、Orca）。继承 `PrinterAgentBase` 的 Python 功能可以再添加一个代理。

| 基类 | `get_type()` 返回 | 必需的方法 | 调用者 |
|---|---|---|---|
| `orca.printer_agent.PrinterAgentBase` | `PrinterConnection` | `get_name()`、`get_agent_info()`，以及[方法]({{L1}})中列出的核心代理方法 | 选中该代理后，由网络 / 打印机代理层（`NetworkAgent`）调用 |

{{T1}}

## 启用打印机代理

有两项设置决定是否使用你的代理：

1. **偏好设置 -> 开发者 -> 实验性功能 -> 使用打印机代理替代打印主机**（应用配置中的 `use_printer_agents`，默认**关闭**）。关闭时，非拓竹打印机沿用传统的打印主机上传流程，所以插件代理永远不会收到打印任务。开启后，设备选项卡、打印按钮和侧边栏都会切换到代理模式。
2. **打印机设置 -> 基本信息 -> 高级 -> 打印机代理**（`printer_agent`，高级模式）。下拉列表按 `AgentInfo.name` 列出所有已注册的代理，内置代理在前，插件代理在后。预设保存的是 `AgentInfo.id` 字符串。值为空表示使用默认值：拓竹打印机为 `bbl`，其他所有打印机为 `orca`。参见[打印机高级设置]({{L2}})。

由于预设只保存代理 ID，如果预设所用的代理来自一个未安装的插件，就会像其他任何依赖插件的设置一样，被报告为缺失插件。

## 注册和代理 ID

像注册其他功能一样注册该功能（参见[注册]({{L3}})）：

{{C1}}

`get_type()` 已由 `PrinterAgentBase` 实现，返回 `orca.PluginType.PrinterConnection`（`"printer-connection"`）。你不需要重写它。

功能加载或启用时，OrcaSlicer 调用 `get_agent_info()`，并以 `AgentInfo.id` 注册代理：

- **ID 不能为空。** ID 为空时会记录一条警告，代理不会被注册。
- **ID 必须唯一。** `orca`、`bbl`、`qidi`、`snapmaker`、`crealityprint` 和 `moonraker` 这些 ID 属于内置代理。如果该 ID 已被某个内置代理或其他插件功能注册，该功能会被**拒绝**：插件被标记为出错（在插件对话框中显示为 *RuntimeError*，而插件本身仍保持加载），该功能被禁用，并弹出警告框，显示 `Printer-agent '<name>' could not be enabled: agent ID '<id>' is already registered by ...`。请选择一个不太可能冲突的 ID，并保持稳定：用户的预设中保存的就是它。
- **允许重新注册。** 当同一功能再次注册时（例如重新加载之后），它的条目会被刷新。如果它现在报告了不同的 ID，会先移除旧的 ID。
- `get_agent_info()` 在注册时调用，并且每当宿主切换当前生效的代理时会再次调用，所以它应当快速返回，并始终返回相同的值。

宿主为每个 ID 创建**一个**代理并缓存起来，所以功能实例本身就是当前生效的代理。你保存在 `self` 上的状态会在功能加载期间一直存在。

当功能被禁用或插件被卸载时，代理会被注销。如果它已被缓存，会调用 `disconnect_printer()`。如果它是当前生效的代理，宿主还会清除它，从而解除宿主回调（参见[生命周期]({{L4}})）。

## 方法

除非另有说明，每个方法都返回一个 `int` 状态码。`0`（`BAMBU_NETWORK_SUCCESS`）表示成功，其他任何值都表示失败。宿主还能识别两个 Orca 特有的代码：`-7010`（不支持该命令）和 `-7020`（这台打印机不具备该功能）。

### 核心方法

这些方法没有后备实现。如果某个方法缺失、抛出异常或返回了错误的类型，该调用会被记录为失败，宿主收到的是最后一列中的失败值。

| 方法 | 返回值 | 调用时机 | 失败值 |
|---|---|---|---|
| `get_agent_info(self)` | `AgentInfo` | 注册时，以及每当切换当前生效的代理时 | 空的 `AgentInfo`（ID 为空：代理不会被注册） |
| `connect_printer(self, params)` | `int` | 选中或重新连接某台机器时；`params` 是一个 `PrinterConnectionParams` | `-1` |
| `disconnect_printer(self)` | `int` | 取消选择机器、切换代理、注销代理、关闭网络时 | `-1` |
| `send_message(self, dev_id, json_str, qos, flag)` | `int` | 通过云端路径发布命令时 | `-1` |
| `send_message_to_printer(self, dev_id, json_str, qos, flag)` | `int` | 通过局域网发布命令时 | `-1` |
| `start_discovery(self, start, sending)` | `bool` | 代理开始生效之后（`True, False`）以及关闭时（`False, False`） | `False` |
| `bind_detect(self, dev_ip, sec_link, detect)` | `int` | 局域网"绑定 / 通过 IP 连接"流程；填写作为 `detect` 传入的 `DetectResult` | `-1` |
| `get_user_selected_machine(self)` | `str` | 宿主读取所选设备的 ID 时 | `""` |
| `set_user_selected_machine(self, dev_id)` | `int` | 所选设备改变时（`""` 表示取消选择） | `-1` |
| `start_send_gcode_to_sdcard(self, params, update_fn, cancel_fn, wait_fn)` | `int` | **发送**（上传但不打印）。也会以 `project_name="verify_job"` 且不带回调的方式调用，用来检查 IP 和访问码 | `-1` |
| `start_local_print(self, params, update_fn, cancel_fn)` | `int` | 通过局域网**打印** | `-1` |
| `start_print(self, params, update_fn, cancel_fn, wait_fn)` | `int` | 云端打印 | `-1` |
| `start_local_print_with_record(self, params, update_fn, cancel_fn, wait_fn)` | `int` | 带云端记录的局域网打印 | `-1` |
| `start_sdcard_print(self, params, update_fn, cancel_fn)` | `int` | 打印已在打印机存储中的文件 | `-1` |
| `check_cert(self)` | `int` | 证书检查 | `-1` |
| `ping_bind(self, ping_code)` | `int` | 绑定流程 | `-1` |
| `bind(self, dev_ip, dev_id, dev_model, sec_link, timezone, improved, update_fn)` | `int` | 绑定流程 | `-1` |
| `unbind(self, dev_id)` | `int` | 解除绑定 | `-1` |
| `request_bind_ticket(self)` | `(int, str)` 元组：状态和票据 | 绑定流程 | `-1`（票据保持不变） |
| `set_server_callback(self, fn)` | `int` | 注册回调，参见[宿主回调]({{L5}}) | `-1` |
| `set_on_ssdp_msg_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_on_printer_connected_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_on_subscribe_failure_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_on_message_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_on_user_message_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_on_local_connect_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_on_local_message_fn(self, fn)` | `int` | 注册回调 | `-1` |
| `set_queue_on_main_fn(self, fn)` | `int` | 注册回调 | `-1` |

> [!NOTE]
> `check_cert`、`ping_bind`、`bind`、`unbind` 和 `request_bind_ticket` 在 C++ 端有表示"成功"的默认实现，但 Python 桥接层没有这样的后备实现：没有实现它们的代理会返回 `-1`。如果你的打印机没有绑定步骤，请实现它们（返回 `0`，`request_bind_ticket` 则返回 `(0, "")`）。

`bind_detect` 把结果写入它收到的 `detect` 对象，这是宿主自己的 `DetectResult`。设置其字段并返回状态码：

{{C2}}

### 可选方法

如果这些方法**没有被重写**，就使用宿主的默认实现。如果重写的方法**抛出异常或返回了错误的类型**，宿主收到的是失败值（`-1`、`False`、`""` 或 `None_`），而不是默认实现的结果。

| 方法 | 返回值 | 未重写时的默认行为 |
|---|---|---|
| `command_ams_refresh_rfid(self, dev_id, ams_id, slot_id, sequence_id, lan_mode)` | `int` | `-7010`（不支持） |
| `command_ams_calibrate(self, dev_id, ams_id, sequence_id, lan_mode)` | `int` | `-7010` |
| `command_ams_select_tray(self, dev_id, tray_id, sequence_id, lan_mode)` | `int` | `-7010` |
| `command_start_camera(self, dev_id)` | `int` | `-7010` |
| `command_xyz_abs(self, dev_id, sequence_id, lan_mode)` | `int` | 以 `gcode_line` 命令发送 `G90` |
| `command_auto_leveling(self, dev_id, sequence_id, lan_mode)` | `int` | 发送 `G29` |
| `command_go_home(self, dev_id, is_printing, supports_mqtt_homing, sequence_id, lan_mode)` | `int` | 发送 `back_to_center`，或 `G28` / `G28 X` |
| `command_set_bed(self, dev_id, temp, supports_mqtt_bed_ctrl, sequence_id, lan_mode)` | `int` | 发送 `set_bed_temp`，或 `M140 S<temp>` |
| `command_set_nozzle(self, dev_id, temp, sequence_id, lan_mode)` | `int` | 发送 `M104 S<temp>` |
| `command_axis_control(self, dev_id, axis, unit, input_val, speed, is_core_xy, supports_mqtt_axis_control, sequence_id, lan_mode)` | `int` | 发送相对的 `G1`（X/Y/Z）或 `G0`（E）移动；其他任何轴返回 `-1` |
| `get_filament_sync_mode(self)` | `FilamentSyncMode` | `FilamentSyncMode.None_` |
| `fetch_filament_info(self, dev_id, sync_mode)` | `bool` | `False` |
| `get_camera_stream_mode(self)` | `CameraStreamMode` | `CameraStreamMode.None_` |
| `get_camera_url(self)` | `str` | `""` |
| `install_device_cert(self, dev_id, lan_only)` | `None` | 什么也不做 |
| `get_hms_snapshot(self, dev_id, file_name, callback)` | `int` | `-1`；实现时返回 `0`，并通过 `callback(body, http_status)` 传回图像 |

默认的 `command_*` 实现会构建一个拓竹风格的 JSON 命令（`{"print": {"command": "gcode_line", "param": "...", "sequence_id": "..."}}`），`lan_mode` 为真时把它交给**你的** `send_message_to_printer()`，否则交给 `send_message()`。在 `send_message*` 中翻译这些 JSON 命令的代理，就能直接获得打印机控制功能。重写某个 `command_*` 方法，可以直接使用你的打印机自己的协议。

`get_filament_sync_mode()` 控制耗材丝同步。选择 `Subscription` 时，侧边栏的耗材丝列表会在所选打印机的每条局域网消息到来时重新加载。选择 `Pull` 时，OrcaSlicer 在需要数据时调用 `fetch_filament_info(dev_id)`。

### Python 无法使用的方法

`set_cloud_agent` 由宿主管理。`default_lan_username`、`start_subscribe`、`stop_subscribe`、`add_subscribe`、`del_subscribe`、`to_orca_filament_id` 和 `from_orca_filament_id` 属于 C++ 接口，但不会转发给 Python：插件代理始终使用默认实现。特别是，对于 Python 代理，`PrinterConnectionParams.username` 始终为空。

## 数据类型

所有类型都位于 `orca.printer_agent` 中。它们的字段可读可写。

**`AgentInfo`**：`AgentInfo()` 或 `AgentInfo(id, name, version, description)`。

| 字段 | 含义 |
|---|---|
| `id` | 唯一的代理 ID，保存在打印机预设中（参见[注册和代理 ID]({{L6}})） |
| `name` | 打印机代理下拉列表中的显示名称 |
| `version` | 代理版本字符串 |
| `description` | 简短描述 |

**`PrinterConnectionParams`**：传给 `connect_printer()`。

| 字段 | 类型 | 含义 |
|---|---|---|
| `dev_id` | `str` | 所选机器的设备 ID |
| `host` | `str` | 去掉 `http://` / `https://` 前缀后的主机地址 |
| `port` | `str` | 地址中的端口，否则为预设中的 `printhost_port`；可能为空 |
| `username` | `str` | 对于 Python 代理始终为空 |
| `password` | `str` | 机器的访问码。对于根据预设创建的机器，这是 `printhost_apikey`；若其为空，则为 `88888888` |
| `use_ssl` | `bool` | 地址以 `https` 开头时为 `True` |
| `ca_file` | `str` | 预设中的 `printhost_cafile` |

**`PrintParams`**：传给各 `start_*` 方法。主要字段：

| 字段 | 含义 |
|---|---|
| `dev_id`、`dev_ip`、`dev_name` | 目标设备 |
| `filename` | 要发送的文件的本地路径（3MF，或者用于验证上传的临时文件） |
| `project_name`、`task_name`、`preset_name`、`plate_index` | 任务标识；连接检查时 `project_name` 为 `"verify_job"` |
| `password`、`username` | 访问码和局域网用户 |
| `connection_type` | 例如 `"lan"` |
| `use_ssl_for_ftp`、`use_ssl_for_mqtt` | 传输标志 |
| `dst_file` | 打印机上的目标路径（如果设置了的话） |
| `ams_mapping`、`ams_mapping2`、`ams_mapping_info`、`nozzle_mapping`、`nozzles_info` | 以 JSON 字符串表示的耗材丝 / 喷嘴映射 |
| `task_bed_leveling`、`task_flow_cali`、`task_vibration_cali`、`task_layer_inspect`、`task_record_timelapse`、`task_use_ams`、`task_bed_type`、`task_ext_change_assist` | 用户的打印选项 |
| `auto_bed_leveling`、`auto_flow_cali`、`auto_offset_cali` | `int` 类型的打印选项 |

其余已绑定的字段有 `config_filename`、`ftp_folder`、`ftp_file`、`ftp_file_md5`、`comments`、`origin_profile_id`、`stl_design_id`、`origin_model_id`、`print_type`、`extra_options` 和 `try_emmc_print`。

**`DetectResult`**：由 `bind_detect()` 填写。所有字段都是字符串：`result_msg`、`command`、`dev_id`、`model_id`、`dev_name`、`version`、`bind_state`、`connect_type`。

**`FilamentSyncMode`**：`None_`、`Subscription`、`Pull`。

**`CameraStreamMode`**：`None_`、`HTTP`、`HTTPS`、`HTTP_SNAPSHOT`、`RTSP`。

> [!TIP]
> 这两个枚举都会把各自的值导出到 `orca.printer_agent` 中，并且都有一个名为 `None_` 的成员。请始终使用限定形式（`FilamentSyncMode.None_`、`CameraStreamMode.None_`），而不要写 `orca.printer_agent.None_`。

## 宿主回调

当代理开始生效时，宿主会把每个 `set_*_fn` 方法各调用一次，并传入一个可调用对象。保存它，并调用它把事件推送到 OrcaSlicer 中。宿主会自行把这些回调调度到 UI 线程上，所以你可以从任何线程调用它们，包括你自己的 `threading.Thread`。

| 设置方法 | 回调签名 | 用途 |
|---|---|---|
| `set_on_ssdp_msg_fn` | `fn(dev_info_json: str)` | 报告发现的打印机（见下文） |
| `set_on_local_connect_fn` | `fn(status: int, dev_id: str, msg: str)` | 局域网连接状态：`0` = 正常，`1` = 失败，`2` = 断开 |
| `set_on_local_message_fn` | `fn(dev_id: str, msg: str)` | 局域网状态推送；设备模型会把它当作带有 `print` 对象的拓竹风格 JSON 来解析 |
| `set_on_message_fn` | `fn(dev_id: str, msg: str)` | 云端状态推送 |
| `set_on_user_message_fn` | `fn(user_id: str, msg: str)` | 用户范围的云端消息 |
| `set_on_printer_connected_fn` | `fn(topic: str)` | 云端打印机连接 |
| `set_on_subscribe_failure_fn` | `fn(topic: str)` | 订阅失败 |
| `set_server_callback` | `fn(url: str, status: int)` | 致命的服务器错误 |
| `set_queue_on_main_fn` | `fn(task)`，其中 `task` 是一个无参数的可调用对象 | 在 UI 线程上运行 `task` |

传给 SSDP 回调的发现消息是一个 JSON 对象，包含字符串字段 `dev_id`、`dev_name`、`dev_ip`、`dev_type`、`dev_signal`、`connect_type`（例如 `"lan"`）和 `bind_state`（例如 `"free"`）。`sec_link`、`ssdp_version` 和 `connection_name` 是可选的。

各 `start_*` 方法会收到每个任务专用的可调用对象：

| 参数 | 签名 | 用途 |
|---|---|---|
| `update_fn` | `update_fn(status: int, code: int, msg: str)` | 报告进度 |
| `cancel_fn` | `cancel_fn() -> bool` | 轮询用户是否取消 |
| `wait_fn` | `wait_fn(status: int, job_info: str) -> bool` | 云端流程使用的等待步骤 |

> [!IMPORTANT]
> 任何可调用对象都可能是 `None`。宿主在解除代理或关闭网络时会给设置方法传入 `None`，有些 `start_*` 调用也会给任务回调传入 `None`（例如 `verify_job` 上传）。每次调用之前都要检查是否为 `None`。

## 线程

代理没有专用的线程。每个方法都在宿主调用它的那个线程上运行。选择、发现、连接和注册回调发生在 UI 线程上。打印和发送任务（`start_*`）在后台任务线程上运行。每次调用在其执行期间都会持有 Python GIL。

- 在 UI 线程上调用的方法要尽快返回。把长时间运行的工作（轮询、websocket、在调用结束后仍需继续的上传）放到你自己的线程中，并通过保存的回调报告结果。
- 不要使用你自己的 GUI 工具包。如果需要界面，请使用 `orca.host.ui`（参见[宿主 UI]({{L7}})）。
- 文件系统、网络和进程访问与其他所有插件调用一样会受到审计（参见[插件审计钩子]({{L8}})）。

## 错误处理

宿主通过 C++ 的 `IPrinterAgent` 接口调用代理方法，该接口通过返回值报告失败，其调用方不会捕获异常。因此，**Python 代理抛出的任何异常都不会到达宿主**。如果某个方法抛出异常、缺失或返回了错误类型的值：

1. Python 回溯（如果有）写入 Python 日志，`Printer agent plugin '<plugin>': <method> failed: <error>` 写入 OrcaSlicer 日志。
2. 宿主收到的答复与完全没有代理时相同：`int` 为 `-1`，或者 `False`、`""`、空的 `AgentInfo`、`None_`，或什么也没有。
3. 解释器和插件保持加载。不会显示任何对话框。

对于可以预料到的失败，请返回非零状态码，而不是抛出异常。Python 日志的位置请参见[错误如何呈现]({{L9}})。

## 生命周期

1. **加载**：插件加载，`on_load()` 运行，代理以其 `AgentInfo.id` 注册。
2. **选择**：当当前打印机预设解析到你的 ID 时，宿主让你的代理开始生效。它先调用 `get_agent_info()`，然后调用每个 `set_*_fn` 设置方法、`start_discovery(True, False)`，最后选择预设中打印主机所指的机器。对于局域网机器，这次选择会调用 `connect_printer()`。在使用同一代理的预设之间切换时，只有打印主机不同时才会重新选择机器。
3. **切换走**：当另一个代理开始生效时，宿主会取消选择机器（`set_user_selected_machine("")`），调用 `disconnect_printer()`，并以 `None` 调用每个设置方法。
4. **禁用 / 卸载**：代理被注销（调用 `disconnect_printer()`，如果当前生效的代理是你的，则将其清除），然后运行 `on_unload()`。请在那里停止你的线程。

每项功能还有 `on_lifecycle_event(self, event, ctx)`。与设备相关的事件有 `orca.LifecycleEvent.DeviceDiscovered`、`DeviceSelected`、`DeviceOnline`、`DeviceOffline` 和 `PrintStateChanged`。对于设备事件，`ctx.name` 保存设备 ID（取消选择时为空）；对于 `DeviceOnline` / `DeviceOffline`，`ctx.msg` 为 `"online"` / `"offline"`。完整列表请参见[生命周期事件]({{L10}})。

## 最小示例

这个代理报告一台固定的局域网打印机，并接受上传。它实现了所有核心方法，所以不会有任何方法意外返回 `-1`。请把标有 `TODO` 的方法体替换为你的打印机协议。

{{C3}}

要试用它，请开启**使用打印机代理替代打印主机**，然后在打印机预设的**打印机代理**中选择 **Example**，并把打印主机设为打印机的地址。

关于注册和命名规则，请参见[注册]({{L11}})；关于打包和测试，请参见[插件开发]({{L12}})。
