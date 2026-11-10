# 如何测试

本 wiki 页面介绍如何在 Windows、macOS 和 Linux 上编译和运行测试，以及如何添加测试。测试使用 [Catch2]({{L1}}) v3。它的[文档]({{L2}})介绍了断言和各种宏，主仓库中的 `tests/CATCH2.md` 则说明了 OrcaSlicer 如何使用它们。

默认不编译测试。在任何平台上都需要显式要求编译测试，这会设置 CMake 选项 `BUILD_TESTS`。

{{T1}}

## Windows

### 在 Windows 上编译测试

给编译脚本传入 `--tests`：

{{C1}}

它会把 `-DBUILD_TESTS=ON` 传给 CMake。`-l -x` 会改用 clang-cl 和 Ninja Multi-Config 编译测试，而不是 MSVC 和 Visual Studio。

编译目录以配置、编译器和架构命名，所以 MSVC 下 Release 为 `build`，clang-cl 下为 `build-clang`。完整的命名规则参见[在 Windows 上编译]({{L3}})。

### 在 Windows 上更快地重新编译

第一次编译之后，可以只重新编译一个测试套件，而不是全部：

{{C2}}

只有源代码改动时，加上 `--no-configure` 可以跳过配置步骤。在 Visual Studio 中打开生成的解决方案并编译测试项目也可以。

### 在 Windows 上运行测试

`--run-tests` 会编译并运行测试套件：

{{C3}}

运行结束时会输出该编译目录对应的 `ctest` 命令行，这样你无需重新编译就可以再次运行。Visual Studio 和 Ninja Multi-Config 都是多配置生成器，所以 `ctest` 需要 `-C` 才知道你指的是哪种配置。不加它会提示找不到任何测试。

{{C4}}

要运行特定的一组，请指向它的目录：

{{C5}}

可执行文件位于编译目录中的 `tests/<suite>/<config>/`。直接运行它，是使用 Catch2 自身过滤功能最简单的方式：

{{C6}}

## macOS

### 在 macOS 上编译测试

给编译脚本传入 `-T`，并指定你要编译的架构：

{{C7}}

`-T` 会编译测试，然后运行它们。设置 `ORCA_TESTS_BUILD_ONLY=1` 可以只编译而不运行。`-s` 跳过依赖库的编译；如果你想要 Release 以外的配置，用 `-c` 选择。

编译目录是 `build/<arch>`，即 `build/arm64` 或 `build/x86_64`，测试位于其下的 `build/<arch>/tests` 中。

### 在 macOS 上更快地重新编译

针对已有的编译目录重新编译一个测试套件：

{{C8}}

给编译脚本传入 `-b`，可以在不重新配置 CMake 的情况下重新编译。

### 在 macOS 上运行测试

默认生成器是 Xcode，它是多配置生成器，所以 `ctest` 需要 `-C` 才知道你指的是哪种配置。如果你更想用 Ninja Multi-Config，请在编译时加上 `-x`。

{{C9}}

要运行特定的一组，请指向它的目录：

{{C10}}

可执行文件位于 `tests/<suite>/<config>/`。直接运行它，是使用 Catch2 自身过滤功能最简单的方式：

{{C11}}

## Linux

### 在 Linux 上编译测试

给编译脚本传入 `-t`：

{{C12}}

（或 `-ter`、`-stb` 等）。

用 `-t` 运行 `build_linux.sh` 时，如果你编译二进制文件时用了 `-e` 或 `-b` 参数，请务必同样加上，否则在测试准备好之前，你会把整个 OrcaSlicer 重新编译一遍。

之后测试二进制文件会出现在 `build/tests`、`build-dbginfo/tests` 或 `build-dbg/tests` 下。

### 在 Linux 上更快地重新编译

`build_linux.sh` 用一条 cmake 命令编译测试，你也可以针对已有的编译目录自己运行同一条命令：

{{C13}}

目录和配置是配套的：`build` 对应 `Release`，`build-dbginfo` 对应 `RelWithDebInfo`，`build-dbg` 对应 `Debug`。

如果只需要一个测试套件，就让 `--target` 指向它：

{{C14}}

