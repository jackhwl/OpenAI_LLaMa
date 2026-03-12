# Day 08: Cherry Studio 环境配置指南

> **引用声明 / Reference**
> * **适用系统:** Windows, macOS, Linux
> * **贡献者:** SnoopyXiao
> * **增强说明:** 补充 Cherry Studio 环境的基础和常用的配置, 提升Cherry Studio的可用性, 有助于后续课程Agent的学习, 新手友好。

---

## 1. Obsidian 环境配置补遗

- Obsidian Canvas 安装及配置, 2025年 && 2026年的课件整理的比较完善, 这里不再赘述, 可以参考以下链接:
	- [Obsidian Canvas 可视化编排操作指南](https://www.gitlink.org.cn/Gitconomy/Git4GenThinking/tree/main/GT-Workflow-Course-2025%2F06-Tools%2Fobsidian-canvas-guide.md) 
	  > 需要吐槽一下: 文中推荐的配色方案,  默认不在调色盘上, 所以按照规范画图会比较费劲。

- Day03 讲义中,  建议安装 **dataview插件** 和 **Menudata Menu插件**。
- Day08 讲义中,  要求在Canvas 中画虚线, 需要安装 **Advanced Canvas插件** 支持,  按照如下方法安装即可。
  ![[Day01-Environment-Setup-Enhanced-by-SnoopyXiao#安装方式1 (推荐方式)：]]

## 2. Cherry Studio 环境配置指南

### 2.1  安装Cherry Studio

- Cherry Studio 安装及配置, 2025年 && 2026年的课件整理的比较完善, 这里不再赘述, 可以参考以下链接:
  - [Cherry Studio安装与配置指南](https://www.gitlink.org.cn/Gitconomy/Git4GenThinking/tree/main/GT-Workflow-Course-2025%2F06-Tools%2Fcherry-studio-intallation-guide.md))

### 2.2 为后续的课程配置MCP Server

#### 2.2.1 安装MCP Server
- Cherry Studio,  右上角 Settings 弹窗 -> MCP 服务器 -> MCP 服务器 ->  打开 "MCP 服务器" 卡片; 
- 右上角,  "添加" 下拉菜单 -> 选择"从Json导入"  -> 贴入Json -> 添加完成; 
- 生成的MCP条目, 右上角点击Enable -> 点击进入MCP条目 -> 右上角日志, 可以检查是否创建/启动成功。
#### 2.2.2 Day09 配置 MCP server(obsidian-vault)：

```json
{
  "mcpServers": {
    "obsidian-vault": {
      "command": "npx",
      "args": [
        "-y",
        "@mauricio.wolff/mcp-obsidian@latest",
        " J:\\datawhale_course\\work\\AI-Agent-Space"
      ]
    }
  }
}
```
#### 2.2.3 Day11 配置 MCP server(fetch-local/filesystem)：

```json
{
  "mcpServers": {
    "fetch-local": {
      "command": "uvx",
      "args": [
        "mcp-server-fetch"
      ]
    }
}
```

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "J:\\datawhale_course\\work\\AI-Agent-Space"
      ]
    }
  }
}
```

#### 2.2.4 Day12 配置 MCP server(Note-Guard)：

```json
{
  "mcpServers": {
	"Note-Guard": {
	  "command": "python",
	  "args": [
		"J:\\datawhale_course\\work\\AI-Agent-Space\\task03\\12-agent-uardrails-notes\\note-guard.py"
	  ]
	}
  }
}
```

#### 2.2.5 Day13 配置 MCP server(knowledge-miner)：

```json
{
  "mcpServers": {
	"knowledge-miner": {
	  "command": "python",
	  "args": [
		"J:\\datawhale_course\\work\\AI-Agent-Space\\task03\\13-mva-project-notes\\miner_server.py"
	  ],
	  "type": "stdio"
	}
  }
}
```

- 安装**python** 以后, 设置环境变量
```markdown
Python 主程序路径：C:\Users\<用户名>\AppData\Local\Programs\Python\Python39\
Scripts 路径：C:\Users\<用户名>\AppData\Local\Programs\Python\Python39\Scripts\
```

- python script **依赖安装**
```python
$ python.exe -m pip install --upgrade pip
$ pip install mcp[cli]
```
