"""
Writing utilities for generating annotated presentation write-ups.

This module provides local implementations using Azure OpenAI, replacing
the Gemini-based functions from hamel.writing.
"""

import base64
import logging
import subprocess
from pathlib import Path

from rich.logging import RichHandler

from azure_openai_client import chat_completion

# Set up logger with RichHandler
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def pdf2imgs(pdf_path: str, output_dir: str = ".", prefix: str = "slide") -> list[str]:
    """
    Split a PDF file into individual slide images using poppler's pdftoppm.
    
    Requires poppler-utils installed:
    - macOS: brew install poppler
    - Ubuntu: apt-get install poppler-utils
    
    Args:
        pdf_path: Path to the PDF file
        output_dir: Directory to save images (default: current directory)
        prefix: Prefix for output filenames (default: "slide")
        
    Returns:
        List of paths to the generated image files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Run pdftoppm to convert PDF to PNG images
    cmd = [
        "pdftoppm",
        "-png",
        str(pdf_path),
        str(output_path / prefix)
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except FileNotFoundError:
        raise FileNotFoundError(
            "pdftoppm not found. Install poppler:\n"
            "  macOS: brew install poppler\n"
            "  Ubuntu: apt-get install poppler-utils"
        )
    
    # pdftoppm creates files like slide-01.png, slide-02.png, etc.
    # Rename to slide_1.png, slide_2.png format (strip leading zeros)
    image_files = []
    for f in sorted(output_path.glob(f"{prefix}-*.png")):
        # Extract page number, strip leading zeros, and rename
        page_num = int(f.stem.split("-")[-1])  # Convert to int to strip leading zeros
        new_name = output_path / f"{prefix}_{page_num}.png"
        f.rename(new_name)
        image_files.append(str(new_name))
    
    return image_files


def transcribe(url: str) -> str:
    """
    Get transcript from YouTube URL.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Transcript text with timestamps
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    import re
    
    # Extract video ID from URL
    video_id = None
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([^&?/]+)',
        r'(?:embed/)([^&?/]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            break
    
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    
    # Format with timestamps
    lines = []
    for snippet in transcript:
        start = int(snippet.start)
        hours, remainder = divmod(start, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            timestamp = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"
        else:
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
        lines.append(f"{timestamp} {snippet.text}")
    
    return "\n".join(lines)


# Default example URLs for annotated post style reference
DEFAULT_EXAMPLE_URLS = [
    "https://raw.githubusercontent.com/hamelsmu/hamel-site/refs/heads/master/notes/llm/evals/inspect.qmd",
    "https://raw.githubusercontent.com/hamelsmu/hamel-site/refs/heads/master/notes/llm/rag/p1-intro.md",
    "https://raw.githubusercontent.com/hamelsmu/hamel-site/refs/heads/master/notes/llm/rag/p2-evals.md",
]


def gather_urls(urls: list[str]) -> str:
    """
    Gather contents from URLs and format as examples.
    
    Args:
        urls: List of URLs to fetch
        
    Returns:
        Formatted string with URL contents in example tags
    """
    import urllib.request
    
    examples = []
    for i, url in enumerate(urls, 1):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                content = response.read().decode('utf-8')
                examples.append(f"<example-{i}>\nTitle: \n\nURL Source: {url}\n\nMarkdown Content:\n{content}\n</example-{i}>")
        except Exception as e:
            logger.warning(f"Failed to fetch {url}: {e}")
    
    return "<examples>\n" + "\n\n".join(examples) + "\n</examples>"


def outline_slides(slide_path: str, image_dir: str) -> str:
    """
    Generate a numbered outline of slides with one-sentence summaries.
    
    Args:
        slide_path: Path to the PDF file
        image_dir: Directory containing slide images (already converted)
        
    Returns:
        Numbered list of slides with summaries
    """
    # Get slide images from image_dir (assumes pdf2imgs was already called)
    image_path = Path(image_dir)
    image_files = sorted(image_path.glob("slide_*.png"))
    
    if not image_files:
        raise ValueError(f"No slide images found in {image_dir}. Run pdf2imgs first.")
    
    # Build content with all slide images
    content = [
        {
            "type": "text",
            "text": "Provide a numbered list of each slide with a one sentence summary of each. Just a numbered list please, no other asides or meta explanations of the task are required."
        }
    ]
    
    # Add each slide image
    for img_path in image_files:
        img_bytes = img_path.read_bytes()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{img_base64}"
            }
        })
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that analyzes presentation slides."
        },
        {
            "role": "user",
            "content": content
        }
    ]
    
    return chat_completion(messages, temperature=0.3)


def yt_chapters(url_or_path: str) -> str:
    """
    Generate video summary and chapters from a video (YouTube URL or local MP4).
    
    Args:
        url_or_path: YouTube URL or path to local MP4 file
        
    Returns:
        Summary and timestamped chapters
    """
    # Get transcript
    transcript = transcribe(url_or_path)
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that creates video chapters and summaries."
        },
        {
            "role": "user",
            "content": f"""Based on this transcript, create:
1. A brief summary paragraph (2-3 sentences) describing what the video is about
2. A list of timestamped chapters in the format "MM:SS - Chapter Title"

The chapters should cover the main sections and topics discussed. Use timestamps from the transcript.

Transcript:
{transcript}"""
        }
    ]
    
    return chat_completion(messages, temperature=0.3)


