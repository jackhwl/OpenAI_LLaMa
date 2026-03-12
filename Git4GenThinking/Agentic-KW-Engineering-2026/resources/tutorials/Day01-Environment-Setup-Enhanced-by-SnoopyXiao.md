# Day 01: Obsidian 环境配置指南

> **引用声明 / Reference**
> * **适用系统:** Windows, macOS, Linux
> * **贡献者:** SnoopyXiao
> * **增强说明:** 补充 Obsidian 环境的基础和常用的配置, 提升Obsidian的可用性, 有助于后续课程的学习, 新手友好。

---

## Obsidian环境配置新手教程

### 1.  安装Obsidian

- Obsidian安装及配置, 2025年 && 2026年的课件整理的比较完善, 这里不再赘述, 可以参考以下链接:
  - [Obsidian安装与使用指南](https://www.gitlink.org.cn/Gitconomy/Git4GenThinking/tree/main/GT-Workflow-Course-2025%2F06-Tools%2Fobsidian-installation-guide.md)

### 2. Obsidian插件的安装方式

#### 安装方式1 (推荐方式)：

- 在左边工具栏 → 打开设置 → 选项 → 第三方插件 → 安全模式（点击关闭）。
- 在社区插件市场,点击浏览 → 在搜索社区插件框，搜索你要的插件名 → 点击"安装" → 点击"启用" → 安装完成。
- 插件自动安装到 Vault/.obsidian/plugins/插件文件夹下。

#### 安装方式2（社区插件市场打不开情况）

- 在左边工具栏 → 打开设置 → 选项 → 第三方插件 → 安全模式（点击关闭）。
- 在github搜索插件地址，比如：[https://github.com/开发者用户名/插件文件地址](https://github.com/开发者用户名/插件文件地址) → 把插件文件名的目录以及里面“main.js/manifest.json/style.css” 下载下来;
- 复制或移动到 Vault/.obsidian/plugins/ 插件文件夹下 → 安装完成。

#### 安装方式3（社区插件市场打不开情况）

- 首先以**安装方式2** 安装 [obsidian-proxy-github插件](https://gitee.com/juqkai/obsidian-proxy-github/releases) → 安装完成。
- **第三方插件obsidian-proxy-github** "安装" && "启用"后,  可以以**安装方式1**安装社区市场的插件 → 安装完成。

#### 安装方式4（社区插件市场打不开情况 && 插件市场没有上架该插件）
 
- 首先以**安装方式2** 安装[obsidian42 BRAT插件](https://github.com/TfTHacker/obsidian42-brat) 
- 在左边工具栏 → 打开设置 → 选项 → 启用插件"BRAT"。
- **第三方插件"BRAT"** → Beta plugin list一栏 → 点击 Add beta plugin → 弹出的窗口输入[https://github.com/开发者github用户名/插件文件名](https://github.com/开发者github用户名/插件文件名)，然后点击Add plugin→ 安装完成
- 插件自动安装到 Vault/.obsidian/plugins/插件文件夹下。


### 3. Obsidian 主题

- 打开 Obsidian → 左下角「设置」→「外观」Appearance →「基础颜色」Base Color scheme → 可点击Manage, 安装/切换官方深色主题, 选一个喜欢的.

### 4. Obsidian 常用快捷键

| 功能                     | Windows/Linux 快捷键            | macOS 快捷键                    | 特别说明                                  |
| ------------------------ | ------------------------------- | ------------------------------- | ----------------------------------------- |
| **通用**                 |                                 |                                 |                                           |
| 新建笔记                 | Ctrl + N                        | Cmd + N                         |                                           |
| 保存                     | Ctrl + S                        | Cmd + S                         |                                           |
| 打开设置                 | Ctrl + ,                        | Cmd + ,                         |                                           |
| 切换预览/编辑模式        | Ctrl + E                        | Cmd + E                         |                                           |
| 笔记中搜索               | Ctrl + F                        | Cmd + F                         |                                           |
| 全局搜索                 | Ctrl + Shift + F                | Cmd + Shift + F                 |                                           |
| 切换全屏                 | F11                             |                                 |                                           |
| 查看帮助                 | F1                              |                                 |                                           |
| **文本编辑**             |                                 |                                 |                                           |
| 复制                     | Ctrl + C                        | Cmd + C                         |                                           |
| 粘贴                     | Ctrl + V                        | Cmd + V                         |                                           |
| 忽略格式粘贴             | Ctrl + Shift + V                | Cmd + Shift + V                 |                                           |
| 剪切                     | Ctrl + X                        | Cmd + X                         |                                           |
| 撤销                     | Ctrl + Z                        | Cmd + Z                         |                                           |
| 重做                     | Ctrl + Y / Ctrl+Shift+Z         | Cmd+Shift+Z                     |                                           |
| 复制段落                 | Ctrl + C （未选择文本时）       | Cmd + C（未选择文本时）         |                                           |
| 剪切段落                 | Ctrl + X（未选择文本时）        | Cmd + X（未选择文本时）         |                                           |
| 删除段落                 | Ctrl + D                        | Cmd + D                         |                                           |
| **文本编辑**             |                                 |                                 |                                           |
| 插入新行                 | Enter                           | Enter                           |                                           |
| 删除前一个字符           | Backspace                       | Backspace                       |                                           |
| 删除后一个字符           | Delete                          | Delete                          |                                           |
| 删除前一个单词           | Ctrl + Backspace                | Option+Backspace                |                                           |
| 删除后一个单词           | Ctrl + Delete                   | Option+Delete                   |                                           |
| 删除当前行               | Ctrl+Shift+K（未选择文本时）    | Cmd + Shift + K（未选择文本时） |                                           |
| 插入外链                 | Ctrl + K                        | Cmd + K                         |                                           |
| **文本导航**             |                                 |                                 |                                           |
| 光标移动到当前行首       | Home / Ctrl + Left Arrow        | Cmd + Left Arrow                |                                           |
| 光标移动到当前行尾       | End / Ctrl + Right Arrow        | Cmd + Right Arrow               |                                           |
| 光标移动到笔记开头       | Ctrl + Home                     | Cmd + Up Arrow                  |                                           |
| 光标移动到笔记末尾       | Ctrl + End                      | Cmd + Down Arrow                |                                           |
| 光标向上一行             | Up arrow                        | Up arrow                        |                                           |
| 光标向下一行             | Down arrow                      | Down arrow                      |                                           |
| 光标向上一页             | PageUp                          |                                 |                                           |
| 光标向下一页             | PageDown                        |                                 |                                           |
| **文本选择**             |                                 |                                 |                                           |
| 全选                     | Ctrl + A                        | Cmd + A                         |                                           |
| 取消选择                 | Escape                          | Escape                          |                                           |
| 其它                     |                                 |                                 | "文本导航"按键 + Shift                    |
| **标签页操作**           |                                 |                                 |                                           |
| 关闭标签                 | Ctrl + W                        | Cmd + W                         |                                           |
| 撤销关闭标签             | Ctrl + Shift + T                | Cmd + Shift + T                 |                                           |
| 切换标签                 | Ctrl + Tab / Ctrl + Shift + Tab | Cmd + Tab / Cmd + Shift + Tab   |                                           |
| 新建标签                 | Ctrl + T                        | Cmd + T                         |                                           |
| **自定义 / Plugin 扩展** |                                 |                                 |                                           |
| 显示/隐藏左面板          | Ctrl + Shift + L                | Cmd + Shift + L                 | 需要用户设定                              |
| 显示/隐藏右面板          | Ctrl + Shift + R                | Cmd + Shift + R                 | 需要用户设定                              |
| 套用模板                 | Ctrl + T                        | Cmd + T                         | 需要用户设定, 替换"新建标签"快捷键        |
| 插入双链                 | Ctrl + I                        | Cmd + I                         | 需要用户设定, 替换"设置斜体"快捷键        |
| AI生成文本               | Ctrl + J                        | Cmd + J                         | 需要安装第三方插件 "Text Generator"       |
| 关系图谱                 | Ctrl + G                        | Cmd + G                         | 需要开启核心插件 "关系图谱"               |
| 局部关系图谱             | Ctrl + Shift + G                | Cmd + Shift + G                 | 需要开启核心插件 "关系图谱", 需要用户设定 |
