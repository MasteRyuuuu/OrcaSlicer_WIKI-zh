# 在 Windows 上编译

为 64 位 Windows 编译 OrcaSlicer。`build_win.bat` 会安装前置工具，并编译依赖库和切片软件本身。默认工具链是 MSVC，也支持以 clang-cl（LLVM）作为替代。

{{T1}}

## 所需工具

> [!TIP]
> 克隆仓库后，`build_win.bat --install-vs ide` 会安装下面所有工具。参见[编译脚本]({{L1}})。

- [Visual Studio]({{L2}}) 2026、2022，或 2019 16.8 及更新版本，并安装*使用 C++ 的桌面开发*（Desktop development with C++）工作负载

    {{C1}}

- [CMake]({{L3}})

    {{C2}}

- [Strawberry Perl]({{L4}})

    {{C3}}

- [Git]({{L5}})

    {{C4}}

> [!IMPORTANT]
> 直接用 `winget install` 安装 Visual Studio 只会装上 IDE，而没有任何 C++ 编译器，之后编译会因为 CMake 找不到 Visual Studio 实例而失败。上面的 `--override` 参数会添加所需的*使用 C++ 的桌面开发*工作负载。
>
> 如果 Visual Studio 已经安装但没有这个工作负载，请在 **Visual Studio Installer** -> **修改（Modify）** 中勾选*使用 C++ 的桌面开发*，然后点击**修改（Modify）**添加它。

> [!IMPORTANT]
> Strawberry Perl 自带一份 CMake。如果它在 `PATH` 中排在前面，`cmake --version` 报告的就是这份副本，而不是你安装的那个。运行 `where cmake` 列出生效的副本，然后在**系统环境变量** > **Path** 中调整顺序，让真正的 CMake 排在前面：
>
> ```text
> C:\Program Files\CMake\bin
> C:\Strawberry\c\bin
> ```
>
> OrcaSlicer 需要 CMake 3.13 或更新版本，使用下文的 clang-cl 预设则需要 3.21 或更新版本。CMake 4.x 也可以。`build_win.bat` 在自己运行时会跳过 Strawberry 的副本，所以这只影响直接调用的 CMake。

{{I1}}

{{I2}}

> [!TIP]
> [GitHub Desktop]({{L6}}) 是可选的，它提供一个管理仓库和分支的图形界面：
>
> ```pwsh
> winget install --id=GitHub.GitHubDesktop -e
> ```

## 硬件要求

- 至少 16 GB 内存
- 至少 23 GB 可用磁盘空间
- 64 位 CPU
- 64 位 Windows 10 或更高版本

## 获取源代码

用 GitHub Desktop 或在命令行中克隆仓库：

{{C5}}

下面的步骤都不需要开发者命令提示符。进入克隆的目录：

{{C6}}

## 编译脚本

仓库根目录下的 `build_win.bat` 负责编译依赖库和切片软件。它可以在任何 shell、任何目录中运行，并会自行设置 Visual Studio 环境。

它会安装上面列出的工具（包括 Visual Studio），以及编译真正需要的组件：

{{C7}}

如果只需要不带 IDE 的生成工具（Build Tools），请用 `buildtools` 代替 `ide`；加上 `-l` 则会包含 clang 工具集。安装完成后请重启 shell，让新的 `PATH` 生效。`build_win.bat -u` 只安装 CMake、Perl 和 Git。

`build_win.bat --help` 会列出所有选项。最常用的几个：

| 选项 | 作用 |
| --- | --- |
| `-d`、`-s` | 编译依赖库、编译切片软件。`-ds` 两者都编译。 |
| `--config <name>` | `release`（默认）、`debug`、`relwithdebinfo` 或 `minsizerel` |
| `-l`、`-x` | 使用 clang-cl 编译，使用 Ninja Multi-Config 生成 |
| `--tests` | 与切片软件一起编译单元测试 |
| `--run-tests` | 编译并运行单元测试 |
| `--slicer-target <name>` | 只编译一个目标，而不是全部 |
| `--no-configure` | 只有源代码改动时，跳过配置步骤 |
| `--no-gettext` | 跳过重新生成翻译 |
| `-j <n>` | 限制并行编译器的数量 |
| `-c` | 删除本次运行将要编译的目录 |
| `--cache <tool>` | 通过[编译器缓存]({{L7}})编译，需要配合 `-l -x` |
| `-D` | 只输出每条命令而不执行 |

