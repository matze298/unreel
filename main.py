"""Main Streamlit app for UnReel: A knowledge synthesis tool that curates insights from articles or topics using the Gemini API."""

import streamlit as st

from app.curator.response import generate_insights
from app.parser.url import fetch_article_content

# --- UI Layout ---
st.set_page_config(page_title="UnReel", page_icon="🧠", layout="centered")

st.title("🧠 UnReel")

# --- 2. THE PERSONAS ---
# This dictionary maps the UI selection to specific system instructions
PERSONAS = {
    "The Essentialist (Default)": "Focus on the absolute core concepts. Strip away fluff. Be concise and direct.",
    "The Pragmatist (Action-Oriented)": "Focus on 'How-to' and applicability. Convert abstract ideas into actionable steps or advice.",
    "The Skeptic (Critical Thinker)": "Analyze the ideas critically. Highlight potential flaws, counter-arguments, or edge cases where the idea fails.",
    "The Philosopher (Big Picture)": "Connect these ideas to broader mental models, historical context, or human nature.",
    "The ELI5 (Simple & Clear)": "Explain the ideas simply, as if to a 12-year-old, using analogies and metaphors.",
}

st.title("🧠 Knowledge Synthesizer")
st.caption("Curate, Expand, and Learn.")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password")
    st.markdown("---")
    selected_persona = st.selectbox("Choose Curator Persona", list(PERSONAS.keys()))
    persona_prompt = PERSONAS[selected_persona]
    st.info(f"**Persona Logic:**\n{persona_prompt}")

# Main Input Area (Tabs)
tab1, tab2 = st.tabs(["🔗 Analyze Article", "🔍 Explore Topic"])

source_content = ""
is_topic_mode = False
process = False

with tab1:
    url_input = st.text_input("Paste Article URL", placeholder="https://...")
    if st.button("Synthesize Article"):
        if not url_input:
            st.warning("Please paste a URL.")
        else:
            with st.spinner("Reading article..."):
                title, content = fetch_article_content(url_input)
                if content:
                    st.success(f"Source: {title}")
                    source_content = content
                    process = True
                    is_topic_mode = False

with tab2:
    topic_input = st.text_input("Enter a Topic", placeholder="e.g. Stoicism, Quantum Computing, Negotiation")
    if st.button("Research Topic"):
        if not topic_input:
            st.warning("Please enter a topic.")
        else:
            source_content = topic_input
            process = True
            is_topic_mode = True

# Processing & Display
if process and api_key and source_content:
    with st.spinner(f"Curating insights as '{selected_persona}'..."):
        ideas = generate_insights(
            api_key, source_content, is_topic_mode=is_topic_mode, persona_instruction=persona_prompt
        )

        if ideas:
            st.markdown("---")
            for idea in ideas:
                # Custom HTML Card
                st.markdown(
                    f"""
                    <div style="
                        background-color: #262730;
                        padding: 20px;
                        border-radius: 12px;
                        margin-bottom: 20px;
                        border: 1px solid #444;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.3);">

                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin:0; color: #FFF; font-size: 22px;">{idea["emoji"]} {idea["title"]}</h3>
                            <span style="background-color: #333; color: #4CAF50; padding: 4px 10px; border-radius: 15px; font-size: 12px; font-weight: bold;">{idea["tag"]}</span>
                        </div>

                        <p style="color: #DDD; font-size: 16px; line-height: 1.6; margin-top: 15px;">{idea["explanation"]}</p>

                        <div style="background-color: #333; padding: 10px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #FFC107;">
                            <p style="color: #FFC107; font-size: 14px; margin: 0; font-weight: bold;">🚀 Deep Dive:</p>
                            <p style="color: #EEE; font-size: 14px; margin: 5px 0 0 0; font-style: italic;">{idea.get("expansion", "")}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
elif process and not api_key:
    st.error("🔑 You must enter your Gemini API key in the sidebar first!")
