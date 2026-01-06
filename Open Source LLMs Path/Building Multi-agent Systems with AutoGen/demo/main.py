
import asyncio
import os
from dotenv import load_dotenv
from colorama import Fore
from autogen_agentchat.agents import AssistantAgent

from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import UserProxyAgent
from utils import geo_code, get_current_weather

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

PROMPT_AGENT_1 = "You are a helpful agent that provides coordinates for a given location."""

PROMPT_AGENT_2 = (
    """ You are a weather forecasting assistant in a multi-agent system.
    Your role is to accurately assist in retrieving, analyzing, and forecasting weather data.
    Reply with TERMINATE when the task has been completed."""
)
# Define a model client. You can use other model client that implements
# the `ChatCompletionClient` interface.
model_client = OpenAIChatCompletionClient(
  model="gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Define an AssistantAgent with the model, tool, system message, and reflection enabled.
# The system message instructs the agent via natural language.

agent_weather_1 = AssistantAgent(
    "get_coordinates",
    description="Get the coordinates given a location.",
    system_message=PROMPT_AGENT_1,
    model_client=model_client,
    tools=[geo_code],
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)

agent_weather_2 = AssistantAgent(
    "weather_agent",
    description="A weather forecasting assistant that provides current weather information given a location using emojis.",
    model_client=model_client,
    tools=[get_current_weather],
    system_message=PROMPT_AGENT_2,
    reflect_on_tool_use=True,
    model_client_stream=True,  # Enable streaming tokens from the model client.
)


user_proxy = UserProxyAgent("user_proxy")

# Build the workflow graph
builder = DiGraphBuilder()
builder.add_node(user_proxy).add_node(agent_weather_1).add_node(agent_weather_2)
builder.add_edge(user_proxy, agent_weather_1)
builder.add_edge(agent_weather_1, agent_weather_2)


# Build and validate the graph
builder.set_entry_point(user_proxy)
graph = builder.build()

# Create the flow
flow = GraphFlow([user_proxy, agent_weather_1, agent_weather_2], graph=graph)

# Use `asyncio.run(...)` and wrap the below in a async function when running in a script.
async def main() -> None:
    await Console(flow.run_stream(task="Please enter the city : "))
    # Close the connection to the model client.
    await model_client.close()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())





