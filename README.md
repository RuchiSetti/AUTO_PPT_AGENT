# 🚀 AI PPT Generator — Holo-Deck Presentations

> **Type a topic. Get a PowerPoint. Done.**  
> An AI-powered multi-agent pipeline that turns any topic into a fully styled `.pptx` file — no manual slide work, ever.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-green?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-Tool%20Server-purple?style=flat-square)
![Gemini](https://img.shields.io/badge/Google-Gemini-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 What Is This?

This project is a **multi-agent AI system** that generates a complete PowerPoint presentation from just a topic string. You type *"Solar System"* or *"Machine Learning Basics"* — and the system plans the slides, writes the content, designs the layout, and exports a `.pptx` file, all on its own.

It's built using **LangGraph for agent orchestration**, **Google Gemini** as the LLM brain, **MCP (Model Context Protocol)** as the tool execution layer, and **python-pptx** to actually build the file. A **Streamlit** frontend ties it all together with a live preview.

---

## 🏗️ Architecture

The system is split into **3 clear layers**. Each layer has one job and hands off to the next.

```
┌─────────────────────────────────────────────┐
│           LAYER 1 — Frontend                │
│              Streamlit UI                   │
│   (User input → live preview → download)    │
└─────────────────┬───────────────────────────┘
                  │  topic string
                  ▼
┌─────────────────────────────────────────────┐
│         LAYER 2 — Agent Brain               │
│          LangGraph (StateGraph)             │
│                                             │
│   ┌─────────────┐     ┌─────────────────┐   │
│   │ plan_slides │────▶│   create_ppt    │   │
│   │ (Gemini LLM)│     │  (calls MCP)    │   │
│   └─────────────┘     └────────┬────────┘   │
└────────────────────────────────┼────────────┘
                                 │  tool calls (stdio)
                                 ▼
┌─────────────────────────────────────────────┐
│         LAYER 3 — Tool Execution            │
│          MCP Server (FastMCP)               │
│                                             │
│   create_presentation()                     │
│   add_slide()  ×5                           │
│   save_presentation()                       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         📄 output.pptx
         (ppt_storage/)
```

---

## 🔄 Full Flow — Step by Step

Here's exactly what happens from the moment you hit **Generate**:

```
User types topic
       │
       ▼
  Streamlit (app.py)
  calls graph.astream()
       │
       ▼
  LangGraph Agent
  ┌────────────────────────────────────────┐
  │  Node 1: plan_slides()                 │
  │  → Sends prompt to Google Gemini       │
  │  → Gemini returns 5 slides as JSON     │
  │    [{title, content:[...]}, ...]       │
  └────────────────────┬───────────────────┘
                       │  slides[] stored in AgentState
                       ▼
  ┌────────────────────────────────────────┐
  │  Node 2: create_ppt()                  │
  │  → Spins up ppt_mcp_server.py          │
  │    as a subprocess (stdio transport)   │
  │  → Calls create_presentation tool      │
  │  → Loops through each slide            │
  │    → Calls add_slide tool per slide    │
  │  → Calls save_presentation tool        │
  └────────────────────┬───────────────────┘
                       │
                       ▼
  MCP Server (ppt_mcp_server.py)
  → python-pptx builds the PPTX
  → Background image applied to each slide
  → Gold title + white bullets styled
  → Saves to ppt_storage/output.pptx
                       │
                       ▼
  Streamlit renders glassmorphism slide previews
  User hits download → gets the .pptx
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | UI, live preview, download button |
| LLM | Google Gemini (via LangChain) | Slide content planning & generation |
| Agent | LangGraph (StateGraph) | Orchestrates plan → build pipeline |
| Tool Protocol | MCP (FastMCP, stdio) | Agent ↔ tool server communication |
| PPT Engine | python-pptx | Builds the actual `.pptx` file |
| Config | Python class | API keys, model name, temperature |

---

## 📁 Project Structure

```
ai-ppt-generator/
│
├── app.py                  # Streamlit UI — entry point
├── agent_ppt.py            # LangGraph agent (plan + create nodes)
├── ppt_mcp_server.py       # MCP tool server (PPTX creation logic)
├── config.py               # API keys + model config (you create this)
├── test_slide.py           # Quick test script for pptx rendering
├── requirements.txt        # Python dependencies
│
├── assets/
│   └── space.png           # Background image for every slide
│
└── ppt_storage/            # Generated PPTX files land here
    └── output.pptx
```

---

## ⚙️ Setup & Running

### Prerequisites

- Python 3.10+
- A Google Gemini API key — [get one free here](https://aistudio.google.com/app/apikey)

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/your-username/ai-ppt-generator.git
cd ai-ppt-generator
```

### Step 2 — Install dependencies

```bash
pip install streamlit langchain-google-genai langgraph mcp python-pptx
```

Or if `requirements.txt` is populated:

```bash
pip install -r requirements.txt
```

### Step 3 — Create `config.py`

Create a file called `config.py` in the root folder:

```python
class Config:
    GOOGLE_API_KEY = "your-google-gemini-api-key-here"
    MODEL_NAME = "gemini-1.5-flash"
    TEMPERATURE = 0.7
```

### Step 4 — Add a background image

Create an `assets/` folder and drop any 16:9 image in as `space.png`:

```bash
mkdir assets
# Copy your background image → assets/space.png
```

### Step 5 — Create the output folder

```bash
mkdir ppt_storage
```

### Step 6 — Run the app

```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🖥️ UI Preview

```
┌──────────────────────────────────────────────────────────────┐
│  Sidebar                │  Main Content Area                 │
│  ───────────────────    │  ─────────────────────────────     │
│                         │                                    │
│  ⚡ AI PPT Generator    │   ✨ HOLO-DECK PRESENTATIONS ✨    │
│                         │      (animated neon header)        │
│  Generate a full PPT    │                                    │
│  from just a topic.     │  ┌────────────────────────────┐   │
│                         │  │  🔵 Status: Planning...     │   │
│  Enter a topic:         │  └────────────────────────────┘   │
│  [_________________ ]   │                                    │
│                         │  ┌──────────┐   ┌──────────┐     │
│  [🚀 Generate Pres.. ]  │  │ Slide 1  │   │ Slide 2  │     │
│                         │  │──────────│   │──────────│     │
│  ─────────────────      │  │ • Point  │   │ • Point  │     │
│  Built with             │  │ • Point  │   │ • Point  │     │
│  LangChain + MCP        │  │ • Point  │   │ • Point  │     │
│  + Streamlit            │  └──────────┘   └──────────┘     │
│                         │                                    │
│                         │   [ ⬇️  Download PPT as .pptx ]   │
└──────────────────────────────────────────────────────────────┘
```

**What the UI includes:**
- Dark cyberpunk / glassmorphism visual theme
- Real-time status updates during each generation phase
- 2-column grid with a preview card per slide
- One-click `.pptx` download once generation is done

---

## 🧠 Key Design Decisions

**Why MCP instead of calling python-pptx directly in the agent?**

MCP creates a clean boundary between the *thinking* layer and the *doing* layer. The agent doesn't know or care how PowerPoints are built — it just calls named tools. This also means you could swap the tool server entirely (use Google Slides API, for example) without touching the agent code.

**Why LangGraph instead of plain LangChain?**

LangGraph lets you define explicit nodes and edges. For this pipeline the order is strict — you *must* plan before you build. A `StateGraph` with `plan → create → END` makes that constraint explicit and gives streaming state output so the UI can update in real time.

**Why stdio transport for MCP?**

The MCP server runs as a subprocess. No network ports, no auth, no setup. The agent spawns it, uses it, and it shuts down. Clean and self-contained.

---

## 🔧 Customization

**Change number of slides**

Edit the prompt string in `plan_slides()` inside `agent_ppt.py` — change *"5-slide"* to whatever you want.

**Use a different LLM**

Swap `ChatGoogleGenerativeAI` for any LangChain-compatible model:

```python
# OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", api_key="...")

# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key="...")

# Local via Ollama
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3")
```

**Change slide design**

All colors, fonts, and layout live in `add_slide()` inside `ppt_mcp_server.py`. Look for `RGBColor`, `Pt()`, and `Inches()` calls — those control everything visual.

**Topic-based backgrounds**

`add_slide()` already receives the `topic` parameter. You can map topics to different images in `assets/` and load them conditionally based on keywords.

---

## ⚠️ Known Issues

- The MCP server uses a global `ppt` object. If the server crashes mid-generation, restart the Streamlit app before retrying.
- Streamlit's `asyncio.run()` can clash with existing event loops in some environments. Fix: `pip install nest_asyncio` and add `nest_asyncio.apply()` at the top of `app.py`.
- The output filename is hardcoded as `output.pptx` — running two generations quickly overwrites the first. Add a timestamp to the filename if you want to keep multiple outputs.

---

## 🏷️ Tags

`AI` · `LangChain` · `LangGraph` · `MCP` · `Streamlit` · `PPT-Generator` · `Google-Gemini` · `python-pptx` · `Multi-Agent` · `Generative-AI`

---

## 📄 License

MIT — use it, modify it, build on it.

---

*Built to skip the boring part of making presentations.*