def generate_annotated_talk_post(
    slide_path: str,
    video_source: str,
    output_dir: str,
    transcript_path: str | None = None,
    user_prompt: str | None = None,
) -> str:
    """
    Generate an annotated blog-style write-up from presentation slides and video.
    
    This function:
    1. Converts PDF slides to images
    2. Gets/transcribes video transcript
    3. Generates chapter summaries
    4. Creates an annotated write-up with embedded slide images
    
    All generated outputs are saved to output_dir for caching and inspection.
    
    Args:
        slide_path: Path to the PDF slides
        video_source: YouTube URL or path to local MP4
        output_dir: Directory to save all generated outputs
        transcript_path: Optional path to pre-made transcript (in source folder)
        user_prompt: Additional context/instructions
        
    Returns:
        The generated write-up in markdown format
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Set up paths for cached outputs
    image_dir = output_path / "slide_images"
    chapters_file = output_path / "chapters.txt"
    outline_file = output_path / "outline.txt"
    transcript_file = output_path / "transcript.txt"
    
    # Check if video_source is a local MP4 or YouTube URL
    is_local_video = Path(video_source).exists() and Path(video_source).suffix.lower() == '.mp4'
    
    # Generate or load video chapters
    if chapters_file.exists():
        logger.info(f"Loading cached chapters from {chapters_file}")
        video_chapters = chapters_file.read_text()
    else:
        logger.info("Generating video chapters...")
        video_chapters = yt_chapters(video_source)
        chapters_file.write_text(video_chapters)
        logger.info(f"Saved chapters to {chapters_file}")
    
    # Convert slides to images (check if already done)
    image_dir.mkdir(exist_ok=True)
    existing_images = list(image_dir.glob("slide_*.png"))
    if existing_images:
        logger.info(f"Using {len(existing_images)} cached slide images from {image_dir}")
    else:
        logger.info("Converting slides to images...")
        pdf2imgs(slide_path, output_dir=str(image_dir))
    
    # Generate or load slide outline
    if outline_file.exists():
        logger.info(f"Loading cached outline from {outline_file}")
        slide_outline = outline_file.read_text()
    else:
        logger.info("Generating slide outline...")
        slide_outline = outline_slides(slide_path, str(image_dir))
        outline_file.write_text(slide_outline)
        logger.info(f"Saved outline to {outline_file}")
    
    # Get or load transcript
    if transcript_file.exists():
        logger.info(f"Loading cached transcript from {transcript_file}")
        transcript = transcript_file.read_text()
    elif transcript_path and Path(transcript_path).exists():
        logger.info(f"Loading transcript from {transcript_path}")
        transcript = Path(transcript_path).read_text()
        transcript_file.write_text(transcript)
        logger.info(f"Saved transcript to {transcript_file}")
    else:
        logger.info("Fetching transcript from video...")
        transcript = transcribe(video_source)
        transcript_file.write_text(transcript)
        logger.info(f"Saved transcript to {transcript_file}")
    
    # Build the prompt
    if is_local_video:
        timestamp_note = "Note: For local MP4 files, timestamps cannot be linked directly. Just provide the timestamp in [MM:SS] format."
    else:
        timestamp_note = f"Additionally, reference the correct timestamp in the form of a timestamped linked to the youtube video that corresponds to the start of each slide. The link to this presentation is {video_source} (so use this when adding timestamps please)."
    
    prompt = f"""Attached is the transcript (in <transcript> tags) of a technical talk. Create an annotated blog post that explains the content of each slide.

For each slide, provide a detailed synopsis of the information to maximize understanding for the reader. Each section should provide enough commentary and info to understand the full context of that particular slide. The idea is that the reader will not have to watch the video and can instead read the material, so the writing + slide should stand alone. Do not simply repeat the information on each slide. Capture supplementary information from the talk that is NOT visible on the slides. Be thoroughly detailed and capture useful asides or commentary as well, such that the notes you generate should be a legitimate value add on top of the slides.

IMPORTANT: Write in an expository style that directly explains the concepts. Do NOT narrate what the speakers said or did (e.g., avoid "Matt explains that..." or "She describes..."). Instead, directly state the information (e.g., "RAG is a technique that..." or "Hybrid search combines...").

When writing the article, provide markdown image references with appropriate captions where the slides will go. For example:

![Overview of xyz concept](slide_images/slide_1.png)

Note that images for this post will be placed in slide_images/

Refer to slides with naming convention (slide_1.png, slide_2.png, etc)

{timestamp_note}

If there is a Q&A section of the talk that does not correspond to any slides, list those questions with answers in a Q&A section at the end. Add timestamps to each question if possible.

<transcript>
{transcript}
</transcript>

Here is the video description with chapters from the talk. Use timestamps from the transcript when constructing timestamped links.
<video-chapters>
{video_chapters}
</video-chapters>

Below is a brief slide outline:
<slide-outline>
{slide_outline}
</slide-outline>

Writing guidelines:

1. Write in direct expository style. State facts and explanations directly.
2. Never narrate what speakers said or did. No "The speaker explains..." or "Matt shows..."
3. Make every sentence information-dense without repetition.
4. Get to the point while providing necessary context.
5. Use short words and fewer words.
6. Avoid multiple examples if one suffices.
7. Remove sentences that restate the premise.
8. Cut transitional fluff like "This is important because…"
9. Combine related ideas into single statements.
10. Avoid overusing bullet points. Prefer flowing prose.
11. Trust the reader's intelligence.
12. Use direct statements. Avoid hedge words unless exceptions matter.
13. No emojis in professional writing.
14. Use simple language. Present information objectively.

Please go ahead and draft the post."""

    if user_prompt:
        prompt += f"\n\nAdditional context/instructions from the user:\n{user_prompt}"
    
    logger.info("Generating annotated write-up (this may take a while)...")
    messages = [
        {
            "role": "system",
            "content": "You are a technical writer creating annotated blog posts from presentation talks. Write in a clear, educational style."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    return chat_completion(messages, temperature=0.7, max_tokens=16000)
