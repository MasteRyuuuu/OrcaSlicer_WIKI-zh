# Clang-Tidy 检查

每个修改了 `src/` 或 `tests/` 下 C++ 代码的拉取请求，都会在 CI 中运行一次 `clang-tidy` 检查。目前它只检查一件事：文件是否为它使用的每个符号包含了对应的头文件，而不是依赖预编译头或其他头文件的包含。依赖这些的代码通常能正常编译，但一旦不使用预编译头编译，或者某个无关的头文件不再包含某些内容，编译就会失败。

`scripts/run_clang_tidy.sh`（Linux 和 macOS）和 `scripts\run_clang_tidy.ps1`（Windows）会在你的机器上运行同样的检查，这样你可以在推送之前修复它报告的问题。

{{T1}}

## 检查会报告什么

检查规则来自仓库根目录中的 `.clang-tidy`。检查只关注你的分支相对于 `main` 的改动：

- 在你新增或修改的行上，如果用到的某个符号的头文件没有被该文件包含，检查就会失败。你没有改动的行上的旧代码不受此约束。
- 你修改过的源文件必须能够在不使用预编译头的情况下单独编译。
- 你修改过的头文件会被单独编译，只有你的改动新增的错误才会导致失败。
- 如果你删除了某个 `#include`，所有用到它所提供内容的地方都会失败，包括你没有改动的行。

那些属于库的内部实现、而不是应当包含的头文件（例如 wxWidgets 的各平台头文件，或 Boost 和 oneTBB 的内部头文件），列在 `.clang-tidy` 的 `IgnoreHeaders` 中，永远不会被要求包含。

脚本也会检查尚未提交的改动，所以你可以在工作过程中运行它们。

## 开始之前

检查需要一个编译数据库，它来自对 OrcaSlicer 的配置，所以你需要为你的平台[编译好 OrcaSlicer 的依赖库]({{L1}})。脚本会配置一个单独的、不使用预编译头的 `build-tidy` 目录，不会动你平常的编译目录。它们不会编译 OrcaSlicer，所以运行一次只需要几分钟，而不是一次完整编译的时间。

它们还需要一些工具，以及与 CI 完全相同版本的 `clang-tidy`，该版本固定在 `scripts/clang_tidy_requirements.txt` 中。更新或更旧的 `clang-tidy` 可能报告不同的结果，所以脚本会把固定版本安装到 `build-tidy` 中的 Python 虚拟环境里，而不使用 `PATH` 中的版本。

缺少某样东西时，脚本会写明缺少什么，并询问是否安装。回答 `y` 就会运行安装命令。回答 `n`，或者在没有终端的情况下运行时，它会输出命令，让你自己运行。传入 `--yes`（Windows 上为 `-Yes`）可以不经询问直接安装。

## Linux

在仓库根目录中运行：

{{C1}}

它需要 `git`、带有 `venv` 的 `python3`、`cmake`、`ninja` 和 `clang`。即使你平常用 GCC 编译，它也会使用 clang，因为 CI 用的是 clang，而 GCC 的编译参数会改变 `clang-tidy` 看到的内容。要自行安装它们：

{{C2}}

依赖库应位于 `deps/build` 中，`./build_linux.sh -d` 会把它们放在那里。如果配置因缺少系统库而失败，请用 `./build_linux.sh -u` 安装。

## macOS

在仓库根目录中运行：

{{C3}}

它需要 `git`、`python3`、`cmake` 和 `ninja`，以及提供编译器的 Xcode 命令行工具。要自行安装它们：

{{C4}}

依赖库应位于 Apple 芯片上的 `deps/build/arm64` 或 Intel 上的 `deps/build/x86_64` 中，`./build_release_macos.sh -d -a <arch>` 会把它们放在那里。

## Windows

在 PowerShell 中，从仓库根目录运行：

{{C5}}

它需要 Git、Python 3，以及带有 C++ 工具的 Visual Studio，其中的 CMake 组件提供 CMake 和 Ninja。脚本会自行加载 Visual Studio 开发者环境，所以任何终端都可以。要自行安装它们：

{{C6}}

`--install-deps` 安装 CMake、Perl 和 Git，`--install-vs` 安装 Visual Studio 生成工具（Build Tools）；两者都参见[在 Windows 上编译]({{L2}})。安装后请打开一个新终端，让 `PATH` 生效。

