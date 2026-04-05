# AI PPT Generator

Type a topic. Get a PowerPoint.

This is a multi-agent AI system that generates a complete PowerPoint presentation from just a topic string. You type "Solar System" or "Machine Learning Basics" — and the system plans the slides, writes the content with bullet points, designs the layout, and exports a `.pptx` file, all on its own. Each presentation is 5 slides, with a title and 3–5 bullet points per slide, styled with a custom background.



---

## How it works

```
Your topic
    ↓
Gemini (plans 5 slides + bullet points)
    ↓
LangGraph (orchestrates the flow)
    ↓
MCP Server (builds the actual file)
    ↓
output.pptx
```

The frontend is a Streamlit app — type, generate, preview, download.

---

## Tech stack

| What | Why |
|---|---|
| Streamlit | Frontend UI |
| Google Gemini | Slide content generation |
| LangChain | LLM interface |
| LangGraph | Agent orchestration |
| MCP (FastMCP) | Tool server communication |
| python-pptx | PowerPoint file creation |

---

## Installation

Step 1 — Clone the repo

```bash
git clone https://github.com/your-username/ai-ppt-generator.git
cd ai-ppt-generator
```

Step 2 — Install dependencies

```bash
pip install streamlit langchain-google-genai langgraph mcp python-pptx
```

Or if `requirements.txt` is populated:

```bash
pip install -r requirements.txt
```

Step 3 — Create `config.py`

Create a file called `config.py` in the root folder:

```python
class Config:
    GOOGLE_API_KEY = "your-google-gemini-api-key-here"
    MODEL_NAME = "gemini-1.5-flash"
    TEMPERATURE = 0.7
```

Step 4 — Add a background image

Create an `assets/` folder and drop any 16:9 image in as `space.png`:

```bash
mkdir assets
# Copy your background image → assets/space.png
```

Step 5 — Create the output folder

```bash
mkdir ppt_storage
```

Step 6 — Run the app

```bash
streamlit run app.py
```
```bash
Open your browser at **http://localhost:8501**
```

```bash
Demo Link: **https://youtu.be/FtO1bSt0JQ8**
```

---

## License

MIT — use it, modify it, build on it.

