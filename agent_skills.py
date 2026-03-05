"""
Agent Skills Write-up Generator

Generates annotated blog-style write-ups from presentations by loading the
generate-writeup prompt and the target presentation.md as agent instructions.
The agent follows the pipeline step by step using shell, file, and directory
tools, and has access to individual skills from .github/skills/ via a
FileAgentSkillsProvider.
"""

import asyncio
import os
import re
import sys
from pathlib import Path
from typing import Annotated

from agent_framework import Agent, FileAgentSkillsProvider, tool
from agent_framework.openai import OpenAIChatClient
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv(override=True)

SKILLS_DIR = Path(__file__).parent / ".github" / "skills"
PROMPT_FILE = Path(__file__).parent / ".github" / "prompts" / "generate-writeup.prompt.md"


def load_prompt() -> str:
    """Load the generate-writeup prompt, stripping YAML frontmatter."""
    text = PROMPT_FILE.read_text()
    # Strip YAML frontmatter (--- ... ---)
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    return text.strip()


# --- Tools for the agent ---


@tool(description="Run a shell command in the workspace directory and return stdout/stderr. Use for running scripts like uv run.")
async def run_shell(command: Annotated[str, "Shell command to execute"]) -> str:
    """Run a shell command and return the output."""
    workspace = Path(__file__).parent
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(workspace),
    )
    stdout, stderr = await proc.communicate()
    result = f"Exit code: {proc.returncode}\n"
    if stdout:
        result += stdout.decode()
    if stderr:
        result += "\nSTDERR:\n" + stderr.decode()
    return result


@tool(description="Read the contents of a file. Returns the full text content.")
def read_file(path: Annotated[str, "File path relative to the workspace or absolute"]) -> str:
    """Read a file and return its contents."""
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path(__file__).parent / file_path
    return file_path.read_text()


@tool(description="Write content to a file. Creates parent directories if needed.")
def write_file(
    path: Annotated[str, "File path relative to the workspace or absolute"],
    content: Annotated[str, "Content to write to the file"],
) -> str:
    """Write content to a file."""
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path(__file__).parent / file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)
    return f"Wrote {len(content)} characters to {file_path}"


@tool(description="List files and directories at a given path. Returns names, with '/' suffix for directories.")
def list_directory(path: Annotated[str, "Directory path relative to the workspace or absolute"]) -> str:
    """List contents of a directory."""
    dir_path = Path(path)
    if not dir_path.is_absolute():
        dir_path = Path(__file__).parent / dir_path
    entries = sorted(dir_path.iterdir())
    lines = []
    for entry in entries:
        if entry.name.startswith("."):
            continue
        lines.append(f"{entry.name}/" if entry.is_dir() else entry.name)
    return "\n".join(lines)


@tool(description="Check if a file or directory exists.")
def path_exists(path: Annotated[str, "File or directory path relative to the workspace or absolute"]) -> str:
    """Check whether a path exists."""
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path(__file__).parent / file_path
    return str(file_path.exists())


async def main() -> None:
    """Run the write-up generation agent."""
    if len(sys.argv) < 2:
        print("Usage: python agent_skills.py <presentation_folder>")
        print("Example: python agent_skills.py presentations/python-agents-session3")
        sys.exit(1)

    presentation_folder = sys.argv[1]

    # --- 1. Load prompt and presentation metadata ---
    prompt_instructions = load_prompt()
    presentation_md_path = Path(presentation_folder) / "presentation.md"
    if not presentation_md_path.is_absolute():
        presentation_md_path = Path(__file__).parent / presentation_md_path
    presentation_md = presentation_md_path.read_text()

    # --- 2. Create the chat client ---
    async_credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(async_credential, "https://cognitiveservices.azure.com/.default")
    client = OpenAIChatClient(
        base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/v1/",
        api_key=token_provider,
        model_id=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    )

    # --- 3. Create the skills provider ---
    skills_provider = FileAgentSkillsProvider(skill_paths=str(SKILLS_DIR))

    # --- 4. Build agent instructions from prompt + presentation metadata ---
    instructions = (
        f"{prompt_instructions}\n\n"
        f"## Presentation folder\n\n`{presentation_folder}`\n\n"
        f"## presentation.md contents\n\n{presentation_md}\n\n"
        "The workspace root is the current directory. "
        "Use cached outputs when they exist to avoid re-generating them. "
        "Follow the pipeline steps in order."
    )

    async with Agent(
        client=client,
        instructions=instructions,
        tools=[run_shell, read_file, write_file, list_directory, path_exists],
        context_providers=[skills_provider],
    ) as agent:
        prompt = f"Generate a presentation write-up for the folder: {presentation_folder}"
        print(f"Prompt: {prompt}\n")
        response = await agent.run(prompt)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
