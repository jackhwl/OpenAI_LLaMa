# 06-Tools · 工具集与辅助脚本说明

> 本目录收录课程中使用的 **工具链（Toolchain）**、**辅助脚本（Scripts）**、**安装清单（Install List）**
> 以及与模型调用、智能体构建、环境配置相关的资源文件。
> 简而言之：这里存放的是“让你的知识工作流可以真正跑起来的工具”。

---

## 1. 目录用途

`06-Tools/` 用于存放以下内容：

- 🔧 **本课程所需的软件工具清单（Tools List）**
- 🤖 **智能体相关配置示例（MCP / Cherry Studio / Agent Scripts）**
- 🛠 **用于提升知识工作效率的辅助脚本（如自动重命名、批量清洗文本等）**
- 📦 **ModelScope / OpenAPI 示例配置文件**
- 📝 **可被复用的自动化 Workflow（非实验性质）**

该目录不包含：

- ❌ 课程讲义 → `03-Modules/`
- ❌ 实验指引 → `04-Labs/`
- ❌ 模板文件（Prompt/Config） → `05-Templates/`
- ❌ 小组作业 → `08-Workspace/`

---

## 2. 工具链概览（Toolchain Overview）

本课程涉及一个完整的 **AI + 笔记 + 工作流 + 智能体** 工具栈，包括：

### ### 2.1 核心工具（必备）

| 工具 | 用途 | 备注 |
|------|------|------|
| **Cherry Studio** | 本地 AI 工作台（对话、模型切换、MCP 调用） | 用于 M06-M07 智能体开发 |
| **ModelScope API** | 调用 Qwen / DeepSeek / 语音识别等模型 | 需创建 API Key |
| **Obsidian** | 结构化输入与知识库管理 | 用于 M03-M05 |
| **GitLink / Git** | 协作、版本控制、PR 提交 | Fork → Commit → PR |

---

### 2.2 可选工具（按需启用）

| 工具 | 用途 |
|------|------|
| Python + requests | 自定义接口测试、批处理脚本 |
| Node.js | MCP 扩展工具或自动化任务 |
| Typora / VS Code | Markdown 编辑辅助 |

---

## 3. 目录结构

`06-Tools/` 目录推荐保持如下结构（课程更新可能增加子目录）：

```text
06-Tools/
├── tool-install-guide.md      # 工具安装指南（必读）
├── modelscope-examples/       # ModelScope API 调用示例
│     ├── text-generation.json
│     ├── embeddings.json
│     └── workflow-demo.md
├── mcp-tools/                 # MCP 工具定义与示例
│     ├── file-reader.json
│     ├── web-search.json
│     └── multi-tools-config.md
├── cherry-config/             # Cherry Studio 配置示例
│     ├── agent-config.json
│     └── settings-example.md
├── scripts/                   # 辅助脚本（可选）
│     ├── clean-text.py
│     ├── rename-batch.py
│     └── pdf2md.sh
└── README.md                  # 当前文件
````

你可以根据自己的项目需求添加新的工具文件，只需保持命名规范与目录清晰即可。

---

## 4. 工具安装与配置（简版说明）

### 🔹 4.1 Cherry Studio

下载地址：
👉 [https://github.com/cherryHQ/cherry-studio/releases](https://github.com/cherryHQ/cherry-studio/releases)

安装后需完成：

* 选择默认模型 / API Provider
* 配置 ModelScope API Key
* 导入 MCP 工具文件（位于本目录）

详细操作见：`tool-install-guide.md`

---

### 🔹 4.2 ModelScope API

使用步骤：

1. 注册并获取 API Key
2. 选择模型（如 Qwen2.5, DeepSeek-V3）
3. 可将示例 JSON 拷贝到 Cherry Studio 的“自定义模型”配置中

示例文件：`modelscope-examples/text-generation.json`

---

### 🔹 4.3 MCP 工具（AI 的“插件系统”）

MCP（Model Context Protocol）允许你的 AI 调用：

* 本地文件系统
* 网络请求工具
* 自定义脚本/函数

你可以在：

```
cherry-config/agent-config.json
```

中看到一个完整的 Agent 配置示例（用于 M06-M07 的智能体开发模块）。

---

### 🔹 4.4 辅助脚本（Optional）

放在 `scripts/` 目录下的小工具，可用于：

* 清洗文本噪音（OCR 错误、网页杂质）
* 批量重命名文件（项目整理）
* 批量转 Markdown（pdf → md）

这些工具不是课程必须，但能明显提升工作效率。

---

## 5. 如何在课程中使用这些工具？

不同模块对工具的依赖不同，以下为映射表：

| 模块                | 工具使用内容                                   |
| ----------------- | ---------------------------------------- |
| **M02：工作流定义**     | 不涉及工具，侧重设计与描述                            |
| **M03：结构化输入**     | Obsidian 用于资料整理与结构化输出                    |
| **M04：生成与迭代**     | 任意模型平台（Cherry/ModelScope）均可              |
| **M05：SOP 与资产沉淀** | 本目录中的模板可协助标准化                            |
| **M06-M07：智能体开发** | Cherry Studio + MCP + ModelScope 组成核心工具链 |
| **M08：成果路演**      | 脚本与工具用于最终展示资产化                           |

**一句话总结：**

> 从 M06 开始，`06-Tools/` 内的工具文件将直接决定你们的 AI 助手能否“跑起来”。

---

## 6. 注意事项（必读）

* `06-Tools/` 中的所有配置文件 **不得包含个人 API Key**。
* 自动化脚本请加上注释，方便其他小组理解与复用。
* 若你开发了新的工具文件（如自定义 MCP 工具），欢迎提交 PR 到主仓库。
* 小组作业不要放在此目录，请放在 `08-Workspace/`。

---

## 7. 常见问题（FAQ）

### ❓ 工具无法运行怎么办？

请检查：

* Cherry Studio 是否导入成功
* MCP 工具路径是否正确
* API Key 是否已放入环境变量
* 网络环境是否允许访问模型服务

必要时可在 Issues 区提交截图。

---

## 8. 联系与支持

如对本目录使用有任何问题，可以：

* 在仓库的 `Issues` 中提交问题（建议使用“工具相关”标签）
* 或在微信群 / 上课现场咨询助教

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025 Gitconomy Research社区。
