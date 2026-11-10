# 插件审计钩子

本页介绍 OrcaSlicer 插件系统所使用的 CPython 审计钩子。Python 可以读写文件、启动进程、打开套接字和加载原生代码，因此插件执行这几类操作时，会在 CPython 执行之前提示用户做出**是/否**决定，记住的答复会按插件持久保存。

> [!NOTE]
> 这是一个交互式的权限系统，而不是沙箱：点击**是**的用户就授权了该操作，此后没有任何隔离层能阻止真正恶意的插件造成破坏。目前它对文件系统、网络、启动进程和创建线程事件进行分类和把关；加载原生代码（`ctypes`）不受审计，插件创建的线程启动后所做的事情也不会归属到该插件。在把它当作安全边界之前，请先阅读[当前已知的限制]({{L1}})。

## 什么是插件审计钩子？

CPython 提供了一个审计 API（PEP 578）。用 `PySys_AddAuditHook` 注册的任何解释器全局钩子，都会在运行时执行敏感操作*之前*被调用——例如打开文件（`open`）、启动子进程（`subprocess.Popen`）或连接套接字（`socket.connect`）。钩子会收到事件名称及其参数，并且可以通过设置 Python 异常并返回非零值来中止该操作。

我们只注册**一个**这样的钩子，并且只注册一次：在 `PythonInterpreter.cpp` 中通过 `PluginAuditManager::instance().install_hook()` 注册。它是一个进程级的 C 钩子——插件代码周围没有单独的解释器或进程沙箱；审计钩子本身就是边界。其他一切——*哪个*插件正在运行、它试图做*什么*，以及*用户已经批准了什么*——都由 `PluginAuditManager` 跟踪。

钩子只在插件**审计上下文**处于活动状态时才起作用（见下文）。非插件的 Python 代码，以及设置上下文之前的插件加载过程，都会直接放行。

## 工作原理

### 1. 审计身份

每个功能实例都带有一个仅限 C++ 的身份，从不暴露给 Python：

{{C1}}

这就是规范的运行时 ID，即 `PluginDescriptor::plugin_key`。加载器在捕获插件**之后**、运行 `on_load()` **之前**把它标记到实例上：

- `PluginLoader::load_plugin_impl()` -> `set_audit_plugin_key(descriptor.plugin_key)`
- `PluginLoader::update_loaded_plugin_key()` -> 如果键发生迁移，则重新标记

标记身份本身**不会**开启强制检查——它只是给对象打上标签，让之后的调用知道自己属于哪个插件。这一点很重要，因为打印机代理插件之后是通过 `IPrinterAgent` / `NetworkAgent` 调用的，在调用点已经拿不到原来的 `plugin_key`；改由实例自身携带它。

### 2. 审计上下文

当前的插件、功能名称以及作用域内的根目录保存在 `PluginAuditManager` 的 `thread_local` 状态中，由 RAII 守卫 `ScopedPluginAuditContext` 设置和恢复：

{{C2}}

上下文在**每次 C++ 到 Python 的 trampoline 调用开始时**开启（参见 [trampoline 与审计宏]({{L2}})），在该调用返回或抛出异常时关闭。因此强制检查是*按调用*进行的：在任何 trampoline 调用之外，`current_plugin()` 为空，`audit_hook` 会无条件放行一切——OrcaSlicer 自身内部对 Python 的使用，以及第一次 trampoline 调用之前的插件导入/注册，就是这样保持不受审计的。

**由于是 `thread_local`，上下文不会传递到插件自己创建的 Python 线程中**（`threading.Thread`、`_thread.start_new_thread`……）。新创建的操作系统线程拥有自己空白的 `thread_local` 存储，所以在其中读取 `current_plugin()` 为空，该线程所做的一切都不受审计，除非它恰好回调进某个 C++ 到 Python 的 trampoline。创建这样的线程本身会作为 `Threading` 事件单独把关（参见[类别解析]({{L3}})），但那项授权只涵盖创建线程这一动作，不涵盖新线程运行的内容。

