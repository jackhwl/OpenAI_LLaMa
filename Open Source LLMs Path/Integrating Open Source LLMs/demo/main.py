import os
from colorama import Fore
from dotenv import load_dotenv

from openai import OpenAI # type: ignore
import anthropic  # type: ignore
from mistralai import Mistral # type: ignore


from rich.console import Console # type: ignore
from rich.pretty import Pretty # type: ignore

 
load_dotenv()

console = Console()
console.rule("[bold blue]Pretty Object")


SYSTEM_PROMPT = "You are a skilled web development assistant who generates and explains coding tasks clearly in 1 sentence."
PROMPT = "Explain large language models pretrained vs fine-tuned in 1 sentence."

client_openai = OpenAI()
client_anthropic = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
client_mistral = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


