# Presentation Write-ups

This repo turns presentations into annotated blog-style write-ups with embedded slide images. It uses Azure OpenAI to process video recordings and PDF slides.

## Raw materials

Each presentation requires:

- **Slides**: PDF file (required)
- **Recording**: YouTube video URL or local MP4 file (required)
- **Transcript**: Optional text file (auto-fetched from video if not provided)

## Setup

Install [uv](https://docs.astral.sh/uv/) if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the project dependencies:

```bash
uv sync
```

You'll also need:
- Azure OpenAI access with the following environment variables:
  - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
  - `AZURE_OPENAI_CHAT_DEPLOYMENT`: The deployment name for chat completions
- Azure authentication configured (uses `DefaultAzureCredential` - works with Azure CLI login, managed identity, etc.)
- `ffmpeg` installed for local video transcription: `brew install ffmpeg`
- `poppler` installed for PDF processing: `brew install poppler`

## Generating write-ups

Create a `presentation.yaml` file in your presentation folder (see [examples/presentation.yaml](examples/presentation.yaml)):

```yaml
title: "My Presentation"
date: 2026-01-06

# Video source: YouTube URL or local MP4 path (required)
video: "https://www.youtube.com/watch?v=abc123"

# Slides: PDF path relative to this folder (required)
slides: "slides.pdf"

# Transcript: optional, auto-fetched from video if not provided
# transcript: "transcript.txt"

# Optional: additional notes
notes: |
  Any additional context
```

Then run the script:

```bash
uv run generate_writeup.py presentations/my-talk
```

The script:

1. Converts PDF slides to images
2. Fetches transcript from YouTube
3. Generates chapter summaries using Azure OpenAI
4. Generates slide outline using Azure OpenAI
5. Creates an annotated blog-style write-up with embedded slide images

All generated outputs are saved to an `outputs/` folder, and intermediate results are cached for faster re-runs.

## Folder structure

```text
presentations/
  my-talk/
    presentation.yaml      # Configuration: video URL, slides path
    slides.pdf             # PDF slides (required)
    transcript.txt         # Optional: pre-made transcript
    outputs/               # All generated content
      slide_images/        # Individual slide images (PNG)
      chapters.txt         # Generated video chapters
      outline.txt          # Generated slide outline
      transcript.txt       # Fetched/cached transcript
      writeup.md           # Final annotated blog post
```