### 3. 类别解析

每个受审计的 CPython 事件都映射到一个 `AuditEventCategory`：

{{C3}}

`audit_event_categories`（`PluginAuditManager.cpp`）是一张扁平的 `event_name -> category` 查找表。`event_category(event_name)` 对未列出的任何事件返回 `None`，`audit_hook` 会立即放行类别为 `None` 的事件，不做审计。

| 类别 | 事件 |
|---|---|
| `FsRead` | `glob.glob`、`glob.glob/2`、`os.fwalk`、`os.getxattr`、`os.listdir`、`os.listdrives`、`os.listmounts`、`os.listvolumes`、`os.listxattr`、`os.scandir`、`os.walk`、`pathlib.Path.glob`、`pathlib.Path.rglob` |
| `FsReadWrite` | `os.chflags`、`os.chmod`、`os.chown`、`os.removexattr`、`os.rename`、`os.setxattr`、`os.truncate`、`os.utime`、`shutil.chown`、`shutil.copymode`、`shutil.copystat`、`shutil.copyfile`、`shutil.copytree`、`shutil.make_archive`、`shutil.move`、`shutil.unpack_archive` |
| `FsCreate` | `os.link`、`os.mkdir`、`os.symlink`、`tempfile.mkdtemp`、`tempfile.mkstemp`、`_winapi.CreateJunction` |
| `FsDelete` | `os.remove`、`os.rmdir`、`shutil.rmtree` |
| `Http` | `http.client.connect`、`http.client.send`、`urllib.Request` |
| `Socket` | `socket.__new__`、`socket.bind`、`socket.connect`、`socket.getaddrinfo`、`socket.gethostbyaddr`、`socket.gethostbyname`、`socket.gethostname`、`socket.getnameinfo`、`socket.getservbyname`、`socket.getservbyport`、`socket.sendmsg`、`socket.sendto` |
| `ProcessCreate` | `os.fork`、`os.forkpty`、`os.posix_spawn`、`os.spawn`、`os.system`、`os.startfile`、`os.startfile/2`、`pty.spawn`、`subprocess.Popen`、`_winapi.CreateProcess`、`_posixsubprocess.fork_exec` |
| `Threading` | `_thread.start_new_thread`（创建线程；`threading.Thread` 也是通过这个调用实现的，但新线程自身的工作不受审计） |

`open` 是一个特例，会在查表之前检查：CPython 的 `open` 审计事件既会由 `open()`/`io.open()` 触发（`args = (path, mode, flags)`，`mode` 是 `"r"`/`"wb"`/`"a+"` 之类的字符串），也会由底层的 `os.open()` 触发（`mode` 为 `None`，`flags` 中携带的是数字形式的 `os.O_*` 位掩码）。单纯的只读模式字符串解析为 `FsRead`；其他任何情况——带有写入/追加/创建/截断/独占模式字符，或者无法识别的 `None` 模式——都解析为 `FsReadWrite`。这是唯一一个类别取决于参数而不是名称的事件，所以它不能放在静态映射表中。

### 4. 决策流程

`audit_hook` 先解析类别（`None` -> 放行，不审计），然后依次执行：

