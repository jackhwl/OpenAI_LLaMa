from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import SearchTool

# 创建LLM和智能体
llm = HelloAgentsLLM()

# 创建一个强调工具使用的系统提示词
system_prompt = """你是一个AI助手，可以使用搜索工具来获取最新信息。

当需要搜索信息时，请使用以下格式：
[TOOL_CALL:search:搜索关键词]

例如：
- [TOOL_CALL:search:最新AI新闻]
- [TOOL_CALL:search:Python编程教程]

请在回答问题前先使用搜索工具获取最新信息。"""

agent = SimpleAgent(name="AI助手", llm=llm, system_prompt=system_prompt)

# 添加搜索工具
agent.add_tool(SearchTool())

# 示例：使用搜索工具回答问题
response = agent.run("最新的AI技术发展趋势是什么？")
print(f"\n回答：{response}")
