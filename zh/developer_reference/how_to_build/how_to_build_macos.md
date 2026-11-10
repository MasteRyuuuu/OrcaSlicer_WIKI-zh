# 在 macOS 上编译

如何在 64 位 macOS 上使用 Xcode 编译。

{{T1}}

## 所需的 macOS 工具

- Xcode
- CMake
- Git
- gettext
- libtool
- automake
- autoconf
- texinfo
- pkgconf

> [!TIP]
> 其中大部分可以通过运行以下命令安装：
>
{{C1}}

> [!IMPORTANT]
> 如果你最近升级了 Xcode，请务必至少打开一次 Xcode，并安装所需的 macOS 编译支持。

让命令行工具指向你的 Xcode 安装，并接受许可协议：

{{C2}}

## macOS 编译步骤

1. 克隆仓库：

    {{C3}}

2. 编译应用程序：

    {{C4}}

    > [!TIP]
    > 如果你使用的是最新的 macOS 和 Xcode，请显式设置部署目标，让编译使用受支持的 SDK，例如：
    >
    > ```bash
    > ./build_release_macos.sh -s -t 15.4
    > ```

3. 打开应用程序：

    {{C5}}

## 在 Xcode 中调试

要直接在 Xcode 中编译和调试：

1. 打开 Xcode 项目：

    {{C6}}

2. 在菜单栏中：
    - **Product > Scheme > OrcaSlicer**
    - **Product > Scheme > Edit Scheme...**
        - 在 **Run > Info** 下，把 **Build Configuration** 设为 `RelWithDebInfo`
        - 在 **Run > Options** 下，取消勾选 **Allow debugging when browsing versions**
    - **Product > Run**
