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

```
API_URL = "http://127.0.0.1:8000/chat"
PINECONE_NAMESPACE = "custom_sources"
OPENAI_API_KEY = "sk-your-key-here"
PINECONE_API_KEY = "your-pinecone-key"
```

## 5. Get Shareable URL

Your public URL will be: 
`https://telecommunications-smb-bot.streamlit.app`

Share this link with anyone!

## Troubleshooting

- **ImportError**: Make sure all dependencies are in `requirements.txt`
- **API Connection Failed**: Verify API_URL is accessible and API is running
- **Secrets not working**: Use `st.secrets.get("KEY_NAME", "default_value")`

## Next: Connect Your API

Update the backend integration:
- Modify `API_URL` to point to your production API endpoint
- Ensure API has CORS configured to accept Streamlit Cloud