`CMakeLists.txt` 改变时，Ninja 会自己重新运行 CMake，所以添加新的源文件不需要单独的配置步骤。

### 在 Linux 上运行测试

{{C15}}

要运行特定的一组，请指向它的目录：

{{C16}}

可执行文件位于 `tests/<suite>/<config>/`。直接运行它，是使用 Catch2 自身过滤功能最简单的方式：

{{C17}}

## 测试套件

每个测试套件编译出自己的可执行文件，并覆盖代码库的不同部分。

| 套件 | 可执行文件 | 覆盖范围 |
|---|---|---|
| `libslic3r` | `libslic3r_tests` | 核心库：几何、网格、文件格式、配置和预设、Clipper、算法和数据结构 |
| `fff_print` | `fff_print_tests` | FFF 切片流水线，从 `Model` 加配置开始，经过 `Print` 和 `PrintObject`，直到输出 G-code |
| `sla_print` | `sla_print_tests` | SLA 打印：支撑树和底座几何、支撑点生成、光线投射 |
| `libnest2d` | `libnest2d_tests` | 使用无拟合多边形的二维排样和装箱 |
| `slic3rutils` | `slic3rutils_tests` | Python 插件系统、它的切片流水线绑定，以及设备和网络工具 |
| `filament_group` | `filament_group_tests` | 耗材丝到挤出机的分组，与基准结果对照检查 |

有几处特殊之处。`sla_print` 把文件命名为 `sla_<subsystem>_tests.cpp` 而不是 `test_<subsystem>.cpp`，并且有自己的入口点。在 `libslic3r` 中，`test_hollowing` 只有在有 OpenVDB 时才会编译，`test_png_io` 在 `CMakeLists.txt` 中被注释掉了。而 `tests/compare_analyzer/` 根本不是测试套件，它是用于比较不同版本或不同切片软件之间 `.3mf` 输出的 Python 工具。

`filament_group` 与其 `golden/` 目录中的基准文件进行比较。如果你有意修改了分组逻辑，请重新生成基准文件，并把差异连同其余改动一起审查。否则，基准比较失败就意味着出现了回归。

## 测试放在哪里

根据测试所检验的生产代码来选择测试套件，而不是根据测试的写法。

人们最常弄错的是 `libslic3r` 和 `fff_print` 的划分。如果行为取决于打印设置，或者会产生或使用 G-code 或切片状态，它就属于 `fff_print`。如果它是类本身的属性，在不涉及 `Print` 的情况下也成立，它就属于 `libslic3r`。所以网格变换、`Model` 构造检查或挤出几何测试都放在 `libslic3r` 中，尽管由于历史原因，有少数这类测试位于 `fff_print` 中。

同样的规则也决定了套件内部的文件。每个子系统一个文件，命名为 `test_<subsystem>.cpp`，该子系统的所有测试都归它所有，无论测试读取的是内存中的状态还是生成的输出。子系统通常是一个类，但也可以是分布在多个文件中的一项功能。如果你改动了某个子系统，你的测试就放在它的文件中。如果还没有这个文件，就添加 `test_<subsystem>.cpp`，并在该套件的 `CMakeLists.txt` 中列出它。

## 测试辅助工具

在自己编写准备代码或 G-code 解析之前，先检查是否已有现成的辅助工具。

`tests/test_utils.hpp` 由所有测试套件共用。它提供 `load_model()`，用于从 `tests/data/` 中取出网格，以及 `ScopedTemporaryFile`，提供会自行清理的临时路径。当你需要 `load_model()` 没有涵盖的测试夹具时，`TEST_DATA_DIR` 宏会给出同一个目录。

大多数测试套件在此基础上还有自己的本地辅助代码：

- `fff_print/test_helpers.hpp` 功能最多。它构建并切片一个 `Print`，并解析生成的 G-code。
- `sla_print/sla_test_utils.hpp` 构建 SLA 场景，并检查生成的支撑和底座几何。
- `libnest2d/libnest2d_test_utils.hpp` 包含排样辅助函数。它的 `printer_parts.cpp` 中有测试夹具几何，`libslic3r` 的摆放测试也会借用。
- `slic3rutils/plugin_test_utils.hpp` 支撑插件测试，`filament_group/fg_test_utils.hpp` 构建分组用例。

