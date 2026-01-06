import asyncio
import os
from dotenv import load_dotenv
from colorama import Fore

from autogen_agentchat.agents import AssistantAgent 
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import UserProxyAgent


load_dotenv()

# 1. Initialize OpenAI client
model_client = OpenAIChatCompletionClient(
    model="gpt-4.1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 2. Define system prompts for each agent
PROMPT_DEVELOPER = """You are a developer tasked with implementing a feature based on the provided requirements.
Your job is to create a detailed implementation plan, including code snippets, architecture decisions, and any
necessary considerations for the feature. Ensure that your plan is clear, concise, and ready for review by the lead developer.
"""

PROMPT_LEAD_DEVELOPER = """You are a lead developer reviewing the implementation plan created by the developer.
Your role is to assess the plan for technical feasibility, adherence to best practices, and alignment with
project goals. Provide constructive feedback, suggest any necessary changes or improvements, and ensure that the plan is ready for final
review by the final reviewer. If the plan is satisfactory, approve it for final review.
"""

PROMPT_FINAL_REVIEWER = """You are a final reviewer assessing the implementation plan.  
Your role is to provide high-level feedback and ensure alignment with project goals. ✅ Approve or ❌ reject the plan with justification. add in generated response"""

# 3. Define assistant agents
assistant_developer = AssistantAgent(
    "developer",
    system_message=PROMPT_DEVELOPER,
    model_client=model_client,
)

assistant_lead_developer = AssistantAgent(
    "lead_developer",
    system_message=PROMPT_LEAD_DEVELOPER,
    model_client=model_client,
)

assistant_final_reviewer = AssistantAgent(
    "final_reviewer",
    system_message=PROMPT_FINAL_REVIEWER,
    model_client=model_client,
)

# 4. Define user proxy
user_proxy = UserProxyAgent("user_proxy")

# 5. Define the agent graph and flow
builder = DiGraphBuilder()
builder.add_node(user_proxy).add_node(assistant_developer).add_node(assistant_lead_developer).add_node(assistant_final_reviewer)


# 6. Define the edges for communication between AI agents
builder.add_edge(assistant_developer, assistant_lead_developer)
builder.add_edge(assistant_lead_developer, assistant_final_reviewer)

# 7. Set the entry point of the conversation
builder.set_entry_point(user_proxy)

graph = builder.build()


# 8. Main async function to run the flow
async def main():
    """Run the multi-agent development workflow."""
    print(f"{Fore.GREEN}🚀 Running multi-agent dev workflow...\n{Fore.RESET}")

    flow = GraphFlow(
        [user_proxy, assistant_developer, assistant_lead_developer, assistant_final_reviewer],
        graph=graph,
    )
    await Console(flow.run_stream(task="Create a detailed implementation plan for a new feature in the project, including code snippets and architecture decisions."))
    await model_client.close()
    
if __name__ == "__main__":
    asyncio.run(main())
