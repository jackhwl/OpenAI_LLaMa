
import asyncio
import os
from dotenv import load_dotenv
from colorama import Fore
from autogen_agentchat.agents import AssistantAgent # type: ignore
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console # type: ignore
from autogen_ext.models.openai import OpenAIChatCompletionClient # type: ignore

load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

PROMPT = "You are a creative marketing assistant who generates and explains product ideas clearly in 1 sentence"

# 1. Set up OpenAI model client
# Create an agent that uses the OpenAI GPT-4o model.
model_client = OpenAIChatCompletionClient(
    model="gpt-3.5-turbo",  
    api_key=OPENAI_API_KEY,
)

# 2. Set up Single Agent (AssistantAgent)
marketing_agent = AssistantAgent(
    name="marketing_agent",
    model_client=model_client,
    system_message=PROMPT,
)

presenter_agent = AssistantAgent(
    name="presenter_agent",
    model_client=model_client,
    system_message="You are a presentation assistant to present the marketing idea nicely using colors and emojis.",
)

# Async function for getting results
async def main():
    """Main function to run the multi-agent system."""
    print(f"{Fore.MAGENTA} Generating idea... {Fore.RESET}")

    group_chat = RoundRobinGroupChat([marketing_agent, presenter_agent])

    await Console(group_chat.run_stream(task="Create a marketing concept for an 'idea box'"))
    await model_client.close()


# Entry point
if __name__ == "__main__":
    asyncio.run(main())