1. **禁止路径检查**（仅限文件系统类别——`is_denied_path`，参见下文的[允许的根目录和禁止的路径]({{L4}})）。如果任何目标是被禁止的文件名，或匹配被禁止的路径关键字，就立即阻止：调用 `report_denied`，不显示对话框——无论祖先级联批准或允许的根目录本来会给出什么结论。它被特意放在接下来两步*之前*执行，使两者都无法为访问被禁止的路径"洗白"。
2. **祖先级联检查。** 如果当前的 Python 调用栈中已经包含一个在同一调用链中为先前事件批准过的标准库帧，就立即放行，不显示对话框。
3. **允许根目录的快捷通道**（仅限文件系统类别——`check_path_access`）。如果每个目标都解析到某个允许的根目录内——并且对于写入/创建/删除类的事件，该根目录允许写入——就立即放行，不显示对话框，也不持久保存任何内容。
4. 其余情况统一交给 `PluginAuditDetail::decide_audited_event` 处理：
    1. **提取目标**（`audit_targets`）——事件所指的路径/地址/命令，作为用于显示和持久保存的字符串。
    2. **查找该类别的权限列表**（`permission_list_for`）——对于从不持久保存的类别为 `nullptr`。
    3. **从待提示列表中过滤掉已授权的目标。** 如果该类别会持久保存授权，并且每个目标都已获授权，就放行，不显示对话框。
    4. 对仍未解决的所有目标**显示一个对话框**（`audit_message` + 一个"是/否"消息框）。
    5. **选择"是"时**：持久保存每个新批准的目标（如果该类别会持久保存），把当前的调用点链记录为已批准（用于级联检查），然后放行。
    6. **选择"否"时**：`report_denied` 记录一条 `AuditViolation`，在调用方解释器中抛出 `PermissionError`，钩子返回 `-1`——CPython 把非零返回值视为"阻止此操作"，所以受审计的调用永远不会完成。

对话框是模态的；当事件在主线程/UI 线程上触发时，它的答复适用于当前事件。事件也可能在 UI 线程本身可能正在等待的线程上触发（切片流水线钩子在切片工作线程上运行）。在那个线程上用对话框阻塞会让应用程序死锁，所以提示会被**异步**发送到 UI 线程，当前事件被拒绝（失败即关闭，与未答复的提示完全相同），而用户接受时会持久保存这次**是**。因此插件下一次访问同一目标时会直接成功，不再提示。插件**加载**运行在 UI 线程不会等待的工作线程上，所以在那里调用的声明式 `request_permissions(...)` 可以把对话框同步调度到 UI 线程并等待答复（参见[持久化]({{L5}})）。

#### 目标提取

- **文件系统类别**（`FsRead`/`FsReadWrite`/`FsCreate`/`FsDelete`，包括 `open`）：目标是路径，通过 `PyOS_FSPath` 读取（所以 `str` 和类路径对象都可以）。几乎所有文件系统事件的路径都是参数 0；一小部分例外列在 `two_path_fs_events` 中，即接受*源和目标*两个路径的事件（`os.rename`、`os.link`、`os.symlink`、`shutil.copyfile`/`copytree`/`copymode`/`copystat`/`move`/`unpack_archive`、`_winapi.CreateJunction`）——两个参数会出现在*同一个*对话框中，并保存为*同一份*持久授权。
- **http/socket/processcreate**：`audit_target_arg_indices` 把每个事件映射到若干候选参数索引，按顺序尝试，直到某个参数的 `str()` 不为空。使用 `str()` 可以免去手动解析每一种地址形式（`AF_INET` 的主机/端口元组、`AF_UNIX` 路径、`AF_INET6` 等）——`str()` 得到什么，什么就成为稳定的目标/持久化键。`http.client.send` 被有意排除在外：它自身的参数中不包含主机，转而依赖祖先级联。
- **没有合适对象可指的事件**（`socket.__new__`、`os.fork`……）得到一个空的目标列表。提示中写明的是事件本身，授权按事件保存在 `permissions.events` 下，键为 `<Category>:<event>`（例如 `Socket:socket.__new__`）。这样可以避免事件授权被当成同一类别中同名字符串的目标授权。

#### 持久化

持久保存的类别与 `PluginPermissions`（`PluginFsUtils.hpp`）一一对应：

| 类别 | `PluginPermissions` 字段 |
|---|---|
| `FsRead` | `fs_read` |
| `FsReadWrite` | `fs_readwrite` |
| `Http` | `network_http` |
| `Socket` | `network_socket` |
| `ProcessCreate` | `process` |
| `Threading` | `threading`（始终是固定目标 `thread`） |
| `FsCreate`、`FsDelete` | *（无——从不持久保存）* |

