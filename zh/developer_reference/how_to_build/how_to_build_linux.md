# 在 Linux 上编译

在 Linux 上有两种编译方式：[使用 Docker]({{L1}})（推荐），或者在你的系统上[直接编译]({{L2}})。

{{T1}}

## 使用 Docker

如何使用 Docker 编译并运行 OrcaSlicer。

### Docker 所需依赖

- Docker
- Git

### Docker 编译步骤

{{C1}}

## 故障排除

`scripts/DockerRun.sh` 脚本中有几个被注释掉的选项，可以帮助解决常见问题。它们的作用如下：

- `xhost +local:docker`：如果遇到"Authorization required, but no authorization protocol specified"错误，请在执行 `scripts/DockerRun.sh` 之前在终端中运行这条命令。它授予 Docker 容器与你的 X 显示服务器交互的权限。
- `-h $HOSTNAME`：强制容器的主机名与你的工作站主机名一致。在某些网络配置中会有用。
- `-v /tmp/.X11-unix:/tmp/.X11-unix`：把 X11 Unix 套接字挂载到容器中，帮助解决 X 显示方面的问题。
- `--net=host`：使用主机的网络栈，有利于打印机 Wi-Fi 连接和 D-Bus 通信。
- `--ipc host`：解决某些 X 环境中因权限问题而无法与共享内存套接字通信的情况。
- `-u $USER`：以你工作站的用户名运行容器，有助于保持一致的文件权限。
- `-v $HOME:/home/$USER`：把你的主目录挂载到容器中，方便加载和保存文件。
- `-e DISPLAY=$DISPLAY`：把你的 X 显示编号传给容器，从而启用图形界面。
- `--privileged=true`：授予容器更高的权限，libGL 和 D-Bus 功能可能需要它。
- `-ti`：给容器附加一个 TTY，以便在命令行中与 OrcaSlicer 交互。
- `--rm`：容器退出后自动删除它，保持系统整洁。
- `orcaslicer $*`：把 `scripts/DockerRun.sh` 脚本收到的其他参数直接传给容器中的 OrcaSlicer 可执行文件。

根据需要取消这些选项的注释并使用它们，通常可以解决与显示授权、网络和文件权限相关的问题。

## Linux 编译

如何在 Linux 上编译 OrcaSlicer。

### 依赖

编译系统支持多个 Linux 发行版，包括 Ubuntu/Debian 和 Arch Linux。所提供的 shell 脚本会尽可能自动安装所有必需的依赖，不过有些依赖你可能需要手动安装。

> [!NOTE]
> 目前不支持 Fedora 和其他发行版，但你可以尝试安装下面列出的必需依赖后手动编译。

#### 各发行版通用的依赖

- autoconf / automake
- cmake
- curl / libcurl4-openssl-dev
- dbus-devel / libdbus-1-dev
- eglexternalplatform-dev / eglexternalplatform-devel
- extra-cmake-modules
- file
- gettext
- git
- gstreamer-devel / libgstreamerd-3-dev
- gtk3-devel / libgtk-3-dev
- libmspack-dev / libmspack-devel
- libsecret-devel / libsecret-1-dev
- libspnav-dev / libspnav-devel
- libssl-dev / openssl-devel
- libtool
- libudev-dev
- mesa-libGL-devel / libgl-dev
- ninja-build
- texinfo
- webkit2gtk-devel / libwebkit2gtk-4.0-dev 或 libwebkit2gtk-4.1-dev
- wget

#### 特定发行版的额外依赖

- **Ubuntu 22.x/23.x**：libfuse-dev、m4
- **Arch Linux**：mesa、wayland-protocols

### Linux 编译步骤

1. **安装系统依赖：**

    {{C2}}

2. **编译依赖库：**

    {{C3}}

3. **编译 OrcaSlicer 及测试：**

    {{C4}}

4. **构建 AppImage（可选）：**

    {{C5}}

5. **一键完成全部编译（推荐）：**

    {{C6}}

**其他编译选项：**

- `-b`：以调试模式编译（长期以来在运行时基本不可用；除非你打算修复失败的断言，否则请避免使用）
- `-c`：强制进行干净的编译
- `-C`：启用带 ANSI 颜色的编译输出（仅限 GNU/Clang）
- `-e`：编译 RelWithDebInfo（发布版 + 调试符号）
- `-j N`：编译时最多使用 N 个核心（适用于内存较少的系统）
- `-1`：编译时只使用一个核心
- `-l`：使用 Clang 而不是 GCC
- `-L`：使用 `ld.lld` 作为链接器（如果可用）
- `-p`：禁用预编译头（提高 ccache 命中率）
- `-r`：跳过内存和磁盘检查（适用于内存较少的系统）

**自定义编译器、编译参数和链接器：**

`--` 之后的所有内容都会原样传给依赖库（`-d`）和 OrcaSlicer（`-s`、`-t`）编译的 `cmake` 配置步骤，因此无需修改脚本就能设置任何 CMake 变量：

{{C7}}

这些参数位于 `cmake` 命令行的最后，所以会覆盖 `-l` 和 `-L` 的设置。它们也可以与 `-g` 一起使用，`-g` 会把它们转发到容器中。请把它们传给配置你想修改的那部分编译的调用：依赖库在 `-d` 运行中配置，OrcaSlicer 在 `-s` 或 `-t` 运行中配置。

环境变量 `DEPS_EXTRA_BUILD_ARGS` 和 `ORCA_EXTRA_BUILD_ARGS` 分别为依赖库和 OrcaSlicer 的编译添加以空白分隔的配置参数。它们无法携带包含空格的参数，也不会被转发到 `-g` 容器中，所以请优先使用 `--`。

> [!NOTE]
> CMake 只有在第一次配置编译目录时才会读取编译器和编译参数的设置。要在已有的编译中修改它们，请传入 `-c` 进行干净的编译，或者编辑 `build/CMakeCache.txt`。

> [!NOTE]
> 编译脚本会自动检测你的 Linux 发行版，并使用相应的包管理器（apt、pacman）安装依赖。

> [!TIP]
> 第一次编译时，先用 `./build_linux.sh -u` 安装依赖，然后用 `./build_linux.sh -dsti` 编译全部内容。

> [!TIP]
> 有些改动不会被普通的重新编译察觉，因为它们位于预编译的依赖库（`deps/`）中，而不在 OrcaSlicer 的源代码中。这种情况下，请重新编译受影响的依赖目标，而不是整个 `deps/` 目录树。
>
> 例如，修改 `wxInspector` 之后：
>
> ```bash
> cd ~/OrcaSlicer   # the repository root, where build_linux.sh lives
> cmake --build deps/build --target dep_wxInspector
> ./build_linux.sh -s
> ```
>
> 路径是相对路径，所以在其他任何位置运行都会失败，并报错 `.../deps/build is not a directory`。
>
> 这里不需要 `--config` 参数：依赖库使用单配置生成器进行配置，所以编译类型在配置时就已确定。调试版编译（`-b`）请使用 `deps/build-dbg`，RelWithDebInfo 编译（`-e`）请使用 `deps/build-dbginfo`。

> [!WARNING]
> 如果编译过程中遇到内存问题，请使用 `-j 1` 或 `-1` 限制并行编译，并使用 `-r` 跳过内存检查。
