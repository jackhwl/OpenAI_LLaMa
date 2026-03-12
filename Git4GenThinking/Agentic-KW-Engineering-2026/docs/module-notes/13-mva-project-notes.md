# 第十三天：MVA 实战 —— 构建你的“笔记数字助手”

## 1. 本章摘要

欢迎来到课程的终极实战阶段。在前 12 天里，我们像拼乐高一样，逐一掌握了 **S.C.O.R.E. 提示工程**（大脑）、**Obsidian 知识库**（记忆）、**MCP 协议**（神经）以及 **Python 脚本**（手脚）。我们甚至在第 12 天为了防止 AI“暴走”，专门设计了 **安全围栏**。 今天，我们将把所有积木组装在一起，构建你的第一个 **MVA**(Minimum Viable Agent，最小可行智能体) —— 笔记数字助手)。 这个智能体的任务非常具体且具有挑战性：它将自动扫描你的 Obsidian 收件箱 (`00-Inbox`)，阅读杂乱的笔记，分析其内容，为其打上标签，并将其移动到正确的分类文件夹中。 

**本章交付成果**：一个自动化笔记归档管理智能体。你将亲眼见证 AI 在后台“思考”，并弹窗请求你的批准，最后物理移动文件。这是从“聊天机器人”到“数字员工”的质的飞跃。

---

## 2. 最小可行智能体的系统架构

在开始构建智能体之前，我们需要先画出图纸。MVA 不是简单的脚本堆砌，而是一个有生命的 **PEAR 闭环系统**。

### 2.1 具身智能的解剖图

在这个项目中，我们的系统由以下三部分组成：

- **大脑** (Brain)：由 Cherry Studio 加载的 DeepSeek/Qwen 模型。它负责阅读笔记内容，判断它是“项目”、“概念”还是“资源”。
- **手脚** (Body)：一个 增强版的 Python MCP Server。它不仅能读写文件，还集成了我们第 12 天研发的 Tkinter GUI 弹窗，即使在后台运行也能强制获得人类关注。
- **环境** (Environment)：你的 Obsidian 仓库。这是智能体感知和改变的物理世界。

<br>

### 2.2 交互时序与安全协议

这是一个典型的 "L3 高风险操作"（涉及文件移动和修改）。因此，我们的架构必须包含 **HITL (人机协同)** 环节。

**数据流向图** (Data Flow)：

1. **Perceive** (感知)：Agent 调用 `list_handouts` 发现讲义，调用 `read_handout` 读取全文。

2. **Evaluate** (评估)：Agent 读取内容，根据 Prompt 的内容识别出关键概念，生成带有 `YAML Formatter`  格式的原子卡片 md文件， 并移动到 `/Concepts` 目录。

3. **Act**(行动)：Agent 发起 `create_concept_card` 调用。

	    - 情况 A (无冲突)：Python 脚本检测到文件不存在 → 直接写入 → 返回 Success。
	    - 情况 B (有冲突)：检测到 `S.C.O.R.E.模型.md` 已存在 → **弹出 GUI 警告框**。
		    - 用户点击 **Yes** → 覆盖原文件。
		    - 用户点击 **No** → 脚本自动重命名为 `..._v1.md` 并写入。

4. **Reflect** (反思)：Agent 收到工具返回的 `Success: [新建副本]...`，在对话框回复确认。

<br>

---

## 3. 实战演练：组装知识挖掘机

我们将分三步完成组装：编写“手”（Python）、注入“灵魂”（System Prompt）、配置“神经”（Cherry Studio）。

## 3.1 编写Python 脚本

这是本章的核心工程。我们不仅要实现写入，还要在代码层面实现 **数据契约**（自动注入 YAML） 和 **安全围栏**（GUI 仲裁）。

**文件名**：`miner_server.py` **依赖安装**：`pip install "mcp[cli]"` (如果尚未安装)

```bash 
$ pip install mcp[cli]
```

实验完整的参考Python脚本：