没有目标的事件持久保存到 `events` 中，而不是某个类别列表中；参见[目标提取]({{L6}})。

`FsCreate`/`FsDelete` 总是会提示，跨调用不会记住任何答复，因为创建或删除文件的后果足够严重，每次都需要确认，即使是同一次运行中重复操作同一个目标。

授权是与持久保存列表进行的简单字符串相等匹配（`has_permission`）——不做路径规范化，除了 `str()` 已经得到的结果之外也不识别参数形式。`persist_permission` 直接写入插件的 `.install_state.json` 附属文件：

{{C4}}

与这种被动式授权并存的，还有一条**声明式**的授权途径：在 `register_capabilities()` 中调用 `orca.request_permissions(...)`，预先声明插件预期会用到什么，而不是等到每次首次访问时才提示：

{{C5}}

每个分组接受对应审计事件所报告的目标字符串：`fs_read`/`fs_readwrite` 为文件系统路径，`network_http` 为 URL，`network_socket` 为套接字地址，`process` 为命令。`threading=True` 申请固定目标 `thread`。所有参数都是可选的，默认为空列表 / `False`。

声明在 `register_capabilities()` 运行期间收集。随后，宿主在该方法返回之后、**创建任何功能实例之前**，显示**一个合并的对话框**；已经为该插件持久保存的目标会被跳过，所以重复声明已授权的目标不会再次提示。拒绝请求会以错误中止插件加载，不会实例化任何功能。在插件发现过程之外调用它会抛出 `ValueError`，任何目标列表中出现空字符串也会如此。

两条途径写入的是同一份 `permissions` 列表，所以通过声明获得授权的目标同样满足被动检查，反之亦然。声明并不会放宽策略：它只预先批准所声明的确切目标，其他任何访问在首次使用时仍会提示。

已授予的权限属于已安装的包，而不仅仅属于插件键：每次成功安装（在现有插件上安装本地插件、**重新安装**或云端更新）都会清除该插件附属文件中的 `permissions` 块（`PluginManager::revoke_plugin_permissions()`），所以新代码必须重新获得访问授权。

#### 调用点祖先级联

一个逻辑上的插件操作在穿过标准库各层时，往往会触发多个*嵌套的* CPython 审计事件——`urllib.request.urlopen()` 在返回之前，内部会依次触发 `urllib.Request`、`http.client.connect` 和 `http.client.send`。如果不做特殊处理，用户眼中的一个操作就会弹出三个独立的提示。

`call_site_identities(plugin_root)` 从当前触发的事件开始向上遍历实时的 Python 调用栈，为每一帧构建一个身份字符串（`filename:function:first_line`），并且**一旦遇到文件位于插件自身 `plugin_root` 之下的帧就停止**。只返回受审计调用与这一边界之间的标准库/第三方帧。

这种排除至关重要：插件自己的入口点（例如其功能的 `execute()`）是插件所做每个操作的祖先。如果把插件帧也算进来，批准*任何*一次提示都会把那个入口点帧记录为"已批准"，那么该次调用中任何地方的后续操作——而且由于身份是按代码位置而不是按活动对象确定的，*将来对同一函数的任何调用*也一样——都会悄无声息地绕过审计。把记录的帧限制为库代码，意味着 `urllib.Request` 和 `http.client.connect` 实际共享的身份是 `urlopen()` 自己的标准库帧，它对两者来说确实都还在栈上——级联只会在一条仍然活动、执行同一个由库完成的操作的调用链内生效，而不是"这个插件曾经被批准过一次"。

这个缓存（`unordered_map<plugin_key, unordered_set<call_site_id>>`）只存在于内存中，从不持久保存到附属文件，也从不清理——它随插件操作经过的不同标准库调用点的数量增长，实际上数量很小，并且受插件自身代码的限制。

