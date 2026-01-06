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

project_manager_orchestrator = Agent(
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
    msg = input("Hi! What feature would you want to develop? ")

    # Run the entire orchestration in a single trace
    with trace("Orchestrator evaluator"):
        orchestrator_result = Runner.run_streamed(project_manager_orchestrator, input=msg)

        async for event in orchestrator_result.stream_events():
        # We'll ignore the raw responses event deltas
       
    
            if event.type == "raw_response_event":
                continue
            
            # When the agent updates, print that
            elif event.type == "agent_updated_stream_event":
                print(Fore.MAGENTA + f"Agent updated: {event.new_agent.name}" + Fore.RESET)
                continue
            elif event.type == "response.output_text.delta":
                print(Fore.CYAN + f"Output: {event.new_agent.name}" + Fore.RESET)
                continue
            # When items are generated, print them
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print(Fore.YELLOW + "-- Tool was called" + Fore.RESET)
                elif event.item.type == "tool_call_output_item":
                    print(Fore.YELLOW + f"-- Tool output: {event.item.output}" + Fore.RESET)
                elif event.item.type == "message_output_item":
                    print(Fore.YELLOW + f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}" + Fore.RESET)
                else:
                    pass  # Ignore other event types

        synthesizer_result = await Runner.run(
            project_manager_orchestrator, orchestrator_result.to_input_list()
        )

    print(f"\n\nFinal response:\n{synthesizer_result.final_output}")
    console.rule("[bold Blue]END OF CHAT")
    
if __name__ == "__main__":
    asyncio.run(main())
