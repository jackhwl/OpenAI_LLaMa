from agents import ItemHelpers # type: ignore
from colorama import Fore
from rich.console import Console # type: ignore
from rich.pretty import Pretty # type: ignore

console = Console()

async def log_streaming_events(result):
    """Logs streaming events from the orchestrator result."""
    async for event in result.stream_events():
            # We'll ignore the raw responses event deltas
            if event.type == "raw_response_event":
                continue
            
            # When the agent updates, print that
            elif event.type == "agent_updated_stream_event":
                print(Fore.MAGENTA + f"Agent updated: {event.new_agent.name}" + Fore.RESET)
                continue
             # When items are generated, print them
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    console.print(Pretty(event))
                    print(Fore.CYAN + f"-- Tool was called: " + Fore.RESET)
                    # voir avec Logging and Tracing
                    # print(Fore.MAGENTA + {event.item} + Fore.RESET)
                    # print(Fore.MAGENTA + {event.item} + Fore.RESET)
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}")
                elif event.item.type == "message_output_item":
                    print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                else:
                    pass  # Ignore other event types
                
               
            