### 允许的根目录和禁止的路径

`check_path_access(path, is_write)` / `check_open(path, mode)` 实现了第二层策略，`audit_hook` 会在按目标显示对话框/持久化的流程之前直接查询它（即上文决策流程的第 1 步和第 3 步）：

1. **按文件名禁止**（`is_denied_filename`——应用配置和云端刷新令牌，按基本文件名的前缀匹配，不区分大小写，所以也涵盖 `.bak`/`.tmp` 附带文件和 Windows 备用数据流变体）。
2. **按路径关键字禁止**（`is_denied_path_keyword`——任何路径*组成部分*（而不仅仅是基本文件名）中，不区分大小写地包含 `"secret"`、`"cert"` 或 `"conf"`，初始值来自 `default_denied_path_keywords()`）。它被有意设计得比（1）更宽泛、更模糊：它排除了整*类*敏感路径——`secrets/` 子文件夹、`certificates/` 文件夹、`*.conf`/`config/` 文件或文件夹——无论它们位于哪里，包括位于原本允许的根目录之内，代价是可能误伤恰好包含这些关键字的无关名称。这是偏向安全的方向，理由与（1）相同。
3. **只有位于允许的根目录内才放行**（`is_inside_allowed_root`，使用 `weakly_canonical` + 逐个组成部分比较，拒绝 `..` 路径穿越）——可以是作用域根目录（`m_scoped_allowed_roots`，`thread_local`，按每个 `ScopedPluginAuditContext` 作用域清除和恢复），也可以是全局根目录（`m_global_allowed_roots`，由互斥锁保护，进程级）。每个已注册的根目录（`AllowedRoot { path; allow_write; }`）都带有自己的写入权限：注册为只读的根目录会匹配读取类的请求，但绝不匹配写入/创建/删除类的请求，后者对该根目录而言会被视为"位于允许的根目录之外"。

`is_denied_path(path)` 是 `is_denied_filename(path) || is_denied_path_keyword(path)` 的便捷写法，`audit_hook` 在决策流程第 1 步调用它，此时甚至还不知道目标位于哪个根目录内（如果有的话）。

`install_hook()` 会填充两种根目录和两个禁止列表：

| 根目录 | 访问权限 | 涵盖范围 |
|---|---|---|
| `data_dir()`（全局） | 读写 | 每个插件的存储文件夹（`data_dir()/orca_plugins`）、已安装/系统配置缓存（`data_dir()/system`），以及 `data_dir()` 的其余部分 |
| `resources_dir()`（全局） | **只读** | 应用捆绑的共享资源（已安装的系统配置、捆绑的 TLS 客户端证书、网页资源）——永远不可写入，因为安装目录在磁盘上可能是共享的/只读的 |
| 当前 G-code 文件的父目录（作用域，`SlicingPipelinePluginCapabilityTrampoline::execute()`） | 读写 | 仅当 `psGCodePostProcess` 调用位于栈上时，并且仅针对该次调用 |

禁止的文件名：`default_denied_filenames()`（应用配置的两种扩展名和应用密钥，以及云端刷新令牌）。禁止的关键字：`default_denied_path_keywords()` = `{"secret", "cert", "conf"}`——正是它让位于 `resources_dir()/cert/...` 的捆绑证书无法访问，尽管 `resources_dir()` 本身是允许的根目录。

`check_path_access`/`check_open` 由 `tests/slic3rutils/test_plugin_audit.cpp` 直接测试，不依赖运行中的解释器。

## 审计钩子开发

需要关注的是 **`PluginAuditManager.hpp`/`.cpp`**（类别、目标、持久化、决策流程）和 **`PyPluginTrampoline.hpp`**（每个插件函数如何开启审计上下文）。

### 映射新事件

