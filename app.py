"""
Pipeline Agent — Streamlit Web UI
---------------------------------
Web interface for the LangGraph 4-agent assembly line pipeline.
Run with: streamlit run app.py
"""

import os
import streamlit as st
import streamlit.components.v1 as components
from agent import build_agent, State, OLLAMA_MODEL

st.set_page_config(
    page_title="Pipeline Agent — Content Factory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1a2234;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #2d3748;
        margin-bottom: 12px;
    }
    .step-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .headline-text {
        font-size: 1.8rem;
        font-weight: 800;
        color: #67e8f9;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .article-body {
        font-size: 1.1rem;
        line-height: 1.7;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.title("🏭 Pipeline Agent")
    st.caption("Linear Multi-Agent Content Factory")
    st.markdown("---")
    
    st.subheader("⚙️ Settings")
    model_name = st.text_input("Ollama Model", value=OLLAMA_MODEL, help="Ensure this model is pulled locally via 'ollama pull <model>'")
    temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
    
    st.markdown("---")
    st.subheader("📋 Assembly Line Steps")
    st.markdown("""
    1. 🗂️ **Outliner** — 3-point outline
    2. ✍️ **Writer** — ~120-word draft
    3. 🧹 **Editor** — clarity & grammar
    4. 📰 **Headline** — catchy ≤10 words
    5. 📏 **Quality Gate** — word count & read time *(Code only, no AI)*
    """)
    
    st.markdown("---")
    st.info("💡 **Ollama Required:** Make sure Ollama is running (`ollama serve` or desktop app).")

# ----------------- MAIN TABS -----------------
tab_app, tab_arch = st.tabs(["🚀 Run Pipeline", "🎨 Architecture Diagram"])

with tab_app:
    st.subheader("Create a Blog Post with Multi-Agent Pipeline")
    st.markdown("Type a topic below or click a sample topic to watch the assembly line run sequentially.")

    # Sample topic quick buttons
    col1, col2, col3, col4 = st.columns(4)
    if "topic_input" not in st.session_state:
        st.session_state.topic_input = "Why sleep matters"

    if col1.button("😴 Why sleep matters"):
        st.session_state.topic_input = "Why sleep matters"
    if col2.button("🍳 Learning to cook"):
        st.session_state.topic_input = "Learning to cook"
    if col3.button("🚶 Benefits of walking"):
        st.session_state.topic_input = "Benefits of walking"
    if col4.button("🌋 How volcanoes work"):
        st.session_state.topic_input = "How volcanoes work"

    topic = st.text_input("Blog topic:", value=st.session_state.topic_input, placeholder="e.g. The future of renewable energy")

    run_btn = st.button("🚀 Generate Post", type="primary", use_container_width=True)

    if run_btn:
        if not topic.strip():
            st.warning("Please enter a blog topic.")
        else:
            progress_bar = st.progress(0, text="Initializing assembly line...")
            
            # Container for live step updates
            with st.status("🏭 Processing blog post through the assembly line...", expanded=True) as status:
                try:
                    agent = build_agent(model=model_name, temperature=temperature)
                    initial_state: State = {
                        "topic": topic,
                        "outline": "",
                        "draft": "",
                        "edited": "",
                        "headline": "",
                        "report": ""
                    }
                    
                    collected_state = dict(initial_state)

                    step_info = {
                        "outliner": ("1/5 🗂️ Outliner", 20, "Outliner: Planning the 3-point structure..."),
                        "writer": ("2/5 ✍️ Writer", 40, "Writer: Drafting ~120 words following outline..."),
                        "editor": ("3/5 🧹 Editor", 60, "Editor: Polishing clarity, grammar, and flow..."),
                        "headline": ("4/5 📰 Headline Writer", 80, "Headline: Crafting a punchy headline..."),
                        "quality_gate": ("5/5 📏 Quality Gate", 100, "Quality Gate: Calculating word count and reading time..."),
                    }

                    for update in agent.stream(initial_state):
                        for node_name, state_patch in update.items():
                            collected_state.update(state_patch)
                            if node_name in step_info:
                                label, pct, desc = step_info[node_name]
                                progress_bar.progress(pct, text=f"{label} finished")
                                st.write(f"✅ **{label}**: {desc}")

                    status.update(label="🎉 Pipeline Complete!", state="complete", expanded=False)
                    progress_bar.progress(100, text="Finished!")

                    # Display the final post
                    st.markdown("---")
                    st.markdown(f"<div class='headline-text'># {collected_state['headline']}</div>", unsafe_allow_html=True)
                    
                    mcol1, mcol2, mcol3 = st.columns(3)
                    words_count = len(collected_state["edited"].split())
                    mcol1.metric("Word Count", f"{words_count} words")
                    mcol2.metric("Reading Time", collected_state["report"].split("·")[-1].replace("reading time", "").strip())
                    mcol3.metric("Pipeline Agent Order", "5 / 5 steps executed")

                    st.markdown("### Published Blog Post")
                    st.markdown(f"<div class='article-body'>{collected_state['edited']}</div>", unsafe_allow_html=True)

                    st.markdown(f"*{collected_state['report']}*")

                    # Step-by-step intermediate inspection
                    st.markdown("---")
                    with st.expander("🔍 Inspect Intermediate Outputs (Step-by-Step Evolution)", expanded=False):
                        tab1, tab2, tab3, tab4 = st.tabs(["1. Outline", "2. First Draft", "3. Edited Version", "4. Full State (JSON)"])
                        with tab1:
                            st.markdown("#### 🗂️ Outline created by Outliner")
                            st.text(collected_state["outline"])
                        with tab2:
                            st.markdown("#### ✍️ First Draft written by Writer")
                            st.text(collected_state["draft"])
                        with tab3:
                            st.markdown("#### 🧹 Polished Draft by Editor")
                            st.text(collected_state["edited"])
                        with tab4:
                            st.json(collected_state)

                except Exception as e:
                    status.update(label="❌ Pipeline Error", state="error", expanded=True)
                    st.error(f"Error during execution: {e}")
                    st.info("Check that Ollama is running and that the model is downloaded (`ollama pull " + model_name + "`).")

with tab_arch:
    st.subheader("Interactive Architecture Walkthrough")
    st.caption("Click through the steps below to see how state passes through each agent on the assembly line.")
    html_file = os.path.join(os.path.dirname(__file__), "architecture.html")
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=680, scrolling=True)
    else:
        st.warning("architecture.html not found.")
