"""Telecommunications SMB Bot - Streamlit Cloud UI."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from backend.rag_core import BotConfig, answer_question


load_dotenv()

st.set_page_config(
    page_title="Telecommunications SMB Bot",
    page_icon="Shield",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
    .main { padding: 2rem; }
    .stChatMessage { padding: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Telecommunications SMB Bot")
st.markdown(
    "Expert guidance on cybersecurity controls and supply chain risk management "
    "for small and medium-sized telecommunications businesses."
)


def _setting(name: str, default: str = "") -> str:
    return str(st.secrets.get(name, os.getenv(name, default)) or "")


def _int_setting(name: str, default: int) -> int:
    try:
        return int(_setting(name, str(default)))
    except ValueError:
        return default


def _float_setting(name: str, default: float) -> float:
    try:
        return float(_setting(name, str(default)))
    except ValueError:
        return default


def _bot_config() -> BotConfig:
    return BotConfig(
        openai_api_key=_setting("OPENAI_API_KEY"),
        pinecone_api_key=_setting("PINECONE_API_KEY"),
        pinecone_index_host=_setting("PINECONE_INDEX_HOST"),
        pinecone_index=_setting("PINECONE_INDEX"),
        embedding_model=_setting("OPENAI_EMBEDDING_MODEL", _setting("OPENAI_EMBED_MODEL", "text-embedding-3-small")),
        embedding_dimensions=_int_setting("OPENAI_EMBEDDING_DIMENSIONS", 1536),
        chat_model=_setting("OPENAI_CHAT_MODEL", "gpt-4.1-mini"),
        finetuned_model=_setting("OPENAI_FINETUNED_MODEL", _setting("MODEL")),
        min_source_score=_float_setting("MIN_SOURCE_SCORE", 0.0),
    )


with st.sidebar:
    st.header("Configuration")

    namespace = st.text_input(
        "Namespace",
        value=_setting("PINECONE_NAMESPACE", "custom_sources"),
        help="Pinecone namespace for document retrieval",
    )

    mode = st.selectbox(
        "Response Mode",
        ["base", "finetuned", "rag", "hybrid"],
        index=3,
        help="Select response generation mode",
    )

    model_override = st.text_input(
        "Model Override",
        value="",
        help="Leave blank to use the configured fine-tuned model",
    )

    top_k = st.slider(
        "Top-K Documents",
        min_value=1,
        max_value=20,
        value=8,
        help="Number of documents to retrieve for RAG",
    )

    st.divider()
    st.markdown("**About this bot:**")
    st.info(
        "This bot provides expert guidance on cybersecurity controls, vendor security, "
        "supply chain risk management, access control, and physical security for telecom SMBs."
    )


st.markdown("### Ask a Question")

question = st.text_area(
    "Enter your question:",
    placeholder="What are the key cybersecurity controls for telecommunications SMBs?",
    height=100,
    key="question_input",
)

col1, col2 = st.columns([1, 4])
submit_button = col1.button("Ask", type="primary", use_container_width=True)
clear_button = col2.button("Clear", use_container_width=True)

if clear_button:
    st.rerun()

if submit_button and question.strip():
    with st.spinner("Generating response..."):
        try:
            data = answer_question(
                question=question,
                namespace=namespace,
                mode=mode,
                top_k=top_k,
                config=_bot_config(),
                model_override=model_override or None,
            )

            st.markdown("### Answer")
            if data.get("model_note"):
                st.warning(data["model_note"])
            st.markdown(data.get("answer", "No response received"))

            st.markdown("### Model Information")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Mode", mode.upper())
            with metric_col2:
                st.metric("Model", data.get("model", "Unknown")[:30])
            with metric_col3:
                st.metric("Citations", len(data.get("citations", [])))

            if data.get("citations"):
                st.markdown("### Citations")
                for index, citation in enumerate(data["citations"], start=1):
                    with st.expander(f"[{index}] {citation.get('title', 'Source')}"):
                        st.json(citation)

        except Exception as exc:
            st.error(f"Error: {exc}")

st.divider()
st.markdown(
    "**Telecommunications SMB Bot** | Built with Streamlit | "
    "Powered by RAG and a fine-tuned model"
)