要审计一个尚未覆盖的 CPython 事件，请把它添加到 `PluginAuditManager.cpp` 中 `audit_event_categories` 里它所属的类别下（如果没有合适的类别，先在枚举中扩展一个新类别）。在为它接入 `audit_targets`/`audit_target_arg_indices` 之前，请在官方表格中查到该事件确切的参数元组——每个事件都有自己的参数形式；对于 `two_path_fs_events` 以外的事件，不能想当然地认为参数 0 就是路径。

完整的、与版本对应的审计事件及其参数列表：
**{{U1}}**

如果该事件应当持久保存授权，请在 `permission_list_for` 中把它的类别映射到正确的 `PluginPermissions` 字段；如果不应当（如 `FsCreate`/`FsDelete`），就让它每次都提示。

### trampoline 与审计宏

每次 C++ 到 Python 的插件调用都会经过一个 trampoline 方法，每个方法都通过 `PyPluginTrampoline.hpp` 中的两个宏之一开启审计上下文：

{{C6}}

`ORCA_PY_AUDIT_SCOPE()` 是基本原语：它为当前调用开启 `ScopedPluginAuditContext(audit_plugin_key(), name())`，但前提是实例确实有一个非空的审计键（如果加载器从未给插件标记身份，就不会开启任何上下文，它的调用也就不受审计——参见[身份接线]({{L7}})）。几乎每个 trampoline 方法实际调用的都是 `ORCA_PY_OVERRIDE_AUDITED`：它在唯一的 C++/Python 边界上，把这个作用域与引用计数守卫、GIL 获取以及回溯的记录/重新抛出包装在一起。两个真实的调用点：

{{C7}}

{{C8}}

需要手动解包 Python 返回值（而不是使用普通 pybind11 重写）的方法，可以直接调用 `ORCA_PY_AUDIT_SCOPE()`，而不经过 `ORCA_PY_OVERRIDE_AUDITED`——`PrinterAgentPluginCapabilityTrampoline::request_bind_ticket` 就是这样做的，以便通过输出参数解包一个 `(result, ticket)` 元组。

| 参数 | 含义 |
|---|---|
| `audit_setup` | 在上下文开启*之后*运行的可调用对象（通常是 `[] {}`）；用它来注册作用域根目录 |
| `override_macro` | `PYBIND11_OVERRIDE` 或 `PYBIND11_OVERRIDE_PURE` |
| `ret, base, name, ...` | 常规的 pybind11 重写参数 |

没有按调用选择的"模式"参数——每次 trampoline 调用都以同样的方式接受审计；不同调用之间唯一的区别是 `audit_setup` 回调（见下文）。

### 添加按调用的作用域根目录

`ScopedPluginAuditContext` 的构造函数会清除之前的作用域根目录，所以作用域根目录必须在构造*之后*添加——这正是 `audit_setup` 的用途。切片流水线的 trampoline 用它在 `psGCodePostProcess` 时授予对当前 G-code 文件所在文件夹的写入权限，允许根目录的快捷通道（决策流程第 3 步）现在确实会查询它：

{{C9}}

把第二个参数设为 `false` 可以授予一个**只读**的作用域根目录——`add_scoped_allowed_root(root, /*allow_write=*/false)`——用于应当能够读取某个目录、但不能写入的调用。

### 添加全局允许的根目录

如果*每个*插件都应当被允许访问某个目录，请在 `install_hook()` 中添加。`install_hook()` 授予 `data_dir()` 读写权限，授予 `resources_dir()` 只读权限：

{{C10}}

优先使用作用域根目录，而不是扩大全局根目录；除非插件确实需要在那里写入，否则优先使用只读而不是读写——全局根目录在整个进程生命周期内有效，并适用于每个插件。记住，禁止检查（文件名和关键字）会在查询任何根目录*之前*运行，所以全局根目录永远无法让被禁止的路径变得可以访问。

### 身份接线

如果你添加了加载插件实例或为其重新设置键的新途径，请确保新途径也会调用 `set_audit_plugin_key()`；否则实例的键为空，`ORCA_PY_AUDIT_SCOPE()` 永远不会开启上下文，它的调用会完全不受审计。现有的调用点是 `PluginLoader::load_plugin_impl()` 和 `PluginLoader::update_loaded_plugin_key()`。

