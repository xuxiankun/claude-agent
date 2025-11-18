import sys
import json
import asyncio
import random
import time
from typing import Any
from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    tool,
    create_sdk_mcp_server,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    ResultMessage,
)

# -------------------------
# Custom MCP tools for notes
# -------------------------
QUOTES = [
    "Dream big, start small -- but start.",
    "Stay curious, stay humble, keep building.",
    "Every expert was once a beginner.",
    "Small wins build momentum.",
]

notes_db = {}  # Simple in-memory store; use a real DB in production

@tool("save_note", "Save a note with the given content.", {"content": str})
async def save_note(args: dict[str, Any]) -> dict[str, Any]:
    """Save a note with the given content."""
    content = args["content"]
    note_id = len(notes_db) + 1
    notes_db[note_id] = content
    return {
        "content": [{
            "type": "text",
            "text": f"Note saved with ID: {note_id}"
        }]
    }

@tool("find_note", "Find notes matching the query.", {"query": str})
async def find_note(args: dict[str, Any]) -> dict[str, Any]:
    """Find notes matching the query."""
    query = args["query"]
    matches = [f"ID {k}: {v}" for k, v in notes_db.items() if query.lower() in v.lower()]
    result_text = "\n".join(matches) if matches else "No matching notes found."
    return {
        "content": [{
            "type": "text",
            "text": result_text
        }]
    }

@tool("get_inspirational_quote", "Get a random inspirational quote to motivate the user.", {})
async def get_inspirational_quote(args: dict[str, Any]) -> dict[str, Any]:
    """Get a random inspirational quote to motivate the user."""
    return {
        "content": [{
            "type": "text",
            "text": random.choice(QUOTES)
        }]
    }

# Create MCP server with custom tools
note_server = create_sdk_mcp_server(
    name="note_tools",
    version="1.0.0",
    tools=[save_note, find_note, get_inspirational_quote]
)

# -------------------------
# Main interactive loop
# -------------------------
async def main():
    # Agent options with system prompt for chatbot behavior
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-20250514",  # Latest Claude Sonnet 4 model
        system_prompt="""
        You are a helpful note-taking assistant. Use mcp__note_tools__save_note to save notes, 
        mcp__note_tools__find_note to search notes, and mcp__note_tools__get_inspirational_quote for motivation.
        Be concise and friendly. Commands: /help, /exit.
        """,
        mcp_servers={"note_tools": note_server},  # Pass MCP server
        allowed_tools=[
            "mcp__note_tools__save_note",
            "mcp__note_tools__find_note", 
            "mcp__note_tools__get_inspirational_quote"
        ]
    )

    print("Note-Taking Chatbot: Type 'exit' to quit.\n")

    async with ClaudeSDKClient(options=options) as client:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break

            # Send query to Claude
            await client.query(user_input)

            # Process response
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            # Typewriter effect for text
                            for char in block.text:
                                print(char, end="", flush=True)
                                await asyncio.sleep(0.05)  # Slow for effect
                            print()  # Newline
                        elif isinstance(block, ToolUseBlock):
                            print(f"\n[Tool: {block.name} called with {block.input}]")
                        elif isinstance(block, ToolResultBlock):
                            print(f"[Result: {block.content[0]['text'] if block.content else 'Executed'}]\n")
                elif isinstance(message, ResultMessage):
                    if message.is_error:
                        print(f"\nError: {message.result}")

if __name__ == "__main__":
    asyncio.run(main())