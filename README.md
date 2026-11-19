# Pipeline Agent

> 📘 **Guide:** [HOW_TO_USE.md](HOW_TO_USE.md) · 🎨 Open [architecture.html](architecture.html) for an interactive walkthrough.

A lightweight content factory built with **LangChain + LangGraph + Ollama**: outline → write → edit → headline → measure.

- **LLM**: Ollama (local, free) — default `llama3.2`
- **Tools**: `count_words`, `reading_time`, `clean_text` (plain Python helpers in `tools.py`)
- **Architecture**: **Pipeline (assembly line)** — agents execute in a fixed linear sequence, each passing its output to the next via state.

```
START ─► outliner ─► writer ─► editor ─► headline ─► quality_gate ─► END
          (LLM)      (LLM)     (LLM)     (LLM)      (plain code)
```

## Quickstart

### 1. Web App (Streamlit)
```bash
pip install -r requirements.txt
ollama pull llama3.2
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

### 2. Terminal CLI
```bash
python agent.py
```

### 3. Architecture Walkthrough in Browser
Double-click `architecture.html` or run:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000/architecture.html`.

## Example Inputs
- Why sleep matters
- Learning to cook
- Benefits of walking
- How volcanoes work
