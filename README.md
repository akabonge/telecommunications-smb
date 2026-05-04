# Telecommunications SMB Bot

Expert guidance on cybersecurity controls and supply chain risk management for small and medium-sized telecommunications businesses.

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd telecommunications-smb-bot
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

The app will open at `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select this repository, branch, and `streamlit_app.py` as the main file
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to App settings → Secrets
   - Add your API configuration:
     ```
     API_URL = "https://your-api-endpoint.com/chat"
     PINECONE_NAMESPACE = "custom_sources"
     OPENAI_API_KEY = "sk-..."
     PINECONE_API_KEY = "..."
     ```

## 📁 Project Structure

```
.
├── streamlit_app.py              # Main Streamlit UI (entry point)
├── requirements.txt              # Python dependencies
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── .env.example                 # Environment variables template
├── backend/                     # Backend API (optional)
│   ├── main.py                 # FastAPI application
│   ├── rag_core.py             # RAG logic
│   └── config.py               # Backend configuration
├── app/                         # UI components (if modularized)
│   ├── pages/                  # Streamlit pages
│   └── utils.py                # Utility functions
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# API Configuration
API_URL=http://localhost:8000/chat
PINECONE_NAMESPACE=custom_sources

# Model Configuration
MODE=hybrid
MODEL=ft:gpt-4.1-mini-2025-04-14:resume-ai:psap-911-custom-sources:Dbm2AJlm
TOP_K=8

# API Keys
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
```

### Streamlit Cloud Secrets

In production (Streamlit Cloud), add secrets in the app settings:
- Never commit `.env` files
- Use Streamlit's secrets management

## 🎯 Features

- **Hybrid RAG Mode**: Combines fine-tuned models with retrieval-augmented generation
- **Citation Support**: Each answer includes source citations
- **Configurable**: Switch between base, fine-tuned, RAG, and hybrid modes
- **Custom Namespace**: Query specific document collections
- **Shareable URL**: Public Streamlit Cloud deployment

## 🔗 API Integration

The Streamlit app communicates with a backend API:

```python
POST /chat
{
  "question": "string",
  "namespace": "string",
  "mode": "base|finetuned|rag|hybrid",
  "top_k": 8,
  "model_override": "string (optional)"
}
```

Response:
```json
{
  "answer": "string",
  "model": "string",
  "citations": [...]
}
```

## 📊 Technologies

- **Frontend**: Streamlit
- **Backend**: FastAPI (optional)
- **Vector DB**: Pinecone
- **Embeddings**: OpenAI
- **LLM**: GPT-4.1 Mini (fine-tuned)
- **Deployment**: Streamlit Cloud

## 🛠️ Development

### Adding Pages

Create new Streamlit pages in `app/pages/`:

```python
# app/pages/1_Sources.py
import streamlit as st

st.title("Sources")
# Page content
```

### Customization

- Modify `streamlit_app.py` for UI changes
- Update `.streamlit/config.toml` for theming
- Add dependencies to `requirements.txt`

## 📝 Notes

- The `streamlit_app.py` file must be at the root for Streamlit Cloud to find it
- Use `st.secrets` to access environment variables in Streamlit Cloud
- Keep sensitive API keys in `.env` locally and in Streamlit Cloud secrets in production

## 🚢 Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Secrets configured in Streamlit Cloud
- [ ] API endpoint accessible
- [ ] `.env` file in `.gitignore`
- [ ] README updated with deployment instructions
- [ ] Test app locally before pushing

## 📧 Support

For issues or questions, check the logs in Streamlit Cloud dashboard or run locally with:

```bash
streamlit run streamlit_app.py --logger.level=debug
```

---

**Telecommunications SMB Bot** - Expert guidance for telecom security and supply chain risk management