## 当前已知的限制

- **`is_denied_path_keyword` 是简单的子字符串匹配，而不是有针对性的规则。** 名称正当的插件文件，例如 `myconfig.py` 或 `deconfliction_report.txt`，也会被阻止。这是有意为之（参见[允许的根目录和禁止的路径]({{L8}})），但除了删除关键字之外，没有允许列表机制可以放行某个被误伤的特定名称。
- **允许根目录的快捷通道对四种文件系统类别一视同仁**，包括 `FsCreate`/`FsDelete`：在允许的根目录内创建/删除（例如 `data_dir()` 下插件自己的文件）现在会完全跳过按调用的对话框；而在允许的根目录之外，`FsCreate`/`FsDelete` 仍然总是提示并且从不持久保存（参见[持久化]({{L9}})）。预先确定的允许根目录本来就意味着完全不需要提示——这是与单纯的"类别 + 对话框"模型之间有意为之的行为差异，而不是缺陷。
- **创建线程会被把关，但新线程中的工作不会。** `_thread.start_new_thread`（因而也包括 `threading.Thread`）映射到 `Threading`，并以固定目标 `thread` 按插件授权，但新线程运行时的 `thread_local` 插件上下文为空，所以它所做的事情不受审计，除非它通过 C++ 到 Python 的 trampoline 调用重新进入。
- **声明式请求只预先批准它所声明的确切字符串。** 没有通配符、目录前缀或地址规范化：每个目标仍然必须与审计事件报告的字符串相匹配，而且对话框只能全部接受或全部拒绝（拒绝会中止加载）。
- **不解码 `os.open()` 的数字标志形式。** 当 `mode=None` 时，它总是解析为 `FsReadWrite`，对于实际上只读的 `os.open()` 调用可能会多余地提示。
- **`Http`/`Socket`/`ProcessCreate` 的持久化以提取出的参数（地址元组、argv 列表……）的 `str()` 为键**，而不是规范化/验证后的值——批准一次调用，可能会悄无声息地覆盖将来另一次相关参数恰好 `str()` 结果相同的调用。
- **这不是加固的沙箱。** 批准提示的用户就授权了该操作；加载原生代码（`ctypes`）则完全不受审计。

## 调试

强制检查只在上下文处于活动状态时才会触发，而且现在还取决于用户在对话框中点击了什么，所以当某些操作意外被阻止（或意外没有提示）时，先从日志中查明事实。

**实际的阻止路径。** 对话框/权限流程中的拒绝会记录：

{{C11}}

它来自 `report_violation`，在用户回答**否**之后由 `decide_audited_event` 触发。`audit_denial_pending()` / `last_violation()` 让下游的 C++ 端（例如捕获由此产生的 `pybind11::error_already_set` 的 `ORCA_PY_LOGGED_OVERRIDE_BODY`）能够区分审计拒绝和普通的 Python 异常；它会在记录回溯之前清除 `current_plugin()`，这样在格式化/记录异常时接触到的任何东西，都不会以已经离开的插件的名义接受审计。

**同一个文件中还有第二种更嘈杂的日志行**——`[AUDIT] block path=... is_write=...`——由 `check_path_access` 本身以 `warning` 级别发出，每当某个目标未通过*这项特定检查*时都会出现：被禁止的文件名/关键字，或者路径位于所有允许的根目录之外。由于 `audit_hook` 的允许根目录快捷通道（决策流程第 3 步）现在会为每个文件系统类别的目标调用 `check_path_access`，这一行在"不在允许列表中，转入正常提示"这种普通的预期情况下出现得和真正的拒绝一样频繁——**它本身并不意味着操作被阻止了**。只有 `[AUDIT BLOCKED]`（来自 `report_violation`）才意味着调用确实被拒绝了（要么是无条件命中禁止路径，要么是用户随后在对话框中回答了否）。