```python
import os
import sys
import datetime
import tkinter as tk
from tkinter import messagebox
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务
mcp = FastMCP("Knowledge-Miner")

# ==========================================
# ⚙️ 配置区域 (请修改为您的实际路径)
# ==========================================
# 您的 Obsidian 仓库根目录
VAULT_ROOT = "/home/wguo/Downloads/MyVault"
# 输入源：课程讲义存放位置
INBOX_DIR = os.path.join(VAULT_ROOT, "00-Inbox")
# 输出地：原子概念卡片存放位置
CONCEPT_DIR = os.path.join(VAULT_ROOT, "10-Concepts")
# ==========================================

def validate_path(path):
    """[安全沙箱] 防止路径穿越攻击"""
    full_path = os.path.abspath(path)
    vault_abs = os.path.abspath(VAULT_ROOT)
    if not full_path.startswith(vault_abs):
        raise ValueError(f"🚨 Access Denied: 路径 {path} 超出了安全沙箱范围。")
    return full_path

def get_unique_filename(directory, base_name):
    """
    [辅助函数] 生成不冲突的新文件名
    例如：RAG原理.md -> RAG原理_v1.md -> RAG原理_v2.md
    """
    name, ext = os.path.splitext(base_name)
    counter = 1
    while True:
        new_name = f"{name}_v{counter}{ext}"
        full_path = os.path.join(directory, new_name)
        if not os.path.exists(full_path):
            return new_name, full_path
        counter += 1

@mcp.tool()
def list_handouts() -> list[str]:
    """列出 Inbox 中的所有讲义文件"""
    if not os.path.exists(INBOX_DIR):
        return []
    return [f for f in os.listdir(INBOX_DIR) if f.endswith(".md") and not f.startswith(".")]

@mcp.tool()
def read_handout(filename: str) -> str:
    """读取讲义内容"""
    try:
        path = validate_path(os.path.join(INBOX_DIR, filename))
        if not os.path.exists(path):
            return "Error: File not found."
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Read Error: {str(e)}"

@mcp.tool()
def create_concept_card(source_file: str, concept_name: str, category: str, content: str, reason: str) -> str:
    """
    [L3 级风险] 创建原子概念卡片。
    如果文件存在，弹出 GUI 询问：是覆盖(Yes) 还是 创建副本(No)。
    """
    # 1. 基础路径构建
    safe_name = concept_name.replace(" ", "_").replace("/", "-").replace(":", "")
    filename = f"{safe_name}.md"

    try:
        target_dir = validate_path(CONCEPT_DIR)
        target_path = validate_path(os.path.join(target_dir, filename))

        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
    except ValueError as e:
        return str(e)

    # 2. 冲突检测与 HITL 决策
    final_action = "新建"

    if os.path.exists(target_path):
        try:
            # 启动 GUI 弹窗
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True) # 强制置顶

            msg = (
                f"⚠️ [文件冲突警报]\n\n"
                f"目标文件已存在: {filename}\n"
                f"路径: {target_path}\n\n"
                f"👇 请选择操作:\n"
                f"   [Yes] 覆盖原文件 (危险!)\n"
                f"   [No ] 保留原文件，生成新副本 (_vX)"
            )

            # Yes = True (覆盖), No = False (新建副本)
            should_overwrite = messagebox.askyesno("知识挖掘 - 冲突处理", msg, icon='warning')
            root.destroy()

            if should_overwrite:
                # 用户选择覆盖，保持 target_path 不变
                final_action = "覆盖"
            else:
                # 用户选择保留，生成新文件名
                filename, target_path = get_unique_filename(target_dir, filename)
                final_action = f"新建副本({filename})"

        except Exception as e:
            return f"System Error: GUI 交互失败 - {str(e)}"

    # 3. 组装元数据 (数据契约)
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        clean_content = content.replace("---", "").strip()
        if clean_content.startswith("# "):
            clean_content = "\n".join(clean_content.split("\n")[1:]).strip()

        full_file_content = (
            f"---\n"
            f"type: {category}\n"
            f"source: \"{source_file}\"\n"
            f"tags: [agent, engineering, extracted]\n"
            f"created: {current_date}\n"
            f"---\n\n"
            f"# {concept_name}\n\n"
            f"{clean_content}"
        )

        # 4. 物理写入
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(full_file_content)

        return f"Success: [{final_action}] 卡片已保存至 {filename}"

    except Exception as e:
        return f"Write Error: {str(e)}"

if __name__ == "__main__":
    # 在控制台输出启动日志 (stderr)
    print(f"🚀 Knowledge Miner is running...", file=sys.stderr)
    print(f"📂 Monitoring Inbox: {INBOX_DIR}", file=sys.stderr)
    mcp.run()
```


**脚本逻辑核心解析**：

脚本主要包含三个逻辑模块：**感知层（读）、决策辅助层（交互）、行动层（写）**。

1. 安全沙箱 (Security Sandbox)

	- **函数**: `validate_path(path)`
	- **逻辑**: 所有的文件操作前，都会先调用这个函数。它检查目标路径是否以 `VAULT_ROOT` 开头。
	- **目的**: 防止 AI 出现“幻觉”去修改系统文件或仓库以外的文件（L2 级防御）。

2. 感知工具 (Perception Tools)

	- **函数**: `list_handouts()` 和 `read_handout(filename)`
	- **逻辑**:
		- 扫描 `00-Inbox` 目录。
		- 只读取 `.md` 文件，过滤掉系统隐藏文件。

	- **目的**: 为 AI 提供“眼睛”，让它能看到有哪些讲义需要处理。

