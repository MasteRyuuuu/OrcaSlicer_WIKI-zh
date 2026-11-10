# 如何下载 Pull Request 构建产物进行测试

在 [OrcaSlicer 仓库]({{L1}})中创建或更新 Pull Request（PR）时，GitHub Actions 会自动编译项目，并生成可供下载测试的构建产物（artifacts）。

> [!IMPORTANT]
> 测试 PR 构建产物之前，建议先[备份你的预设]({{L2}})。

1. 登录你的 GitHub 账号。
2. 打开你想测试的 Pull Request。
3. 切换到 PR 页面顶部的"Checks"选项卡。  
   {{I1}}
4. 在"Checks"选项卡中找到"Build all"部分。  
   {{I2}}
5. **向下滚动**，找到"Artifacts"部分。  
   {{I3}}
6. 单击产物名称或其下载按钮，下载包含构建产物的 ZIP 文件。
    - Windows：
        - `OrcaSlicer_Windows_[PR_NUMBER]_portable`：便携版，测试时**推荐**使用。
        - `OrcaSlicer_Windows_[PR_NUMBER]`：安装版，会覆盖已有的安装。
    - macOS：
        - `OrcaSlicer_Mac_universal_[PR_NUMBER]`：通用版 macOS DMG 文件。
    - Linux：
        - `OrcaSlicer-Linux-flatpak_[PR_NUMBER]_x86_64.flatpak`：x86_64 版 Flatpak。
        - `OrcaSlicer-Linux-flatpak_[PR_NUMBER]_aarch64.flatpak`：ARM64 版 Flatpak。
        - `OrcaSlicer_Linux_ubuntu_2404_[PR_NUMBER]`：Ubuntu 24.04 DEB 安装包。
7. 下载完成后，解压 ZIP 文件即可获得构建产物。

> [!TIP]
> 把这份指南分享给其他人吧！
>
> 短链接：
>
> ```css
> {{U1}}
> ```
>
> Markdown 链接：
>
> ```md
> [How to Download Pull Requests Artifacts for Testing]({{L3}})
> ```