脚本使用 `build_win.bat -d` 生成的依赖库目录树：MSVC 为 `deps\build`，clang-cl 为 `deps\build-clang`，ARM64 上再加上 `-arm64`。它会使用编译该目录树时所用的同一编译器进行配置。

## 选项

| Linux、macOS | Windows | 作用 |
|---|---|---|
| `--fix` | `-Fix` | 添加 `clang-tidy` 指出的缺失 include。 |
| `-b`、`--base <rev>` | `-Base <rev>` | 与另一个修订版本比较。默认情况下，脚本与指向 `OrcaSlicer/OrcaSlicer` 的远程仓库的 `main` 比较，并会先获取它，所以在复刻仓库中也能使用。 |
| `--no-fetch` | `-NoFetch` | 不先获取 `main`。 |
| `-B`、`--build-dir <dir>` | `-BuildDir <dir>` | 使用 `build-tidy` 以外的编译目录。 |
| `-d`、`--deps-dir <dir>` | `-DepsDir <dir>` | 使用在其他位置编译的依赖库。 |
| `-j`、`--jobs <n>` | `-Jobs <n>` | 限制同时检查的文件数。 |
| `-y`、`--yes` | `-Yes` | 不经询问直接安装缺少的工具。 |
| | `-Arch <x64\|arm64>` | 针对本机以外的架构进行检查。 |

设置环境变量 `CLANG_TIDY` 可以使用你自己安装的 `clang-tidy`；如果它不是固定的版本，脚本会发出警告。

## 修复报告的问题

每条结果都会写明文件、行号、符号，以及提供该符号的头文件：

{{C7}}

添加它指出的 include，或者用 `--fix` 运行脚本一次性全部添加，然后在提交之前检查结果：

- `clang-tidy` 把每个头文件都写成尖括号形式。OrcaSlicer 自己的头文件使用引号，所以请写 `#include "libslic3r/Polygon.hpp"`，并修改 `--fix` 添加的那些。
- 把每个 include 和文件中的其他 include 放在一起，放在任何 `#if` 块之外，除非该符号只在某个块内使用。
- 在以 Windows 代码块（`_WIN32_WINNT`、`NOMINMAX`、`<Windows.h>`）开头的文件中，把新的 include 放在它下面。
- 如果它要求的是某个库的内部头文件，而不是你包含的那个，那么该头文件应当加入 `.clang-tidy` 的 `IgnoreHeaders` 中；请在你的拉取请求中说明这一点。

再次运行脚本，直到它报告 `clang-tidy passed.`。

## 与 CI 的一致程度

脚本运行的内容与 CI 任务相同：同样的 `clang-tidy` 版本、同样的配置选项、同样的 `.clang-tidy` 和同样的 `scripts/clang_tidy_diff.py`，并与 `main` 进行比较。在 Linux 上，如果你的分支与 `main` 保持同步，它报告的结果就与 CI 相同。

它可能在三个方面有所不同：

- CI 检查的是你的分支合并到最新 `main` 后的结果。如果自你创建分支以来 `main` 修改了相同的文件，请变基以看到相同的结果。
- CI 运行在 Linux 上。在 Windows 和 macOS 上，`clang-tidy` 还会看到 `_WIN32` 或 `__APPLE__` 块中的代码以及该平台的标准库，所以它可能报告 CI 不会报告的问题，也可能漏掉仅限 Linux 的代码中的问题。在你的平台和 Linux 上都通过的改动，就能通过 CI。
- 脚本还会检查尚未提交的改动，而 CI 永远看不到这些。

## 故障排除

- **配置失败**：会输出 CMake 输出的最后几行，完整日志位于 `build-tidy/configure.log`。在 Linux 上，缺少系统库通常意味着还没有运行 `./build_linux.sh -u`。依赖库路径错误可以用 `--deps-dir` 修正。
- **无法创建 Python 虚拟环境**：在 Debian 和 Ubuntu 上，`venv` 是一个单独的软件包，名为 `python3-venv`。
- **警告 `clang-tidy` 不是固定的版本**：`CLANG_TIDY` 指向了另一个版本。取消设置它即可使用固定的版本。
- **`No changed C++ lines to check.`**：你的分支相对于 `main` 在 `src/` 或 `tests/` 下没有 C++ 改动。
- **出现大量无关的结果**：你很可能在与旧的 `main` 比较。让脚本获取最新的 `main`，或者进行变基。
