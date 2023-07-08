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
* L1_student
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