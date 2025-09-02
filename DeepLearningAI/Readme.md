# ChatGPT Prompt Engineering for Developers
* l2-l8

# LangChain for LLM Application Development
* L1-Model_prompt_parser
* L2-Memory
* L3-Chains
* L4-QnA
* L5-Evaluation
* L6-Agents

# Building Systems with the ChatGPT API
* L1_studen
* L2_Classification
* L3_Moderation
* L4_Chain_of_Thought_Reasoning
* L5_Chaining_Prompts
* L6_Check_Outputs
* L7_Evaluation
* L8_Evaluation_Part_I
* L8_Evaluation_Part_II

# How Diffusion Models Work
* L1_Sampling
* L2_Training
* L3_Controlling
* L4_Speeding

# Generative AI with Large Language Models
* LLM pre-training and scaling laws
* Generative AI project lifecycle:

Scope|Select|Adapt and align model|Application integration
---|---|---|---
Define the use case|Choose an existing model or pretrain your own|<table><tr><td>Prompt engineering</td><td colspan=3 >Evaluate</td></tr><tr><td>Fine-tuning</td></tr><tr><td>Align with human feedback</td></tr></table>|<table><tr><td>Optimize and deploy model for inference</td><td>Augment model and build LLM-powered applications</td></tr></table>

# LangChain Chat with Your Data
* Components: Prompts, Models, Indexes, Chains, Agents
* Document Loading
* Document Splitting
* Vectorstores and Embeddings
* Retrieval
* * Maximum marginal relevance (MMR): you may not always want to choose the most similar responses.
* * 1 Query the Vector Store
* * 2 Choose the `fetch_k` most similar responses
* * 3 Within those responses choose the `k` most diverse
* * LLM Aided Reetrieval: There are several situations where the Query applied to the DB is more than just the Question asked. One is SelfQuery, where we use an LLM to convert the user question into a query: Filter + Search term.
* * Compression: Increase the number of results you can put in the context by shrinking the responses to only the relevant information.
* Other types of retrieval: Not using a vector database, such as: SVM, TF-IDF
* Question Answering:
* * 1. Map_reduce
* * 2. Refine
* * 3. Map_rerank
* Chat

# Claude Code: A Highly Agentic Coding Assistant
  - Introduction
  - What is Claude code?
  - Course Notes
    - npm icnstall -g @anthropic-ai/claude-code
  - Setup & Codebase Understanding
  - Adding Features
    - claude mcp add playwright npx @playwright/mcp@latest
  - Testing, Error Debugging and Code Refactoring
  - Adding Multiple Features Simutaneously
    - git worktree add .trees/ui_feature
  - Exploring Github Integration & Hooks
  - Refactoring a Jupyter Notebook & Creating a Dashboard
  - Creating Web App based on a Figma Mockup
    - claude mcp add playwright npx @playwright/mcp@latest
    - Using the app/design.png as the design mockup to analyze the mockup and build the underlying code in this next.js  application. Use the recharts library for creating charts to make this a web application. Check how this application looks using the playwright MCP server and verify it looks as close to the mock as possible   
# MCP: Build Rich-Context AI Apps with Anthropic
  - Introduction
  - Why MCP
  - MCP Architectur
    - Tools: functions and tools that can be invoked by the client
    - Resources: Read-only data or exposed by the server
    - Prompt Templates: Pre-defined templates for AI
    - MCP Client
      - Invokes Tools
      - Queries for Resources
      - Interpolates Prompts
    - MCP Server
      - Exposes Tools: @mcp.tools
      - Exposes Resources
      - Exposes Prompt Templates
      - Defining a Tool
        - @mcp.tools()
      - Resources
        - @mcp.resource("docs://documents", mime_type="application/json")
        - @mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
      - Prompts
        - @mcp.prompt(name="format", description="Rewrites the contents of a document in Markdown format",)
    - MCP Transports
      - For servers running locally: stdio
      - For remote servers:
        - HTTP+SSE stateful 2024-11-05
        - Streamable HTTP stateless or stateful 2025-03-26
  - Chatbot Example
    - .env contains apikey
  - Creating an MCP Server
    - uv init
    - un venv
      - 3.13.6
    - source .venv/bin/activate
    - uv add mcp
    - npx @modelcontextprotocol/inspector uv run research_server.py
  - Creating an MCP Client
    - uv add anthropic python-dotenv nest_asyncio
    - uv run mcp_chatbot.py
  - Connecting the MCP Chatbot to Refrence Servers
  - Adding Prompt and Resource Features
  - Configuring Servers for Claude Desktop
    - source .venv/bin/activate
    - deactivate
    - uv add arxiv mcp
    - Create a symlink without spaces
    - ln -s "/Users/wenlin/OpenAI_LLaMa/DeepLearningAI/MCP Build Rich-Context AI Apps with Anthropic/L4/mcp_project" ~/mcp_project
    - Use the fetch tool visit deeplearning.ai and find an interesting topic about machine learning on that webpage.
    - Then research two papers on arxiv about that topic and summarize the main topics covered.
    - Finally, generate a web based quiz application with a set of flashcards based on the key topics in the papers.
    - ai_agents_quiz.html
  - Creating and Deploying Remote Servers
# Building toward Computer Use with Anthropic
  - Overview
  - Working with the API