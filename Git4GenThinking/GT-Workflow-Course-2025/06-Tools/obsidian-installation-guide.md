# 📘 Obsidian安装与使用指南Beginner Guide）

---

# # 1. 什么是 Obsidian？

**Obsidian** 是一款基于 Markdown 的本地知识库工具，它的三个核心理念：

- **本地文件**：笔记全部以 `.md` 存储在你自己的电脑中，可长期保存；
- **双向链接（[[link]]）**：让知识之间自动形成网络；
- **插件生态强大**：可扩展任务管理、日记、图谱视图、Zettelkasten 等系统。


适合：

- 学生写课堂笔记
- 研究人员搭建知识库
- 写作、项目管理、个人效率系统
- 构建第二大脑（Second Brain）


---

## 2. 安装 Obsidian

### 2.1 Windows/Mac 安装

访问官网：
👉 [https://obsidian.md](https://obsidian.md/)

点击 **Download**，系统会自动识别你的平台。

安装步骤：

1. 打开安装包
2. 点击「Install」
3. 安装完成后启动 Obsidian

---

### 2.2 Linux 安装（deb/AppImage / Flatpak）

### 1. 使用 `.deb` 包安装指南

本指南适用于：

- Ubuntu
- Debian
- Linux Mint
- 以及所有基于Debian的发行版

官方地址（建议优先使用）：

👉 [https://obsidian.md/download](https://obsidian.md/download)

进入 `.deb` 文件所在目录，例如：

```bash
cd ~/Downloads
```

然后执行：

```bash
sudo dpkg -i Obsidian-1.6.5.deb
```

```
如果出现依赖问题，执行：

```
```bash
sudo apt --fix-broken install
```
```
Obsidian 将自动完成安装。
```
### 2. 使用AppImage安装指南

```bash
chmod +x Obsidian-*.AppImage
./Obsidian-*.AppImage
```

### 3. 使用Flatpak安装指南

```bash
flatpak install flathub md.obsidian.Obsidian
flatpak run md.obsidian.Obsidian
```

---

## 3. 第一次使用：创建一个 Vault（知识库）

启动 Obsidian，你会看到三个选项：

- **Create new vault**（创建新的库）
- **Open folder as vault**（打开已有文件夹）

选择：

> **Create new vault → 输入名称 → 选择文件夹位置 → Done**

一个 Vault 就是一个普通文件夹，里面存放 Markdown 文件。

---

## 4. 基本界面介绍

Obsidian 主界面分为 5 大区域：

|区域|功能说明|
|---|---|
|左侧边栏|文件管理器、搜索、标签、插件入口|
|顶部工具栏|面板布局、后退/前进、设置|
|中间编辑区|写笔记的主要界面|
|右侧边栏|反向链接（Backlinks）、出链（Outgoing links）|
|底部状态栏|编辑模式提示、插件状态|

---

## 5. 写下你的第一篇笔记

在左侧点击「新建笔记」图标，输入：

```markdown
# 我的第一篇 Obsidian 笔记

欢迎来到 Obsidian！
这是我学习 Markdown 与双向链接的地方。

## 今日待办
- [ ] 安装必要插件
- [ ] 建立我的工作区结构
- [ ] 学习如何使用双向链接 [[双向链接是什么]]

```

按下 `Ctrl + S`（或自动保存）即可生成一个 `.md` 文件。

---

## 6. Markdown 基础语法（Obsidian 100% 支持）

常用语法示例：

```markdown
# 一级标题
## 二级标题

**加粗**
*斜体*

- 无序列表
1. 有序列表

> 引用内容

`行内代码`

```

代码块

````

插入图片：

```markdown
![[example.png]]
````

插入双向链接：

```markdown
[[笔记名称]]
```

嵌入另一篇笔记：

```markdown
![[另一篇笔记]]
```

---

## 7. Obsidian 最强能力：双向链接（Backlinks）

在笔记中输入：

```markdown
[[数学笔记]]
```

如果这篇笔记不存在，Obsidian 会自动帮你创建。

右侧边栏会显示：

- **Linked mentions：**哪些笔记主动链接到它

- **Unlinked mentions：**哪些笔记提到相关词但未链接（可一键转为链接）


这会自然形成一个“知识网络图谱”。

---

## 8. 图谱视图（Graph View）

点击左侧「Graph view」即可看到：

- 笔记 = 节点
- 连接 = 双向链接


它能帮助你洞察知识之间的关系，非常适合：

- 研究者构建文献关系
- 学生整理课程体系
- 写作大纲可视化


---

## 9. 核心插件推荐（官方内置，无需额外安装）

在 `Settings → Core plugins` 中启用：

|插件|功能|
|---|---|
|Daily notes|自动创建每日笔记|
|Templates|快速插入常用模板|
|Outline|根据标题生成目录结构|
|Page preview|悬停预览笔记内容|
|Backlinks|显示反向链接|
|File explorer|笔记管理器|

---

## 10. 社区插件（Community Plugins）

⚠️ 第一次安装需要先开启：
`Settings → Community plugins → Turn off Safe mode`

## 常用必装插件推荐：

|插件名|用途|
|---|---|
|**Dataview**|在笔记中执行 SQL-like 查询，构建数据库级系统|
|**Calendar**|显示日历 + 与每日笔记联动|
|**Tasks**|强大的任务管理系统|
|**Templater**|高级模板引擎（可自动生成内容）|
|**Periodic Notes**|日/周/月笔记自动化|
|**Advanced Tables**|更容易编辑表格|

---

## 11. 同步与备份

Obsidian 是本地优先，可以自己选择同步方式：

|同步方式|特点|
|---|---|
|Obsidian Sync（官方付费）|最稳、带端到端加密|
|iCloud / OneDrive / Dropbox|跨设备同步（部分冲突需要注意）|
|Git + GitHub|适合程序员，版本管理最强|
|手动备份|复制整个 Vault 文件夹即可|

---

## 12. 常用模板示例（可用于 Templates 插件）

## 日记模板

```markdown
# 🗓 {{date:YYYY-MM-DD}}

## 今日计划
- [ ]

## 今日学习
-

## 今日反思
-
```

### 课程笔记模板

```markdown
# {{title}}

## 课程概要
- 授课教师：
- 日期：
- 课程编号：

## 本节重点
-

## 概念与例子
### 概念
-

### 例子
-

## 我的疑问
-
```

---

## 13. Obsidian 初学者最佳实践（10 条原则）

1. **从小开始**：每天写一条笔记即可
2. **文件夹越少越好**：大量嵌套会降低 Obsidian 的优势
3. **多用 [[链接]] 代替分类**
4. **使用日记记录每日思考**
5. **每周用 Dataview 做一次回顾**
6. 不追求完美结构：让网络随着笔记增长自然长大
7. 定期备份 Vault
8. 重要资源用 `![[embed]]` 嵌入
9. 用模板提升效率
10. 把 Obsidian 当作“思考工具”，不是“资料仓库”


---

# 14. 结束语

Obsidian 的力量来自“你自己的知识网络”。
当你开始：

- 把想法拆成颗粒化的小笔记
- 用链接建立关系
- 用插件让知识系统自动化

---
## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
