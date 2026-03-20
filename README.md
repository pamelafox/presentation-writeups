# Presentation Write-ups

This repo turns presentations into annotated blog-style write-ups with embedded slide images. It uses GitHub Copilot agent skills and prompts (backed by Azure OpenAI) to process video recordings and PDF slides.

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

Create a `presentation.md` file in your presentation folder:

```markdown
# My Presentation

- **Date:** 2026-01-06
- **Video:** https://www.youtube.com/watch?v=abc123
- **Slides:** slides.pdf
- **Transcript:** transcript.txt

## Notes

Any additional context
```

Required fields: **Video** (YouTube URL or local MP4 path) and **Slides** (PDF path, PPTX URL, OneDrive link, or RevealJS URL). All others are optional.

Then run the `generate-writeup` prompt in VS Code Copilot Chat:

```
/generate-writeup presentations/my-talk
```

This uses the prompt defined in [`.github/prompts/generate-writeup.prompt.md`](.github/prompts/generate-writeup.prompt.md), which orchestrates the full pipeline:

1. Fetches/converts slides to PDF (if URL provided)
2. Converts PDF slides to images
3. Extracts transcript from YouTube
4. Generates chapter summaries
5. Extracts slide text and generates slide outline
6. Creates an annotated blog-style write-up with embedded slide images

All generated outputs are saved to an `outputs/` folder, and intermediate results are cached for faster re-runs.

### Agent skills

The pipeline is built from individual agent skills in `.github/skills/`:

| Skill | Purpose |
|-------|---------|
| `/fetch-slides` | Fetch/convert slides from URLs (PDF, PPTX, OneDrive, RevealJS) |
| `/extract-transcript` | Get timestamped transcript from YouTube |
| `/convert-slides-to-images` | Convert PDF slides to individual PNGs |
| `/extract-slide-text` | Extract text from each PDF page into a markdown file |
| `/outline-slides` | Summarize each slide image into a numbered list |

## RevealJS support

For RevealJS presentations, provide the presentation URL as the `slides` value:

```markdown
- **Slides:** https://pamelafox.github.io/my-talks/some-presentation/
```

The `/fetch-slides` skill will automatically:

1. Append `?print-pdf` to the URL
2. Use Playwright to render the presentation
3. Save it as a PDF in the outputs folder
4. Continue with the normal processing pipeline

## PPTX / OneDrive support

For PowerPoint presentations hosted on OneDrive, provide the sharing URL as the `slides` value:

```markdown
- **Slides:** https://onedrive.live.com/:p:/g/personal/...
```

The `/fetch-slides` skill will automatically:

1. Convert the sharing URL to a download URL
2. Download the PPTX file
3. Convert it to PDF using LibreOffice
4. Continue with the normal processing pipeline

**Note:** LibreOffice must be installed for PPTX conversion (`brew install --cask libreoffice` on macOS).

## Folder structure

```text
presentations/
  my-talk/
    presentation.md        # Configuration: video URL, slides path/URL
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
