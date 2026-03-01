"""
Agent Skills Write-up Generator

Uses file-based Agent Skills with a FileAgentSkillsProvider to generate
annotated blog-style write-ups from presentations. The agent loads the
generate-writeup skill and orchestrates the pipeline using shell, file,
and directory tools.

Skills are discovered from .github/skills/ and follow progressive disclosure:
1. Advertise — skill names/descriptions injected into system prompt
2. Load — full instructions loaded on-demand via load_skill tool
3. Read resources — supplementary files read via read_skill_resource tool
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Annotated

from agent_framework import Agent, FileAgentSkillsProvider, tool
from agent_framework.openai import OpenAIChatClient
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv(override=True)

SKILLS_DIR = Path(__file__).parent / ".github" / "skills"


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

    # --- 1. Create the chat client ---
    async_credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(async_credential, "https://cognitiveservices.azure.com/.default")
    client = OpenAIChatClient(
        base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/v1/",
        api_key=token_provider,
        model_id=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    )

    # --- 2. Create the skills provider ---
    skills_provider = FileAgentSkillsProvider(skill_paths=str(SKILLS_DIR))

    # --- 3. Create the agent with skills and tools ---
    instructions = (
        "You are a presentation write-up generator. "
        "You have access to agent skills that define how to generate write-ups from presentations. "
        "You also have tools for running shell commands, reading/writing files, and listing directories. "
        "When asked to generate a write-up, load the generate-writeup skill and follow its instructions step by step. "
        "Use cached outputs when they exist to avoid re-generating them. "
        "The workspace root is the current directory."
    )

    async with Agent(
        client=client,
        instructions=instructions,
        tools=[run_shell, read_file, write_file, list_directory, path_exists],
        context_providers=[skills_provider],
    ) as agent:
        prompt = f"Generate a presentation write-up for {presentation_folder}"
        print(f"Prompt: {prompt}\n")
        response = await agent.run(prompt)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