编译目录以生成它的配置、编译器和架构命名，所以改变三者中的任何一个都会配置一个新目录，而不会复用以其他方式编译的目录：

| 编译 | 切片软件目录 | 依赖库目录 |
| --- | --- | --- |
| MSVC，Release | `build\` | `deps\build\` |
| MSVC，Debug | `build-dbg\` | `deps\build-dbg\` |
| MSVC，RelWithDebInfo | `build-dbginfo\` | `deps\build\` |
| clang-cl，Release | `build-clang\` | `deps\build-clang\` |

`--arch arm64` 会在两个名称后都加上 `-arm64`。`--build-dir` 和 `--deps-dir` 可以分别覆盖它们，这样一次编译就可以与另一个检出目录共用依赖库。每次运行结束时都会输出一段信息，列出它生成了什么，以及接下来可以执行的命令。

## 编译依赖库

每次编译切片软件都要链接一套与之匹配的依赖库，每套依赖库只需编译一次。先编译发布版的一套：

{{C8}}

它会安装到 `deps\build\OrcaSlicer_dep\usr\local`。

调试版链接的是调试版 C 运行时（`/MDd`），不能与发布版运行时混用，所以需要单独的一套：

{{C9}}

它们安装到 `deps\build-dbg\`，无论使用哪种工具链，Debug 编译都需要它们。Release、RelWithDebInfo 和 MinSizeRel 都链接发布版的那一套。

> [!TIP]
> clang-cl 以 MSVC ABI 为目标，所以它链接的是 MSVC 的依赖库。`-d -l -x` 会在 `deps\build-clang\` 中再编译一份。把 `--deps-dir` 指向已有的 MSVC 依赖库目录，就可以跳过这次编译：
>
> ```pwsh
> build_win.bat -s -l -x --deps-dir C:\path\to\OrcaSlicer\deps\build
> ```

## 使用 MSVC 编译

使用 Visual Studio 生成器的 MSVC 是默认方式，也是 CI 使用的工具链。

1. 编译 OrcaSlicer：

    {{C10}}

2. 打开生成的解决方案。编译结束时输出的那段信息会写明它的名称：

    {{C11}}

    Visual Studio 2026 生成的是 `OrcaSlicer.slnx`，更早的版本生成的是 `OrcaSlicer.sln`。

3. 把编译配置设为 `Release`，然后运行**本地 Windows 调试器**（Local Windows Debugger）。

    {{I3}}

4. 可执行文件写入到：

    {{C12}}

如果要进行 Debug 编译，请先编译调试版依赖库，然后：

{{C13}}

这会生成 `build-dbg\src\Debug\orca-slicer.exe`，并且能自行找到 `deps\build-dbg`，因为两个目录都以配置命名。

`build_win.bat -s --run-tests` 会编译并运行测试套件。更多内容参见[如何测试]({{L8}})。

> [!NOTE]
> 任何分支的第一次编译都很慢。之后，修改 `.cpp` 文件编译很快，修改 `.hpp` 文件则耗时更长，具体取决于该头文件被包含的范围有多广。来回切换分支也会迫使进行长时间的重新编译，即使其他什么都没有改变。

## 使用 clang-cl 编译

OrcaSlicer 也可以使用 **clang-cl（LLVM）** 工具链和 **Ninja** 生成器编译。在同一台机器上，它编译项目的速度比 MSVC 快得多，这是使用它的主要理由。官方版本和 CI 使用的是 MSVC，所以改动仍然必须能在 MSVC 下编译。

`build_win.bat -l -x` 只需要下面列出的工具；参见[命令行]({{L9}})。之后介绍的预设文件，用于在 Visual Studio 或 VS Code 中编译和调试。

### 额外工具

除了*使用 C++ 的桌面开发*工作负载之外，clang-cl 还需要 clang 工具集。`build_win.bat` 会安装它：

{{C14}}

这会添加 **C++ Clang Compiler for Windows**（适用于 Windows 的 C++ Clang 编译器）组件，把 `clang-cl.exe` 和 `lld-link.exe` 放到 `VC\Tools\Llvm\x64\bin` 下。如果想手动添加，请在 **Visual Studio Installer** -> **修改（Modify）** -> **单个组件（Individual components）** 中搜索 *Clang*。

Ninja 随 Visual Studio 一起提供，`build_win.bat` 能找到这份副本。VS Code 和单独运行的 `cmake --preset` 则需要 `PATH` 中有它们自己的 Ninja：

{{C15}}

> [!NOTE]
> 另一个组件 **MSBuild support for LLVM (clang-cl) toolset**（`Microsoft.VisualStudio.Component.VC.Llvm.ClangToolset`）通过 Visual Studio 生成器驱动 clang-cl，即不带 `-x` 的 `build_win.bat -l` 所用的方式。下面的 Ninja 设置不使用它。

### 预设文件

Visual Studio、VS Code 和 `cmake --preset` 都读取同一个 CMake 预设文件。在仓库根目录中创建 `CMakeUserPresets.json`：

{{C16}}

`x64-clang` 使用 Ninja Multi-Config，所以一个编译目录同时容纳 Release、RelWithDebInfo 和 MinSizeRel。在它们之间切换无需重新配置。`x64-clang-debug` 是单独的，因为它链接的是 Debug 依赖库。

两个预设都没有设置 `CMAKE_PREFIX_PATH`。CMake 根据编译目录的**名称**推导出依赖库目录，所以 `build-clang` 会找到 `deps\build-clang`，`build-dbg-clang` 会找到 `deps\build-dbg-clang`。这正是 `build_win.bat -l -x` 使用的名称，所以预设和脚本共用编译目录，谁也不会重新配置对方编译好的内容。

四种配置都带有调试符号，因为 `SLIC3R_MSVC_PDB` 默认会给每个 MSVC 编译加上 `/Zi`。让 Release 和 MinSizeRel 难以单步调试的是优化：会出现内联的帧和调试器无法显示的变量，所以需要调试时请切换到 RelWithDebInfo。

> [!TIP]
> `BUILD_TESTS` 为 `ON`，这样测试套件会与应用程序一起编译，测试预设也可以运行它们。如果不需要，把它设为 `OFF` 可以让编译稍快一些。参见[如何测试]({{L10}})。

> [!TIP]
> 在 `cacheVariables` 中再加四项，就可以通过编译器缓存来编译这些预设，让 IDE 和 `build_win.bat` 复用彼此的工作成果。参见[编译器缓存]({{L11}})。

> [!TIP]
> 在 Ninja 1.12 或更新版本上，把 `NINJA_STATUS` 改为 `"[%f/%t %p :: %w / %W] "`，会在每一行加上已用时间和预计剩余时间：
>
> ```text
> [119/760  15% :: 00:07 / 07:23] Building CXX object src\libslic3r\CMakeFiles\libslic3r.dir\RelWithDebInfo\Fill\FillBase.cpp.obj
> ```

### Visual Studio

1. 以 CMake 项目的方式打开仓库：**文件 > 打开 > 文件夹**（File > Open > Folder）。不要打开 `build\OrcaSlicer.slnx`，那是 MSVC 的解决方案。
2. 在**配置**（Configuration）下拉列表中选择一个编译预设，例如 `x64-clang-release`。Visual Studio 把这个下拉列表标为"配置"，但其中的条目其实是编译预设，每个条目同时指定了一个配置预设和一种配置，所以只需要设置这一项。
3. 把启动项设为路径与该预设对应的那个 `orca-slicer.exe` 条目，对于 `x64-clang-release` 是 `src\Release\orca-slicer.exe`。Visual Studio 默认会选另一个可执行文件，之后会记住你的选择。不要选择任何一个 `(Install)` 条目。
4. 用**生成 > 全部生成**（Build > Build All）编译。可执行文件写入该预设的编译目录下，所以 `x64-clang-release` 会得到：

    {{C17}}

5. 测试编译完成后，用**测试 > 为 OrcaSlicer 运行 CTest**（Test > Run CTests for OrcaSlicer）运行它们。

> [!NOTE]
> `x64-clang-debug-build` 使用单配置生成器，所以没有按配置划分的子目录。它的启动项是 `src\orca-slicer.exe`，可执行文件位于 `build-dbg-clang\src\orca-slicer.exe`。

> [!NOTE]
> 第一次编译时，即使编译成功、应用也能运行，Visual Studio 仍可能弹出*生成失败*（Build failed）的提示。选择继续会正常启动，之后的编译也不会再提示。请查看**输出**（Output）窗格，而不是这个对话框。真正的失败会写明某个文件，而配置步骤失败也会弹出同样的对话框。

### VS Code

需要 **CMake Tools** 扩展（`ms-vscode.cmake-tools`）。一旦存在 `CMakeUserPresets.json`，它会自动切换到预设模式，所以无需任何配置。

从活动栏打开 **CMake** 面板，设置 **Project Status** 下的各项：

- **Configure** 设为 `x64 Clang`
- **Build** 设为你想要的配置，例如 `x64-clang-release`
- **Test** 设为 `x64-clang-test-release`
- **Launch** 和 **Debug** 设为 `OrcaSlicer_app_gui`，两者默认都是 `all`。请选择 `src\Release\` 下的条目，而不是 `OrcaSlicer_app_gui (Install)`

编译预设携带配置信息，所以在 Release、RelWithDebInfo 和 MinSizeRel 之间切换，就是切换编译预设。命令面板中的 **CMake: Select Configure Preset** 和 **CMake: Select Build Preset** 提供同样的选项。

该面板中的 **Launch** 和 **Debug** 条目会直接运行所选目标。如果想改用 `F5` 调试，请在 `.vscode/launch.json` 中添加一个启动配置：

{{C18}}

`cppvsdbg` 是 Windows 调试器，可以读取 clang-cl 生成的 PDB。`${command:cmake...}` 的值会跟随当前的启动目标和编译预设，所以没有写死任何内容。`cwd` 让应用程序在它所需的 `resources` 目录联接旁边启动。

> [!IMPORTANT]
> 没有这个配置时，**Run > Start Debugging** 会提出为你生成一个，并推荐 **C++ (GDB/LLDB)**，它面向的是 MinGW 和 LLDB。它写出的模板只调试单个源文件，并会报错 *Variable ${fileDirname} can not be resolved*。

### 命令行

`build_win.bat -l -x` 无需预设文件就能用 clang-cl 和 Ninja 编译，可以在任何 shell 中运行，也不需要开发者命令提示符：

{{C19}}

它会编译 `deps\build-clang\` 和 `build-clang\`，并生成：

{{C20}}

如果想改为通过预设编译，请在 **x64 Native Tools Command Prompt for VS** 中运行，它会把 `clang-cl`、`lld-link` 和 Windows SDK 加入 `PATH`：

{{C21}}

可执行文件写入到：

{{C22}}

## 故障排除

### 依赖库

> [!TIP]
> 有些改动不会被重新编译察觉，因为它们位于预编译的依赖库中，而不在 OrcaSlicer 的源代码中。请单独重新编译受影响的依赖库，而不是 `deps/` 下的全部内容。
>
> 例如，修改 `wxInspector` 之后：
>
> ```pwsh
> build_win.bat -d -t dep_wxInspector
> ```
>
> 依赖库的那一套取决于你的工具链参数，所以要重新编译 `deps\build-clang` 中的那一套，请加上 `-l -x`。然后重新编译切片软件，让更新后的依赖库链接进去。

> [!TIP]
> 依赖库编译以 `patch does not apply` 失败，说明它被打了两次补丁，而 `git apply` 无法把补丁应用到已经包含它的源代码上。请从头重新编译这一套：
>
> ```pwsh
> build_win.bat -d -c
> ```
>
> `-c` 会删除本次运行将要编译的目录，所以它清除的是与你的 `--config` 和工具链参数相对应的那个目录。

> [!TIP]
> 失败的运行最后会写明出错的命令，并建议针对失败的阶段使用 `-c` 重试。如果要丢弃依赖库和切片软件、从头开始：
>
> ```pwsh
> build_win.bat -ds -c
> ```

> [!TIP]
> 如果编译在配置 ZLIB 时失败，请从你的 Vcpkg 库中卸载 ZLIB。

### Windows SDK

> [!TIP]
> 如果对象的右键菜单中没有*修复模型*选项，说明编译没有用上 Windows SDK。修复方法：
>
> 1. 在 Windows SDK 安装目录中找到 `winrt` 文件夹，例如：
>
>    ```pwsh
>    C:\Program Files (x86)\Windows Kits\10\Include\10.0.26100.0\winrt
>    ```
>
>    确切的路径因 Windows SDK 版本而异。
>
> 2. 打开 **libslic3r_gui** 项目属性，进入 **配置属性 > C/C++ > 预处理器 > 预处理器定义**（Configuration Properties > C/C++ > Preprocessor > Preprocessor Definitions）。添加 `HAS_WIN10SDK`。
>
> 3. 打开 **OrcaSlicer_app_gui** 项目属性，进入 **配置属性 > C/C++ > 常规 > 附加包含目录**（Configuration Properties > C/C++ > General > Additional Include Directories）。添加第 1 步中 `winrt` 文件夹的路径。
>
> 4. 生成解决方案。

### clang-cl

> [!TIP]
> clang-cl 编译出现异常时，先检查它用的是哪个编译器。`build_win.bat` 会在编译开始之前输出：
>
> ```text
> Compiler: C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/Llvm/x64/bin/clang-cl.exe
> ```
>
> 除非 `--clang-path` 另有指定，否则用的就是 Visual Studio 中的那一个，所以不会意外用上独立安装的 LLVM。
>
> 预设的情况则不同。它们通过 `PATH` 解析不带路径的 `clang-cl`，而开发者命令提示符会把 Visual Studio 的 LLVM 目录追加到 `PATH` 的*末尾*，所以像 `C:\Program Files\LLVM\bin` 这样的安装会优先。旧版本会在编译任何内容之前就未能通过编译器检查：
>
> ```text
> -- The C compiler identification is Clang 11.0.0 with MSVC-like command-line
> -- Check for working C compiler: C:/Program Files/LLVM/bin/clang-cl.exe - broken
> lld-link: error: undefined symbol: __guard_eh_cont_table
> ```
>
> 运行 `where clang-cl` 列出生效的副本。然后要么在**系统环境变量** > **Path** 中把 Visual Studio 的目录放到前面，要么把预设 `environment` 块中不带路径的 `clang-cl` 换成完整路径。

> [!TIP]
> 由较旧的检出版本编译的依赖库，在 clang-cl 下会以两种方式失败。
>
> **TBB** 是用 `/GL` 编译的，而 `lld-link` 拒绝 LTCG 目标文件。这个问题出现得很晚，在 `Linking CXX shared library src\OrcaSlicer.dll` 这一步，表现为每个目标文件一条错误，并且不带文件名或行号：
>
> ```text
> lld-link: error: tbb.dir\Release\queuing_rw_mutex.obj: is not a native COFF file. Recompile without /GL?
> ```
>
> **wxWidgets** 把它的库安装在 `vc_x64_lib` 下，但当编译器是 clang-cl 时，它自己的 CMake 配置文件会去找 `clang_x64_lib` 目录。这会在配置时失败，报出 `include could not find requested file` 错误，并写明 `clang_x64_lib/wxWidgetsTargets.cmake`。
>
> 从头重新编译 clang 依赖库可以同时解决这两个问题：
>
> ```pwsh
> build_win.bat -d -l -x -c
> ```
>
> 如果只想重新编译 TBB，请先删除 `deps\build-clang\dep_TBB-prefix`，让它的时间戳文件一并删除，然后只指定这一个目标：
>
> ```pwsh
> build_win.bat -d -l -x -t dep_TBB
> ```
