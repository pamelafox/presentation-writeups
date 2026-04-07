---
name: capture-video-frames
description: >-
  Capture frames from a YouTube video at a regular interval, produce a manifest
  mapping filenames to timestamps, and describe each frame with an LLM.
  USE FOR: extract video frames, capture screenshots from YouTube, describe video frames,
  video frame analysis, frame-by-frame summary.
argument-hint: <youtube_url> <output_dir> [--interval SECONDS]
---

# Capture and describe video frames

## Step 1: Capture frames

Run the [capture_video_frames.py](./capture_video_frames.py) script:

```bash
uv run .github/skills/capture-video-frames/capture_video_frames.py <youtube_url> <output_dir> [--interval SECONDS]
```

### Arguments

- `youtube_url` (required): YouTube video URL (same formats accepted by the extract-transcript skill).
- `output_dir` (required): Directory to save frames and the manifest file. Created if it doesn't exist.
- `--interval` (optional): Seconds between captured frames. Defaults to **30**.

### Outputs

- **frame_0000.png**, **frame_0030.png**, … — PNG images named by their timestamp in seconds (zero-padded to 4 digits).
- **frames_manifest.md** — A markdown file listing each frame with its timestamp and a placeholder for descriptions.

Example **frames_manifest.md**:

```
| File | Timestamp | Description |
|------|-----------|-------------|
| frame_0000.png | [00:00] | |
| frame_0030.png | [00:30] | |
| frame_0060.png | [01:00] | |
```

### Prerequisites

- **yt-dlp**: `brew install yt-dlp` or `pip install yt-dlp`
- **ffmpeg**: `brew install ffmpeg` or `apt-get install ffmpeg`

## Step 2: Describe frames using the `describe-frame` subagent

After capturing frames, describe each frame by running the **describe-frame** custom agent as a subagent. Each subagent invocation gets an isolated context, so frame images won't accumulate and exhaust the context window.

The `describe-frame` agent is defined in `.github/agents/describe-frame.md`.

### Procedure

1. Read **frames_manifest.md** from the output directory to get the full list of frames.
2. For each frame, run the `describe-frame` agent as a subagent with a prompt that includes:
   - The **absolute path** to the current frame image to view.
   - The **absolute path** to the previous frame image to view (if one exists).
   - The **previous frame's description** as text (if one exists).
3. The subagent will return a plain-text description (or `(same as previous)` if the frame is essentially identical to the previous one).
4. After each subagent returns, update the Description column for that row in **frames_manifest.md** immediately.
5. Continue until all frames are described.

### Subagent prompt template

Use this as the prompt when invoking the `describe-frame` subagent (fill in the bracketed values):

```
Describe the current frame image at: [CURRENT_FRAME_ABSOLUTE_PATH]

[If previous frame exists, include these two lines:]
The previous frame image is at: [PREVIOUS_FRAME_ABSOLUTE_PATH]
The previous frame was described as: "[PREVIOUS_DESCRIPTION]"
```

### Example output

After describing all frames, **frames_manifest.md** should look like:

```
| File | Timestamp | Description |
|------|-----------|-------------|
| frame_0000.png | [00:00] | Title slide introducing "Building RAG apps with Python" |
| frame_0030.png | [00:30] | Speaker showing the agenda with four main topics |
| frame_0060.png | [01:00] | (same as previous) |
| frame_0090.png | [01:30] | Architecture diagram of a retrieval-augmented generation pipeline |
```