3. 核心行动工具 (Core Action Tool) —— `create_concept_card`

	这部分代码集成了 **数据契约** 和 **冲突仲裁**。

	**逻辑流程图：**

	1. **路径构建**：接收 AI 传来的 `concept_name`，清洗非法字符，生成目标路径 `10-Concepts/概念名.md`。

	2. **冲突检测与仲裁**:
		- **判断**: 目标文件是否存在？ (`if os.path.exists`)
		- **若存在 ，触发 L3 级拦截**：
			- 启动 `tkinter` 弹窗，强制置顶 (`topmost`)。
			- 展示来源、理由，询问用户：“覆盖(Yes) 还是 新建副本(No)？”
			- **分支 A (Yes)**: 保持原路径，准备覆盖写入。
			- **分支 B (No)**: 调用 `get_unique_filename`，自动在文件名后加 `_v1`, `_v2`，直到找到不冲突的文件名。
			
	3. **数据契约执行**:
		- **不信任 AI**: 脚本不信任 AI 传入的 `content` 里是否包含了正确的 YAML。
		- **强制注入**: 脚本使用 Python 的 f-string，利用传入的参数 (`category`, `source_file`, `time`) **强制组装** 标准的 YAML Frontmatter。
		- **清洗**: 去除 `content` 中 AI 可能重复生成的标题或旧 YAML，确保内容纯净。

	4. **物理写入**：将组装好的“元数据 + 正文”写入最终确定的路径。

<br>

### 3.2 配置神经连接 (MCP Client)

在 Cherry Studio配置新的 Server。

```json 
{
  "mcpServers": {
    "knowledge-miner": {
      "command": "python",
      "args": [
        "/Replace/With/Your/Absolute/Path/To/miner_server.py"
      ],
      "type": "stdio"
    }
  }
}
```

### 3.3 注入“研究员”灵魂 (System Prompt)

这是一个 **熵减** 的 Prompt。我们通过 **Top-3 熔断机制**，强迫 AI 进行价值判断，而不是大量主题的提取。

```markdown 
# Role (S)
你是一位精通人工智能工程学的 **知识挖掘研究员 (Knowledge Miner)**。
你的核心能力是深度阅读技术文档，识别其中的核心思维模型、工程协议和设计模式，并将它们从非结构化的长文中提炼出来，转化为高内聚、低耦合的 **“原子化知识卡片”**。

# Context (C)
- **运行环境**: 你连接着用户的 Obsidian 知识库。
- **输入源**: `/00-Inbox` 目录下的课程讲义（Markdown 格式）。
- **输出目标**: `/10-Concepts` 目录下的原子概念卡片。
- **工具能力**: 你拥有读取文件 (`read_handout`) 和创建卡片 (`create_concept_card`) 的能力。

# Objective (O)
严格执行以下 **循环挖掘 (Mining Loop)** 工作流：
1. **Scan (扫描)**: 调用 `list_handouts` 查看有哪些待处理的讲义。
2. **Read (阅读)**: 逐个调用 `read_handout` 读取讲义全文。
3. **Analyze (分析与清洗)**: 
   - 深度理解内容，识别文中的关键概念（如 S.C.O.R.E., ReAct, MCP 等）。
   - **⚡️ Top-3 熔断机制**: 每篇讲义 **最多** 提取 **3个** 价值最高的概念。
   - **优先级排序**: 基于“工程价值”和“复用性”进行排序，仅保留前3名。
4. **Extract (提炼)**: 对筛选出的 Top-3 概念，逐个调用 `create_concept_card` 工具进行物理创建。
5. **Link (连接)**: 在正文内容中，如果涉及其他已知的核心概念，必须使用 `[[关联概念名称]]` 的双向链接语法。

# Requirements (R) - 数据契约与红线
1. **工具调用契约 (Schema Contract)**:
   调用 `create_concept_card` 时，**必须包含以下 5 个参数**：
   - `source_file`: 填写来源讲义的文件名。
   - `concept_name`: 概念名称（如 "S.C.O.R.E. 模型"）。
   - `category`: 必须属于 [model, framework, protocol, pattern, strategy] 之一。
   - `content`: **仅包含 Markdown 正文**。结构必须包含 `## 定义`, `## 核心要素`, `## 工程价值`, `## 关联`。
   - **`reason` (必填)**: 用一句话解释为什么要提取这个概念（例如：“这是提示工程的核心框架”）。**这用于在弹窗中说服用户批准操作。**

2. **安全红线 (Safety Rails)**:
   - **只读原件**: 严禁修改、移动或删除 `/00-Inbox` 中的原始讲义文件。
   - **原子性**: 每次工具调用只创建一个核心概念。

