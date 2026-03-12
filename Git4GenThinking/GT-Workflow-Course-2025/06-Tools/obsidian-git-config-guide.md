# Obsidian + GitLink (CCF) 协同操作指南

核心目标：利用 GitLink 作为云端仓库，配合 Obsidian Git 插件实现自动化备份与多端同步。

---

## **1. 准备工作

在开始之前，请确保你已准备好以下环境：

1. **本地环境**：

    - 已安装 **Git**（[下载地址](https://www.google.com/search?q=https://git-scm.com/downloads&authuser=1)）。
    - 已安装 **Obsidian**。

2. **云端账号**：

    - 注册并登录 [GitLink 确实开源](https://www.gitlink.org.cn/)。

3. **Obsidian 插件**：

    - 在 Obsidian 中安装并启用 **Obsidian Git** 社区插件。

---

## 2. 关键步骤一：在 GitLink 创建仓库与令牌

与 GitHub 不同，GitLink 的 HTTPS 推送通常需要**私人访问令牌 (Access Token)** 或设置专门的**HTTPS 密码**，而非登录密码。

### **2.1 创建云端仓库**

1. 登录 GitLink，点击右上角 **“+”** -> **“新建项目”**。
2. **项目名称**：建议命名为 `obsidian-brain` 或 `knowledge-base`。
3. **可见性**：**强烈建议选择“私有” (Private)**，保护你的个人笔记隐私。
4. **初始化**：不要勾选“使用 Readme 初始化”（保持仓库为空，方便后续推送）。
5. 点击“创建项目”，复制仓库的 **HTTPS 地址**（例如：`https://gitlink.org.cn/yourname/obsidian-brain.git`）。

### **2.2 获取 HTTPS 密码/令牌**

_注：GitLink 某些版本直接使用账号密码即可，但建议检查“个人设置”中的安全选项。_

1. 点击右上角头像 -> **“个人设置”**。
2. 找到 **“安全设置”** 或 **“HTTPS 密码”** / **“访问令牌 (Access Token)”**。
3. 如果设置了 HTTPS 密码，请记住它；如果是 Token，请生成并复制（权限选 `write_repository`）。

    - _提示：后续在 Obsidian 中输入密码时，使用这个 HTTPS 密码/Token，而非你的网页登录密码。_

---

## 3. 关键步骤二：将本地Vault连接到 GitLink

这里提供两种场景，请根据你的情况选择：

### 场景 A：你已经有一个本地Obsidian仓库

_(这是最常见的情况)_

1. **打开终端 (Terminal/CMD)**：

    - Windows 用户：在你的 Obsidian仓库文件夹内右键 -> "Open Git Bash here" 或在 CMD 中 `cd` 到该目录。

    - Mac 用户：打开终端，输入 `cd` (注意空格) 然后把文件夹拖进去。
    - Linux用户：打开终端，输入'cd'进入Obsidian仓库的目录。

2. **初始化 Git**：

    Bash

    ```
    git init
    git add.
    git commit -m "Initial commit from Obsidian"
    ```

3. **关联 GitLink 远程仓库**：

    - 将下面的 URL 替换为你刚才复制的 GitLink 仓库地址。


    Bash

    ```
    # 格式：git remote add origin <你的GitLink仓库地址>
    git remote add origin https://gitlink.org.cn/your_username/your_repo.git
    ```

4. **首次推送 (Push)**：

    Bash

    ```
    git push -u origin master
    ```

    - 此时会弹窗要求输入用户名和密码。
    - **Username**: 你的 GitLink 用户名。
    - **Password**: 你的 GitLink **HTTPS 密码** 或 **Token**。

### **场景 B：你是从零开始**

1. 直接在本地使用 `git clone` 命令克隆刚才创建的空仓库。
2. 将克隆下来的文件夹作为 Obsidian 的新 Vault 打开。

---

## 4. 关键步骤三：配置Obsidian Git插件

完成上述Git连接后，我们需要配置插件来实现“无感自动备份”。

1. 打开 Obsidian **设置 (Settings)** -> **Obsidian Git**。

2. **配置备份策略**：

    - **Vault backup interval (minutes)**: 设置自动备份间隔，建议 `30` 分钟。
    - **Auto backup after file change**: 开启。

3. **配置推送策略**：

    - **Push on backup**: **开启**（非常重要，否则只会提交到本地，不会上传到 GitLink）。
    - **Pull updates on startup**: 建议开启（如果你在多台电脑使用）。

4. **解决鉴权问题 (Authentication)**：

    - 如果之前的 `git push` 已经记住了密码（Windows Credential Manager 或 Mac Keychain），插件通常能直接工作。
    - 如果插件提示 `Authentication failed`，请在插件设置中找到 **Authentication** 部分，填入你的 GitLink 用户名和 HTTPS 密码/Token。

---

## **5. 进阶工作流：Obsidian Canvas 版本控制**

GitLink 对 Canvas 文件（本质是 `.canvas` 的 JSON 文件）支持良好。你可以在 GitLink 的网页端查看 Canvas 的差异（Diff），但这通常可读性较差。

**推荐操作习惯**：

1. **原子化提交**：在修改完一个重要的 Canvas 流程图后，手动触发一次备份（`Ctrl/Cmd + P` -> 输入 `Git: Create backup`）。

2. **提交信息**：在弹出的输入框中写明修改点，例如 `feat: 更新了Agent编排逻辑`。

3. **冲突避免**：Canvas 文件本质是复杂的 JSON，**极难解决合并冲突**。

    - **黄金法则**：避免在两台设备上同时编辑同一个 `.canvas` 文件。

    - 在切换设备前，务必确保 A 电脑已 Push，B 电脑已 Pull。


---

## **6. 常见问题排查 (Troubleshooting)**

|**问题现象**|**可能原因**|**解决方案**|
|---|---|---|
|**Push 失败：403 Forbidden**|密码错误或无权限|检查是否使用了正确的 **HTTPS 密码/Token** 而非登录密码；检查仓库是否为私有且你有写入权限。|
|**一直显示 "Git is not ready"**|未初始化 Git|确保你的仓库根目录下有隐藏的 `.git` 文件夹（参考步骤 3）。|
|**大文件传不上去**|单文件超过限制|检查 `.gitignore` 文件，确保排除了 `.obsidian/cache` 等无关文件。GitLink 普通仓库单文件通常限制 50MB-100MB。|
|**手机端如何同步？**|手机无 Git 环境|iOS 需使用 **Working Copy** 应用（收费但强大）；安卓可使用 **MGit** 或第三方同步插件（如 Remotely Save 支持 S3，但直接 Git 较难）。|

---

## 7. 总结：

通过 GitLink + Obsidian Git，你构建了一个高速度、私有化的知识备份系统。这不仅保障了数据主权，也为后续的团队协作（通过 GitLink 的 Issue 和 PR 功能管理知识库）打下了基础。

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
