# Presentation Write-ups: Instructions for coding agents

The goal of this repo is to turn presentations into annotated blog-style write-ups with embedded slide images. Each presentation requires slides (PDF, PPTX, or URL) and a video recording (YouTube URL or local MP4).

## Prompts

The full writeup pipeline is available as a reusable prompt file:

- [`.github/prompts/generate-writeup.prompt.md`](.github/prompts/generate-writeup.prompt.md) — Orchestrates the full pipeline to produce an annotated write-up

To use it, run the prompt with a presentation folder path (e.g., `presentations/my-talk`).

## Agent Skills

This repo also provides Agent Skills in `.github/skills/` for individual pipeline steps:

| Skill | Type | Purpose |
|-------|------|---------|
| `/fetch-slides` | Script | Fetch/convert slides from URLs (PDF, PPTX, OneDrive, RevealJS) |
| `/extract-transcript` | Script | Get timestamped transcript from YouTube |
| `/convert-slides-to-images` | Script | Convert PDF slides to individual PNGs |
| `/extract-slide-text` | Script | Extract text from each PDF page into a markdown file |
| `/outline-slides` | Instructions | Summarize each slide image into a numbered list |
| `/capture-video-frames` | Script + Subagent | Capture frames from YouTube video, describe each via `describe-frame` subagent |

### Full pipeline

To generate a complete write-up, use the `generate-writeup` prompt with a presentation folder:

```
/generate-writeup presentations/my-talk
```

This requires a `presentation.yaml` in the folder with:

- `video`: YouTube URL or local MP4 path (required)
- `slides`: PDF path, PDF URL, PPTX URL, OneDrive link, or RevealJS URL (required)
- `transcript`: Optional transcript file path
- `title`, `date`, `notes`: Optional metadata

### Prerequisites

- **poppler** (for PDF to PNG conversion): `brew install poppler`
- **LibreOffice** (for PPTX to PDF conversion): `brew install --cask libreoffice`
- **Playwright** (for RevealJS to PDF): `uv run playwright install chromium`