3. **去重策略**:
   - 如果发现概念名称已存在，请在 `reason` 中说明这是“补充”或“修订”，交由用户决定。

# Evaluation (E) - 自我修正
- **自检参数**: 调用工具前，检查 `reason` 字段是否已填充？如果没有，必须补上。
- **自检数量**: 本篇讲义是否已提取超过 3 个？如果是，立即停止。
- **内容清洗**: 确保 `content` 字段不包含 YAML 头（--- ... ---），因为脚本会自动生成它。
```

---

## 4. 本章总结

今天，我们跨越了理论与实践的鸿沟，成功构建了第一个 **MVA** (Minimum Viable Agent) —— 一个能够自主阅读、思考并整理 Obsidian 笔记的数字助手。我们不仅完成了代码的编写，更重要的是验证了一套完整的智能体工程方法论：

1. **具身智能架构** ： 我们走出了纯文本对话框，通过 **MCP 协议** 为大模型装上了“手脚”（Python 脚本），使其能够感知（`list/read`）并改变（`create`）本地文件系统这一物理环境。
    
2. **安全驱动开发** ： 在赋予 AI 修改文件的能力时，我们实施了 **L3 级风险控制**。通过在 Python 脚本中集成 `tkinter`，我们实现了一种“带外（Out-of-Band）”的  **HITL**  (人机协同) 机制。即使智能体在后台运行，关键决策（如覆盖文件）也必须经过人类的显式批准。
    
3. **数据契约与熵减**： 我们没有依赖 AI 的幻觉来生成元数据，而是在 Python 代码层强制注入了标准的 YAML Frontmatter（**数据契约**）。同时，通过 System Prompt 中的“Top-3 熔断机制”，我们强迫 AI 进行价值筛选，实现了从杂乱信息到有序知识的 **熵减** 过程。


---

## 5. 课后思考

1. 目前的脚本是运行一次扫描一次（Polling）。如何利用 Python 的 `watchdog` 库改造 `miner_server.py`，使其变成一个后台守护进程？即：当你按下 `Ctrl+S` 保存一篇讲义时，Agent 毫秒级自动触发阅读与归档？
        
2. 如果在不同的讲义中，AI 分别提取了 "S.C.O.R.E. Model" 和 "SCORE Framework"，系统会创建两个文件。如何在 `create_concept_card` 之前增加一步“向量检索”？先去 `/10-Concepts` 查重，如果发现相似度极高的概念，应该执行“合并（Merge）”操作而不是“新建”。
        
3. 讲义中常包含架构图或白板截图。当前的 `read_handout` 只读取文本。如何集成 OCR 工具（如带有 `Vision` 推理能力的模型），让智能体能“看懂”图片中的流程图，并将其转化为 Mermaid 代码存入卡片？

<br>

---

##  附录1： 核心术语表 (Glossary)

|英文术语|中文翻译|工程定义|
|---|---|---|
|**HITL**|**人机协同**|**Human-in-the-Loop**。在自动化系统的关键决策节点（通常是高风险操作前），强制引入人类反馈介入的机制。|
|**Safety Rails**|**安全围栏**|防止智能体产生有害输出或执行危险操作的限制机制，分为认知层的软围栏和代码层的硬围栏。|
|**Soft Rails**|**软围栏**|基于 **Prompt Engineering** 的限制。通过提示词（如“不要删除”、“先询问”）引导模型行为，但理论上可被“越狱”或忽略。|
|**Hard Rails**|**硬围栏**|基于 **Code Logic** 的物理限制。通过编程语言（Python/Go）的条件判断（`if/else`）或阻塞函数（`input`）强制拦截，AI 无法绕过。|
|**Headless Mode**|**无头模式**|指软件在没有图形用户界面（GUI）的情况下运行。在 MCP 中，Server 端脚本通常运行在无头模式下，因此标准输出通常用于传输数据而非交互。|
|**Idempotency**|**幂等性**|一个操作执行一次和执行多次产生的结果是相同的。在文件写入场景中，需通过“检查是否存在”来处理非幂等的覆盖风险。|
|**Race Condition**|**竞态条件**|在本章中指 AI 在尚未收到人类确认指令（Token）的情况下，因推理速度过快直接生成了工具调用指令（Action）的现象（即“抢跑”）。|
|**MCP Router**|**工具路由**|MCP 客户端根据 LLM 的意图，将自然语言请求分发给具体工具（如 `filesystem` 或 `search`）的决策过程。|

---

## 许可声明

本文档采用 [知识共享署名--相同方式共享 4.0 国际许可协议 (CC BY--SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.zh) 进行许可， &copy; 2025-2026 Gitconomy Research社区。