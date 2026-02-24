# Presentation Write-ups

This repo turns presentations into annotated blog-style write-ups with embedded slide images. It uses Azure OpenAI to process video recordings and PDF slides.

## Raw materials

Each presentation requires:

- **Slides**: PDF file, PDF URL, PPTX file, OneDrive sharing link, or RevealJS URL (required)
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

Install Playwright browsers (required for RevealJS support):

```bash
uv run playwright install chromium
```

You'll also need:

- Azure OpenAI access with the following environment variables:
  - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
  - `AZURE_OPENAI_CHAT_DEPLOYMENT`: The deployment name for chat completions
- Azure authentication configured (uses `DefaultAzureCredential` - works with Azure CLI login, managed identity, etc.)
- `poppler` installed for PDF processing: `brew install poppler`
- `LibreOffice` installed for PPTX support (optional): `brew install --cask libreoffice`

## Generating write-ups

Create a `presentation.yaml` file in your presentation folder (see [examples/presentation.yaml](examples/presentation.yaml)):

```yaml
title: "My Presentation"
date: 2026-01-06

# Video source: YouTube URL or local MP4 path (required)
video: "https://www.youtube.com/watch?v=abc123"

# Slides: PDF path, PPTX URL, OneDrive link, or RevealJS URL (required)
slides: "slides.pdf"
# OR for OneDrive sharing link:
# slides: "https://onedrive.live.com/:p:/g/personal/.../..."
# OR for RevealJS presentations:
# slides: "https://example.com/my-presentation"

# Optional: additional notes
notes: |
  Any additional context
```

Then run the script:

```bash
uv run generate_writeup.py presentations/my-talk
```

The script:

1. Converts PDF slides to images (or fetches PDF from RevealJS URL first)
2. Fetches transcript from YouTube
3. Generates chapter summaries using Azure OpenAI
4. Generates slide outline using Azure OpenAI
5. Creates an annotated blog-style write-up with embedded slide images

All generated outputs are saved to an `outputs/` folder, and intermediate results are cached for faster re-runs.

## RevealJS support

For RevealJS presentations, provide the presentation URL as the `slides` value:

```yaml
slides: "https://pamelafox.github.io/my-talks/some-presentation/"
```

The script will automatically:

1. Append `?print-pdf` to the URL
2. Use Playwright to render the presentation
3. Save it as a PDF in the outputs folder
4. Continue with the normal processing pipeline

## PPTX / OneDrive support

For PowerPoint presentations hosted on OneDrive, provide the sharing URL as the `slides` value:

```yaml
slides: "https://onedrive.live.com/:p:/g/personal/..."
```

The script will automatically:

1. Convert the sharing URL to a download URL
2. Download the PPTX file
3. Convert it to PDF using LibreOffice
4. Continue with the normal processing pipeline

**Note:** LibreOffice must be installed for PPTX conversion (`brew install --cask libreoffice` on macOS).

## Folder structure

```text
presentations/
  my-talk/
    presentation.yaml      # Configuration: video URL, slides path/URL
    slides.pdf             # PDF slides (if using local file)
    transcript.txt         # Optional: pre-made transcript
    outputs/               # All generated content
      slides.pdf           # Downloaded PDF (if using RevealJS URL)
      slide_images/        # Individual slide images (PNG)
      chapters.txt         # Generated video chapters
      outline.txt          # Generated slide outline
      transcript.txt       # Fetched/cached transcript
      writeup.md           # Final annotated blog post
```

## Acknowledgements

Inspired by the [hamel](https://github.com/hamelsmu/hamel) package by [Hamel Husain](https://hamel.dev).
