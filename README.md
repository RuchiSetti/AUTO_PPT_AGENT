# 🚀 AI PPT Generator — Turn Any Topic into a Presentation in Seconds

Ever had to make a PowerPoint at the last minute and just... didn't want to? Yeah, that's exactly why I built this.

This project takes a topic you type in, sends it through an AI agent, and spits out a fully designed `.pptx` file — complete with a custom background, styled slides, gold titles, and bullet points. You don't touch a single slide manually.

---

## What It Actually Does

You type something like *"The Future of AI in Space"* and hit Generate. Here's what happens behind the scenes:

1. **Google Gemini** reads your topic and plans out 5 slides — each with a proper title and 3–5 bullet points.
2. **LangGraph** orchestrates the whole flow — first plan, then build. It's basically an agent that has two jobs and does them in order.
3. **A local MCP server** (`ppt_mcp_server.py`) handles the actual PowerPoint creation. It's a small tool server that receives commands like "add this slide" and does the dirty work with `python-pptx`.
4. The finished `.pptx` lands in a `ppt_storage/` folder, and Streamlit shows you a live preview of every slide before you download it.

The UI is a Streamlit app with a cyberpunk/glassmorphism look — dark gradients, glowing text, floating cards for each slide. It's a bit extra, intentionally.

---

## Project Structure

```
├── app.py                  # Streamlit frontend — the UI you interact with
├── agent_ppt.py            # LangGraph agent — plans slides, then calls the MCP server
├── ppt_mcp_server.py       # MCP tool server — creates and saves the actual PPTX file
├── config.py               # Your API keys and model settings (you create this)
├── assets/
│   └── space.png           # Background image used on every slide
├── ppt_storage/            # Where the generated PPTX files are saved
└── requirements.txt        # Python dependencies
```

---

## How to Set It Up

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-ppt-generator.git
cd ai-ppt-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

The key packages you need are:

```
streamlit
langchain-google-genai
langgraph
mcp
python-pptx
```

If `requirements.txt` is empty (oops), just run:

```bash
pip install streamlit langchain-google-genai langgraph mcp python-pptx
```

### 3. Create your `config.py`

Make a file called `config.py` in the root folder with this:

```python
class Config:
    GOOGLE_API_KEY = "your-google-gemini-api-key-here"
    MODEL_NAME = "gemini-1.5-flash"   # or whichever Gemini model you're using
    TEMPERATURE = 0.7
```

You can get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Add your background image

Drop an image named `space.png` into an `assets/` folder. It'll be used as the background on every slide. Any 16:9 image works — space, abstract gradients, dark textures, whatever fits your vibe.

### 5. Create the output folder

```bash
mkdir ppt_storage
```

### 6. Run it

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and you're good to go.

---

## Using It

Once the app is running:

- Type your topic in the sidebar (e.g. *"Climate Change"*, *"Machine Learning Basics"*, *"History of the Roman Empire"*)
- Hit **Generate Presentation**
- Watch the status bar — it'll tell you what's happening (planning, generating, compiling)
- Slide previews show up in the main area once done
- Hit the download button to grab your `.pptx`

That's it. The whole thing usually takes 10–20 seconds depending on API response times.

---

## How the Code Connects

If you want to understand what's talking to what:

```
app.py  →  agent_ppt.py (LangGraph graph)
               ├── plan_slides()   →  Gemini API (generates slide content)
               └── create_ppt()   →  ppt_mcp_server.py (via MCP stdio)
                                       ├── create_presentation()
                                       ├── add_slide()  (×5)
                                       └── save_presentation()
```

The MCP server runs as a subprocess — `agent_ppt.py` spins it up, sends tool calls to it over stdin/stdout, and shuts it down when done. It's a clean separation: the agent doesn't care *how* the PPTX gets made, and the server doesn't care *what* the topic is.

---

## Customizing It

**Want a different background per topic?**  
In `ppt_mcp_server.py`, the `add_slide()` function receives the `topic` parameter. You could map topics to different images in `assets/` and swap them conditionally.

**Want more or fewer slides?**  
Change the `5-slide` instruction in the `plan_slides()` prompt inside `agent_ppt.py`.

**Want different fonts or colors?**  
Edit `add_slide()` in `ppt_mcp_server.py` — that's where all the `RGBColor`, `Pt()`, and font settings live.

**Want to use a different LLM?**  
Swap out `ChatGoogleGenerativeAI` in `agent_ppt.py` for any LangChain-compatible model (OpenAI, Anthropic, Ollama, etc.) and update `config.py` accordingly.

---

## Known Quirks

- The MCP server is stateful (uses a global `ppt` variable), so if something crashes mid-generation, you might need to restart. It's fine for this use case but worth knowing.
- Streamlit's `asyncio.run()` can occasionally throw a "event loop already running" error in certain environments. If that happens, try running with `nest_asyncio` or use a fresh terminal.
- The slides always use the same `space.png` background regardless of topic — intentional for now, easy to change if you want.

---

## Built With

- [Streamlit](https://streamlit.io/) — UI framework
- [LangChain + Google Gemini](https://python.langchain.com/) — LLM integration
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Agent orchestration
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) — Tool server communication
- [python-pptx](https://python-pptx.readthedocs.io/) — PowerPoint generation

---

## Contributing

If you want to add features — multi-language support, different slide templates, better error handling, whatever — feel free to fork and open a PR. The codebase is small and pretty readable, shouldn't take long to get oriented.

---

*Built to skip the boring parts of making presentations.*