**常见陷阱**

- **根本没有出现提示。** 检查目标是否已经获得授权（被动地或通过 `orca.request_permissions(...)` 持久保存在插件的 `.install_state.json` 附属文件中），或者是否被祖先级联覆盖——两者都是按设计静默放行，并不是缺陷。
- **加载期间、插件可用之前出现了提示。** 那是合并的 `orca.request_permissions(...)` 对话框。拒绝它会中止加载，原因会显示在插件的诊断选项卡中；批准请求或删除声明后即可再次加载。
- **提示仍然打开时，首次使用就被拒绝了。** 在非主线程上，提示会被异步发出，当前事件被拒绝（失败即关闭）。接受提示会持久保存授权，所以之后的尝试会成功；它不会追溯放行已被拒绝的那次调用。
- **没有上下文 = 没有强制检查。** 如果某个插件的调用从未受到审计，请检查它的实例是否调用过 `set_audit_plugin_key()`（键非空），以及该方法是否确实经过 `ORCA_PY_OVERRIDE_AUDITED` / `ORCA_PY_AUDIT_SCOPE()` 包装。
- **过时的 / 增量的编译。** `PyPluginTrampoline.hpp` 和 `PluginAuditManager.hpp` 被许多编译单元包含。仅修改头文件的改动在增量编译中可能不会传播；如果运行时行为与源代码不符，请对受影响的目标进行干净的重新编译。修改 `PluginAuditManager.cpp` 只需重新编译单个编译单元并重新链接。

## 测试

- `tests/slic3rutils/test_plugin_audit.cpp`——纯逻辑的覆盖测试，涵盖禁止文件名列表、禁止路径关键字列表，以及 `check_path_access`/`check_open`（允许的根目录、只读根目录和禁止情况），不依赖运行中的解释器，也不依赖 `audit_hook` 流程本身。
- `sandboxes/orca_audit_matrix_plugin_any.py`——一个手动的端到端测试夹具插件，每个类别一项功能（`Audit: fsread`、`Audit: fsreadwrite`、`Audit: fscreate`、`Audit: fsdelete`、`Audit: http`、`Audit: socket`、`Audit: processcreate`），外加一项全部运行的功能，可以从插件管理界面运行，在运行中的解释器上观察每个类别真实的提示、持久化和拒绝行为（包括 `open()` 以及上文所述的级联/持久化保证）。

## 关键文件

| 文件 | 职责 |
|---|---|
| `src/slic3r/plugin/PluginAuditManager.{hpp,cpp}` | 类别、目标、持久化、声明式 `request_permissions`、决策流程、`audit_hook`、`ScopedPluginAuditContext` |
| `src/slic3r/plugin/PyPluginTrampoline.hpp` | `ORCA_PY_AUDIT_SCOPE()` / `ORCA_PY_OVERRIDE_AUDITED`（审计上下文 + 回溯日志） |
| `src/slic3r/plugin/PythonPluginInterface.hpp` | 每个实例的审计身份 |
| `src/slic3r/plugin/PluginLoader.cpp` | 在加载 / 键迁移时标记审计键 |
| `src/slic3r/plugin/pluginTypes/*/*Trampoline.hpp` | 各插件类型的方法及其 `audit_setup` 回调 |
| `src/slic3r/plugin/PythonPluginBridge.cpp` | 绑定 `orca.request_permissions(...)`，在捕获插件期间收集声明，并在 `register_capabilities()` 之后统一询问一次 |
| `src/slic3r/plugin/PluginFsUtils.hpp` | `PluginPermissions` / `PluginInstallState`：附属文件的 `permissions` 分组（`fs_read`、`fs_readwrite`、`network_http`、`network_socket`、`process`、`threading`、`events`） |
| `src/slic3r/plugin/PythonInterpreter.cpp` | 在解释器初始化时安装一次钩子 |
