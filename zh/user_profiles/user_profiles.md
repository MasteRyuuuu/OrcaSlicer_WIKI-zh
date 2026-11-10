# OrcaSlicer 用户配置

本页说明 OrcaSlicer 把你的用户配置和自定义预设存放在哪里、配置如何通过 OrcaCloud 同步，以及如何迁移现有的配置。

{{T1}}

## 存储位置

OrcaSlicer 把用户配置存放在应用程序的配置目录中。具体位置取决于你的操作系统：

| 操作系统 | 典型路径 |
|---|---|
| Windows | `%APPDATA%\OrcaSlicer` |
| macOS | `~/Library/Application Support/OrcaSlicer` |
| Linux（AppImage / 原生安装） | `~/.config/OrcaSlicer` |
| Linux（Flatpak） | `~/.var/app/com.orcaslicer.OrcaSlicer/config/OrcaSlicer` |

卸载或重新安装 OrcaSlicer **不会**删除这些配置，所以你的设置和自定义预设在更新之后仍会保留。

!!! info "卸载后配置仍会保留"
    卸载 OrcaSlicer——包括 **Microsoft Store** 版本——不会删除你的配置文件夹。
    `%APPDATA%\OrcaSlicer`（Windows）以及上面对应路径中的配置会被有意保留，
    这样重新安装后它们仍然存在，并继续与其他 OrcaSlicer 版本共用。如果要删除它们，
    请在卸载后手动删除该文件夹。

> [!WARNING]
> 在 macOS 上，卸载 OrcaSlicer 时可能会提示你删除配置目录。如果你确认，**你的所有用户配置都将永久丢失**。只有在确定不再需要这些配置时，才删除这个目录。

## 找到配置文件夹

你可以直接在 OrcaSlicer 中打开配置文件夹：

1. 在菜单栏中单击**帮助** > **打开配置文件夹**。

{{I1}}

## 用户配置文件夹

在配置文件夹中，你会找到一个名为 `user` 的子文件夹。这个文件夹包含你所有的自定义预设和用户配置。

{{I2}}

`user` 目录中可能包含以下一个或多个子文件夹：

### `default`

这是你**没有**登录任何云同步服务时 OrcaSlicer 使用的文件夹。如果你从未使用过配置同步，通常只会有这一个文件夹。

### `<UUID>`（OrcaCloud）

以 UUID 命名的文件夹（例如 `6b89c630-39bb-42cb-a1f0-476bef493c06`）。这个文件夹在你登录 **OrcaCloud**（2.4 及以后版本可用）时创建。登录后，OrcaSlicer 会自动从这个文件夹而不是 `default` 中保存和加载你的自定义预设。

> [!NOTE]
> **OrcaCloud 是免费的。** 配置同步和云端备份现在免费，今后也将保持免费；详情请参见 [Orca Cloud 常见问题]({{L1}})。

### `<10 位数字>`（Bambu Cloud）

以 10 位数字命名的文件夹（例如 `1509812367`）。这个文件夹由旧的 **Bambu Cloud** 配置同步功能使用。

> [!NOTE]
> 从 OrcaSlicer 2.4 开始，配置同步不再支持 Bambu Cloud，已由 OrcaCloud 取代。用于打印机通信的 Bambu Cloud 不受影响。

### OrcaSlicer 如何选择文件夹

- **已登录 OrcaCloud** → 使用 UUID 文件夹
- **未登录** → 使用 `default` 文件夹

切换登录状态会自动切换当前使用的文件夹，无需任何手动操作。

## OrcaCloud 自动迁移

从 2.4 版本开始，OrcaSlicer 提供自动迁移功能，帮助你过渡到 OrcaCloud。

当你**第一次**登录 OrcaCloud 时，OrcaSlicer 会自动把 `default` 或 Bambu Cloud 文件夹中的现有配置复制到新的、以 UUID 命名的文件夹中。也就是说，你的自定义预设会被保留并同步到云端，无需任何手动步骤。

> [!TIP]
> 迁移完成后，你可以访问 [cloud.orcaslicer.com]({{L2}}) 并登录账户，确认配置已经备份。

## 手动迁移

大多数情况下，自动迁移都能顺利完成。不过，如果登录 OrcaCloud 后你的配置没有出现，可以手动迁移：

1. 把旧配置文件夹（`default` 或 10 位数字的 Bambu Cloud 文件夹）中的内容复制到新的 UUID 文件夹中。
2. 重启 OrcaSlicer。
3. 等待 1–3 分钟，让 OrcaSlicer 检测到新的配置并将其同步到 OrcaCloud。

## 从 Bambu Cloud 更新后配置不见了

如果你之前使用 **Bambu Cloud** 同步配置，并且选择了**不**使用 OrcaCloud，那么更新后打开 OrcaSlicer 时，可能会发现自定义预设似乎不见了。这是停用 Bambu Cloud 同步带来的已知副作用——**你的配置并没有丢失。**

背后的情况是这样的：

- 你的配置仍然安全地保存在 Bambu Cloud 文件夹（以 10 位数字命名的那个）中。
- 由于不再支持 Bambu Cloud 同步，而你又没有登录 OrcaCloud，OrcaSlicer 现在从 `default` 文件夹加载和保存配置。
- 如果你一直只用 Bambu Cloud，那么 `default` 文件夹是空的，所以看起来好像所有配置都不见了。

你可以用下面任意一种方式找回配置。两种方式都可行——选择适合你的即可。

### 方法 1：在本地复制配置（无需账户）

如果你更愿意在不使用任何云账户的情况下继续工作，只需把配置移到 OrcaSlicer 现在使用的文件夹中：

1. 通过**帮助** > **打开配置文件夹**打开配置文件夹，然后打开 `user` 子文件夹。
2. 打开你的 Bambu Cloud 文件夹（10 位数字的那个），复制其中的**全部**内容。
3. 把它们粘贴到 `default` 文件夹中。
4. 重启 OrcaSlicer。

你的配置会重新出现，OrcaSlicer 之后会继续从本地的 `default` 文件夹加载和保存它们。

### 方法 2：登录 OrcaCloud（自动）

如果你还希望配置得到备份并在多台设备之间同步，登录 OrcaCloud 就会自动为你迁移。首次登录时，OrcaSlicer 会把配置从 Bambu Cloud 文件夹复制到新的 OrcaCloud 文件夹中。详情请参见 [OrcaCloud 自动迁移]({{L3}})。

> [!NOTE]
> 你可能会想，为什么 OrcaSlicer 不直接帮你把 Bambu Cloud 配置复制到 `default` 文件夹中。因为 `default` 文件夹只存在于你的电脑上，没有任何云端备份，自动写入它可能会无意中覆盖或混淆你已经存放在那里的配置。为了避免在你不知情的情况下改动本地数据，OrcaSlicer 不会动 `default` 文件夹，而是让你自己决定如何迁移。自动迁移只在你登录 OrcaCloud 时进行，因为那时目标文件夹是为你的账户全新创建的。
