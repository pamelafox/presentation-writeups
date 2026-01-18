# Presentation Write-ups: Instructions for coding agents

The goal of this repo is to turn presentations into annotated blog-style write-ups with embedded slide images. Each presentation requires PDF slides and a video recording (YouTube URL or local MP4).

## Generating write-ups

Use `generate_writeup.py` which uses Azure OpenAI to generate annotated write-ups:

```bash
uv run generate_writeup.py presentations/my-talk
```

This requires:
- Azure OpenAI environment variables: `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_CHAT_DEPLOYMENT`
- A `presentation.yaml` in the folder with:
  - `video`: YouTube URL or local MP4 path (required)
  - `slides`: PDF path (required)  
  - `transcript`: Optional transcript file path
  - `title`, `date`, `notes`: Optional metadata