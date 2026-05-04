"""
Telecommunications SMB Bot - Streamlit Cloud UI
Main entry point for Streamlit deployment (must be at root level)
"""

import streamlit as st
import requests
import json
from typing import Optional, Dict, Any

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Telecommunications SMB Bot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main { padding: 2rem; }
    .stChatMessage { padding: 1rem; }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("🛡️ Telecommunications SMB Bot")
st.markdown("""
Expert guidance on cybersecurity controls and supply chain risk management for small and medium-sized telecommunications businesses.
""")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_url = st.text_input(
        "API Endpoint",
        value=st.secrets.get("API_URL", "http://127.0.0.1:8000/chat"),
        help="Backend API URL for chat requests"
    )
    
    namespace = st.text_input(
        "Namespace",
        value=st.secrets.get("PINECONE_NAMESPACE", "custom_sources"),
        help="Pinecone namespace for document retrieval"
    )
    
    mode = st.selectbox(
        "Response Mode",
        ["base", "finetuned", "rag", "hybrid"],
        index=3,
        help="Select response generation mode"
    )
    
    model_override = st.text_input(
        "Model Override",
        value="",
        help="Leave blank to use default model"
    )
    
    top_k = st.slider(
        "Top-K Documents",
        min_value=1,
        max_value=20,
        value=8,
        help="Number of documents to retrieve for RAG"
    )
    
    st.divider()
    st.markdown("**About this bot:**")
    st.info("""
    This bot provides expert guidance on:
    - Cybersecurity controls for telecom SMBs
    - Supply chain risk management
    - Vendor security requirements
    - Access control and physical security
    """)

# Chat interface
st.markdown("### Ask a Question")

question = st.text_area(
    "Enter your question:",
    placeholder="What are the key cybersecurity controls for telecommunications SMBs?",
    height=100,
    key="question_input"
)

col1, col2 = st.columns([1, 4])

submit_button = col1.button("🔍 Ask", type="primary", use_container_width=True)
clear_button = col2.button("🗑️ Clear", use_container_width=True)

if clear_button:
    st.rerun()

# Process query
if submit_button and question.strip():
    with st.spinner("🔄 Generating response..."):
        try:
            # Prepare request
            payload = {
                "question": question,
                "namespace": namespace,
                "mode": mode,
                "top_k": top_k
            }
            
            if model_override:
                payload["model_override"] = model_override
            
            # Call backend API
            response = requests.post(
                api_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Display answer
                st.markdown("### Answer")
                st.markdown(data.get("answer", "No response received"))
                
                # Display model info
                st.markdown("### Model Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mode", mode.upper())
                with col2:
                    st.metric("Model", data.get("model", "Unknown")[:30])
                with col3:
                    st.metric("Citations", len(data.get("citations", [])))
                
                # Display citations if available
                if data.get("citations"):
                    st.markdown("### Citations")
                    for i, citation in enumerate(data["citations"], 1):
                        with st.expander(f"[{i}] {citation.get('title', 'Source')}"):
                            st.json(citation)
            else:
                st.error(f"API Error: {response.status_code}")
                st.text(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("⚠️ Cannot connect to API. Check that the backend is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.markdown("""
---
**Telecommunications SMB Bot** | Built with Streamlit | Powered by RAG & Fine-tuned LLMs
""")
