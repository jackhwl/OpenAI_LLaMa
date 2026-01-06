import asyncio
from colorama import Fore, Style
from typing import Literal
from dotenv import load_dotenv

from openai import OpenAI # type: ignore
from agents import Agent, FileSearchTool, Runner, trace # type: ignore
from dataclasses import dataclass

from rich.console import Console # type: ignore
from utils import log_streaming_events

load_dotenv()

console = Console()

client = OpenAI()

vector_store = client.vector_stores.create(        # Create vector store
    name="Project Guidelines",
)

with open("code-review_checklist.txt", "r") as f:
    text = f.read()
    file_upload = client.files.create(
        file=("code-review_checklist.txt", text.encode("utf-8")),
        purpose="assistants",
    )
    

indexed = client.vector_stores.files.create_and_poll(
            vector_store_id=vector_store.id,
            file_id=file_upload.id
    )
       
print(Fore.BLUE + f"Stored files in vector store: {indexed.to_dict()}" + Fore.RESET)
   
developer_agent = Agent(
    name="Developer",
    instructions="You are a a skilled software developer. You write code based on the Project Guidelines and Client's request, assist with software features development, and fix bugs.",
)

code_reviewer_agent = Agent(
    name="Developer and Reviewer",
    instructions="You specialize in peer programming and code review. Your role is to review code written by other developers, provide constructive feedback, and suggest improvements based on the coding standards, project guidelines and best practices.",
    handoff_description="When the code review is complete, hand off to the lead developer for final approval.",
    tools=[FileSearchTool(
        max_num_results=3, 
        vector_store_ids=[vector_store.id], 
        include_search_results=True
    )] 
)

@dataclass
class EvaluationFeedback:
    feedback: str
    score: Literal["✅ pass", "⚠️ needs_improvement", "❌ fail"]

lead_developer_agent = Agent[None](
    name="Lead Developer",
    instructions="You are the lead developer. Oversee the project and provide guidance to other developers based on the code review checklist and project guidelines. You approve code before sending to Q&A.",
    output_type=EvaluationFeedback,
)

project_manager_orchestrator = Agent(
    name="project_manager_orchestrator",
    instructions=(
        "You are a project manager agent. You use the tools given to you to run code writing, review and approval."
        "you always use the provided tools for the tasks, never answer directly."
        "incorporation the validation and feeback format in the final response : Literal['✅ pass', '⚠️ needs_improvement', '❌ fail']"
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


console.rule("[bold Green]START OF CHAT")

async def main():
    msg = input("Hi! What feature would you want to develop? ")
    
    # Run the entire orchestration in a single trace
    with trace("Orchestrator Code Review Process"):
        orchestrator_result = Runner.run_streamed(project_manager_orchestrator, input=msg)
        await log_streaming_events(orchestrator_result)
       
        code_review_result = await Runner.run(
            project_manager_orchestrator, orchestrator_result.to_input_list()
        )

    print(Fore.GREEN + f"\n\n ====== Final response:\n{code_review_result.final_output} ======" + Fore.RESET)
    print(code_review_result.final_output)
    console.rule("[bold Blue]END OF CHAT")


if __name__ == "__main__":
    asyncio.run(main())
