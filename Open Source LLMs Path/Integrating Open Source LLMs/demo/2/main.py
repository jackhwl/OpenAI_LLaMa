import asyncio
from colorama import Fore, Style
from dotenv import load_dotenv

from openai import OpenAI # type: ignore
from agents import Agent, ItemHelpers, MessageOutputItem, Runner, trace # type: ignore

from rich.console import Console # type: ignore

load_dotenv()

console = Console()

developer_agent = Agent(
    name="developer_agent",
    instructions="You are a skilled software developer. You write code based on the Project Guidelines and Client's request, assist with software features development, and fix bugs.",
    handoff_description="When the coding task is complete, hand off to code reviewer.",
)

code_reviewer_agent = Agent(
    name="code_reviewer_agent",
    instructions="You specialize in peer programming and code review. Your role is to review code written by other developers, provide constructive feedback, and suggest improvements based on the coding standards, project guidelines, and best practices.",
    handoff_description="When the code review is complete, hand off to the lead developer for final approval.",
)

lead_developer_agent = Agent(
    name="lead_developer_agent",
    instructions="You are the lead developer. Oversee the project and provide guidance to other developers based on the code review checklist and project guidelines. You give final approval on code before it is merged into the main codebase.",
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        developer_agent.as_tool(
            tool_name="developer_tool",
            tool_description="A tool to write code, assist with software features development, and fix bugs.",
        ),
        code_reviewer_agent.as_tool(
            tool_name="code_reviewer_tool",
            tool_description="A tool to assist with code review and provide feedback.",
        ),
        lead_developer_agent.as_tool(
            tool_name="lead_developer_tool",
            tool_description="A tool to oversee the project, provide guidance to the development team and approve code.",
        ),
    ],
)

client_openai = OpenAI()


console.rule("[bold Green]START OF CHAT")

async def main():
    """Main function to run the orchestrator example."""
    pass

    console.rule("[bold Blue]END OF CHAT")


if __name__ == "__main__":
    asyncio.run(main())
