# Streamlit Cloud Deployment Troubleshooting

## Common Issues and Solutions

### 1. "OpenAI API key is required" Error
**Problem**: The app can't find your OpenAI API key.

**Solution**: 
- Go to your Streamlit Cloud app dashboard
- Click "Manage app" 
- Navigate to "Secrets" tab
- Add this configuration:
  ```toml
  OPENAI_API_KEY = "your_actual_api_key_here"
  ```
- Click "Save"
- The app will automatically restart

### 2. API Key Format
Make sure your API key:
- Starts with `sk-`
- Is from OpenAI (not Azure OpenAI or other providers)
- Has sufficient credits/quota
- Is correctly copied without extra spaces

### 3. Dependencies Issues
If you see import errors, make sure your `requirements.txt` includes all necessary packages:
```
streamlit
openai
langchain
langchain-openai
langchain-community
sentence-transformers
chromadb
PyPDF2
python-docx
python-dotenv
```

### 4. File Access Issues
- The `data/` folder should contain your personal documents
- Supported formats: PDF, DOCX, TXT, MD, PY, JS, HTML, CSS, JSON
- Use the "Refresh Documents" button after adding new files

### 5. Memory Issues
If the app crashes due to memory limits:
- Reduce the number of documents
- Use smaller document chunks
- Consider using a lighter embedding model

### 6. OpenAI Rate Limits
If you hit rate limits:
- Check your OpenAI usage dashboard
- Upgrade your OpenAI plan if needed
- Wait for the rate limit to reset

## Testing Locally

To test with the same configuration as Streamlit Cloud:

1. Create `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your_api_key_here"
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Getting Help

1. Check the app logs in Streamlit Cloud dashboard
2. Verify your OpenAI API key works by testing it directly
3. Make sure you have sufficient OpenAI credits
4. Try deploying a minimal version first, then add features

## Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] OpenAI API key added to Streamlit secrets
- [ ] API key has sufficient credits
- [ ] Documents added to data/ folder
- [ ] App successfully starts without errors
- [ ] Test a few questions to verify functionality
