# 搜索工具配置
## 工具选择
- **首选**：Tavily Search API（专用搜索工具，结果更适合 AI 处理）
- **备选**：内置 WebSearch（通用搜索，效果稍差但无需配置）
## Tavily 配置步骤
### 1. 获取 API Key
1. 访问 https://tavily.com
2. 注册账号并获取 API Key
3. 将 API Key 保存为环境变量：`export TAVILY_API_KEY="your-key-here"`
### 2. 测试搜索
使用以下命令测试搜索是否正常：
```bash
curl -X POST “https://api.tavily.com/search” \
  -H “Content-Type: application/json” \
  -d '{“api_key”: “your-key-here”, “query”: “MIT vs Apache license”}'
```
### 3. 在 Deep Research 中使用
在工作流步骤 3（资料检索）中，调用 Tavily 搜索工具：
- 输入：子问题
- 输出：搜索结果列表（标题、URL、摘要）
## 使用规范
- 每个子问题至少搜索一次
- 优先选择权威来源（官方文档、学术论文、权威媒体）
- 记录搜索结果的基本信息（标题、URL、日期）