import asyncio
import json
from typing import TypedDict, List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

from config import Config

llm = ChatGoogleGenerativeAI(
    model=Config.MODEL_NAME,
    google_api_key=Config.GOOGLE_API_KEY,
    temperature=Config.TEMPERATURE
)

class AgentState(TypedDict):
    topic: str
    slides: List[dict]

def plan_slides(state: AgentState):
    topic = state["topic"]

    prompt = f"""Create a 5-slide presentation on {topic}.

Return STRICTLY in this format:
[
  {{
    "title": "Slide title",
    "content": ["point1", "point2", "point3"]
  }}
]

Do not add extra text."""

    # ✅ LLM call
    response = llm.invoke(prompt)

    import re
    text = response.content

    # ✅ extract JSON safely
    match = re.search(r"\[.*\]", text, re.DOTALL)

    if match:
        slides = json.loads(match.group())
    else:
        print("LLM OUTPUT:", text)  # debug
        raise ValueError("Invalid JSON")

    return {"slides": slides}

async def create_ppt(state: AgentState):
    import sys
    server = StdioServerParameters(
        command=sys.executable,
        args=["ppt_mcp_server.py"]
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            await session.call_tool(
                "create_presentation",
                {"filename": "output.pptx", "topic": state["topic"]}
            )

            for slide in state["slides"]:
                title = slide["title"]
                content = "\n".join(slide["content"])
                await session.call_tool(

                    "add_slide",
                    {
                        "title": title,
                        "content": content,
                        "topic": state["topic"]
                    }
                )

            await session.call_tool("save_presentation", {})

    return state


builder = StateGraph(AgentState)
builder.add_node("plan", plan_slides)
builder.add_node("create", create_ppt)
builder.set_entry_point("plan")
builder.add_edge("plan", "create")
builder.add_edge("create", END)

graph = builder.compile()


async def main():
    result = await graph.ainvoke({"topic": "Solar System"})
    print("PPT Created!")


if __name__ == "__main__":
    asyncio.run(main())