`libslic3r` 没有本地辅助代码，只使用共用的头文件。

## 编写测试

一个完整的测试如下：

{{C18}}

把它保存为所属套件中的 `test_<subsystem>.cpp`，在该套件的 `CMakeLists.txt` 中列出它，然后按上文的方法编译和运行。

### 命名与标签

用一个描述行为的普通句子（一般现在时）给测试用例命名，而不要以子系统作为前缀：

{{C19}}

每个测试都带有一个子系统标签，指明它覆盖的内容，与其文件对应。这是唯一一个可以确定一定存在的标签，人们也用它来过滤。新标签请使用 PascalCase，尽管旧标签在这一点上并不统一。

在确实有用的地方添加更多标签：

- 更窄的标签可以把一个大文件切分成可单独运行的部分，例如几何测试中的 `[Rotcalip]` 或排样测试中的 `[Placer]`。
- 共用标签用于标记跨越多个文件的内容，例如 `[Python]`、`[H2C]` 或 `[Regression]`。
- `[NotWorking]` 标记因已知原因而禁用的测试，`[.]` 让测试在默认运行中隐藏。无论使用哪一个，都要在注释中说明原因。

Catch2 标签会注册为 CTest 标签，所以 `ctest -L` 和 `ctest -LE` 也可以按标签过滤。

### 测试风格

优先为每种行为写一个平铺的 `TEST_CASE`，参数化用例使用 `GENERATE`，共用的准备代码提取到辅助函数中。名称已经说明了行为，所以 BDD 的那套结构通常只是噪音。`SCENARIO` / `GIVEN` / `WHEN` / `THEN` 只留给确实有共用准备代码、并分支出几个相近变体的测试，并且不要让一个 `SCENARIO` 收集彼此无关的 `WHEN`。

### 测试设计

测试应当在它所命名的行为出错时失败，其他情况下则不应失败。这主要取决于你准备了什么、断言了什么。

**设置你所依赖的值。** 如果断言中的某个数字来自某个配置键，就设置这个键。否则测试同时也在测试默认值。

{{C20}}

**断言属性，而不是偶然的数字。** 字节数、坐标和挤出量会随着上游的任何重构而变化，而它们都不是测试名称所指的内容。

{{C21}}

**匹配你关心的那个标记。** 一整行 G-code 中带有速度、坐标和注释措辞，它们都与你的测试无关。

{{C22}}

**比较浮点数时使用容差。**

{{C23}}

**其他几点。**

- 测试之间不要保留共享状态。它们必须能在 `--order rand` 下通过，你可以把这个参数传给测试套件的二进制文件来检查。
- 只在顺序本身就是约定的地方依赖顺序，例如 `role_sequence`。
- 以回归测试所保护的行为来命名它，而不是以 issue 或 PR 编号命名，这样两年后它仍然有意义。

## 添加新的测试套件

创建 `tests/<suite>/`，其中包含一个 `<suite>_tests.cpp` 和一个 `CMakeLists.txt`。每个测试套件的结构都相同，所以最快的方法是复制最接近的那个：

{{C24}}

`_TEST_NAME` 取自目录名，`<suite>_tests` 目标的名称就来源于此。`orcaslicer_copy_test_dlls()` 在 Windows 上把运行时 DLL 放到可执行文件旁边，在其他平台上什么也不做。`orcaslicer_discover_tests()` 把每个 Catch2 用例注册到 CTest，并把标签转换为 CTest 标签，`ctest -L` 正是因此才能工作。

链接测试套件真正需要的内容，而不要盲目复制上面那一行。大多数套件链接 `libslic3r`，`libnest2d` 链接 `libnest2d`，`slic3rutils` 还会引入 `libslic3r_gui` 和 `pybind11::embed`。

然后在 `tests/CMakeLists.txt` 中注册该目录：

{{C25}}

如果某个源文件需要可选的依赖，请像 `test_hollowing` 那样只对这个源文件加条件，而不是整个测试套件：

{{C26}}
