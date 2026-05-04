# Streamlit Cloud Deployment Steps

## 1. Create GitHub Repository

1. Go to https://github.com/new
2. Enter repository name: `telecommunications-smb-bot`
3. Select "Public" (required for Streamlit Cloud free tier)
4. Click "Create repository"
5. Copy the repository URL (HTTPS or SSH)

## 2. Push to GitHub

Run these commands in the terminal (from the project directory):

```bash
cd "c:\Users\aloys\Documents\911 Data\telecommunications-smb-bot"

# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/telecommunications-smb-bot.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## 3. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Sign in with GitHub
4. Select:
   - Repository: `YOUR_USERNAME/telecommunications-smb-bot`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
5. Click "Deploy"

**Wait for deployment to complete (~2-3 minutes)**

## 4. Configure Secrets

After deployment:
1. Click "Advanced settings" (gear icon)
2. Go to "Secrets"
3. Add your configuration:

```toml
PINECONE_NAMESPACE = "custom_sources"
PINECONE_INDEX_HOST = "your-pinecone-index-host"
PINECONE_API_KEY = "your-pinecone-key"

OPENAI_API_KEY = "sk-your-key-here"
OPENAI_CHAT_MODEL = "gpt-4.1-mini"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
OPENAI_EMBEDDING_DIMENSIONS = "1536"
OPENAI_FINETUNED_MODEL = "ft:gpt-4.1-mini-2025-04-14:resume-ai:psap-911-custom-sources:Dbm2AJlm"
MODEL = "ft:gpt-4.1-mini-2025-04-14:resume-ai:psap-911-custom-sources:Dbm2AJlm"
MIN_SOURCE_SCORE = "0.0"
```

Important: `OPENAI_API_KEY` must belong to the same OpenAI project/account that
created the fine-tuned model. If it does not, hybrid/finetuned mode will fail
with `model_not_found`.

## 5. Get Shareable URL

Your public URL will be: 
`https://telecommunications-smb-bot.streamlit.app`

Share this link with anyone!

## Troubleshooting

- **ImportError**: Make sure all dependencies are in `requirements.txt`
- **Missing key / index errors**: Verify `OPENAI_API_KEY`, `PINECONE_API_KEY`, and `PINECONE_INDEX_HOST` are set in Streamlit secrets
- **Secrets not working**: Use `st.secrets.get("KEY_NAME", "default_value")`

## Architecture note

The Streamlit Cloud app calls OpenAI and Pinecone directly. Do not set
`API_URL` to `127.0.0.1`; that only works when a backend is running on the
same machine.
