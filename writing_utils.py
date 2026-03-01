"""
Writing utilities for generating annotated presentation write-ups.

This module provides local implementations using Azure OpenAI, replacing
the Gemini-based functions from hamel.writing.
"""

import base64
import logging
import subprocess
from pathlib import Path
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

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


def is_onedrive_url(url: str) -> bool:
    """Check if URL is a OneDrive sharing link."""
    return 'onedrive.live.com' in url or '1drv.ms' in url


def get_onedrive_download_url(url: str) -> str:
    """
    Convert a OneDrive sharing URL to a direct download URL.
    
    OneDrive sharing URLs like:
    https://onedrive.live.com/:p:/g/personal/...
    
    Can be converted to download URLs by adding ?download=1
    
    Args:
        url: OneDrive sharing URL
        
    Returns:
        Direct download URL
    """
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params['download'] = ['1']
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def convert_pptx_to_pdf(pptx_path: str, output_path: str) -> str:
    """
    Convert a PPTX file to PDF using LibreOffice.
    
    Requires LibreOffice installed:
    - macOS: brew install --cask libreoffice
    - Ubuntu: apt-get install libreoffice
    
    Args:
        pptx_path: Path to the PPTX file
        output_path: Path for the output PDF file
        
    Returns:
        Path to the generated PDF file
    """
    import shutil
    
    pptx_path = Path(pptx_path)
    output_path = Path(output_path)
    output_dir = output_path.parent
    
    # Find LibreOffice binary
    soffice_paths = [
        '/Applications/LibreOffice.app/Contents/MacOS/soffice',  # macOS
        '/usr/bin/soffice',  # Linux
        '/usr/bin/libreoffice',  # Linux alternative
        shutil.which('soffice'),  # PATH lookup
        shutil.which('libreoffice'),  # PATH lookup
    ]
    
    soffice = None
    for path in soffice_paths:
        if path and Path(path).exists():
            soffice = path
            break
    
    if not soffice:
        raise FileNotFoundError(
            "LibreOffice not found. Install it:\n"
            "  macOS: brew install --cask libreoffice\n"
            "  Ubuntu: apt-get install libreoffice"
        )
    
    logger.info(f"Converting PPTX to PDF using LibreOffice: {soffice}")
    
    # LibreOffice outputs to the same directory with .pdf extension
    cmd = [
        soffice,
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', str(output_dir),
        str(pptx_path)
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"LibreOffice conversion output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"LibreOffice conversion failed: {e.stderr}")
        raise RuntimeError(f"Failed to convert PPTX to PDF: {e.stderr}")
    
    # LibreOffice creates PDF with same base name as input
    generated_pdf = output_dir / f"{pptx_path.stem}.pdf"
    
    if not generated_pdf.exists():
        raise FileNotFoundError(f"Expected PDF not found: {generated_pdf}")
    
    # Rename to the requested output path if different
    if generated_pdf != output_path:
        generated_pdf.rename(output_path)
    
    logger.info(f"Saved PDF to: {output_path}")
    return str(output_path)


def fetch_slides_from_url(url: str, output_dir: str) -> tuple[str, str | None]:
    """
    Fetch slides from a URL, detecting whether it's a PDF, PPTX, or HTML (RevealJS).
    
    Supports:
    - Direct PDF URLs
    - OneDrive sharing links (PPTX)
    - RevealJS HTML presentations
    
    Args:
        url: URL of the slides (PDF, PPTX, or RevealJS HTML)
        output_dir: Directory to save the output files
        
    Returns:
        Tuple of (pdf_path, html_content_path or None)
    """
    import httpx
    
    output_path = Path(output_dir)
    pdf_path = output_path / 'slides.pdf'
    pptx_path = output_path / 'slides.pptx'
    html_content_path = output_path / 'slides_content.md'
    
    # Check if this is a OneDrive URL (needs special handling)
    if is_onedrive_url(url):
        download_url = get_onedrive_download_url(url)
        logger.info(f"Detected OneDrive URL, using download URL: {download_url}")
        
        # Download the file
        response = httpx.get(download_url, follow_redirects=True, timeout=60.0)
        content_type = response.headers.get('content-type', '').lower()
        
        if 'presentationml' in content_type or 'pptx' in content_type:
            # PPTX file - download and convert
            logger.info("Detected PPTX, downloading and converting to PDF...")
            pptx_path.write_bytes(response.content)
            logger.info(f"Saved PPTX to: {pptx_path}")
            convert_pptx_to_pdf(str(pptx_path), str(pdf_path))
            return str(pdf_path), None
        elif 'application/pdf' in content_type:
            # Direct PDF
            logger.info("Detected PDF from OneDrive, downloading...")
            pdf_path.write_bytes(response.content)
            logger.info(f"Saved PDF to: {pdf_path}")
            return str(pdf_path), None
        else:
            raise ValueError(f"Unexpected content type from OneDrive: {content_type}")
    
    # Make a HEAD request to check content type
    logger.info(f"Checking content type for: {url}")
    response = httpx.head(url, follow_redirects=True)
    content_type = response.headers.get('content-type', '').lower()
    
    if 'application/pdf' in content_type:
        # Direct PDF download
        logger.info("Detected PDF, downloading directly...")
        response = httpx.get(url, follow_redirects=True)
        pdf_path.write_bytes(response.content)
        logger.info(f"Saved PDF to: {pdf_path}")
        return str(pdf_path), None
    elif 'presentationml' in content_type or 'pptx' in content_type:
        # PPTX file - download and convert
        logger.info("Detected PPTX, downloading and converting to PDF...")
        response = httpx.get(url, follow_redirects=True)
        pptx_path.write_bytes(response.content)
        logger.info(f"Saved PPTX to: {pptx_path}")
        convert_pptx_to_pdf(str(pptx_path), str(pdf_path))
        return str(pdf_path), None
    elif 'text/html' in content_type:
        # HTML - assume RevealJS
        logger.info("Detected HTML, treating as RevealJS presentation...")
        fetch_revealjs_pdf(url, str(pdf_path))
        extract_revealjs_content(url, str(html_content_path))
        return str(pdf_path), str(html_content_path)
    else:
        # Unknown - try RevealJS approach
        logger.warning(f"Unknown content type '{content_type}', attempting RevealJS fetch...")
        fetch_revealjs_pdf(url, str(pdf_path))
        return str(pdf_path), None


def extract_revealjs_content(url: str, output_path: str) -> str:
    """
    Extract text content and links from RevealJS slides.
    
    Detects section slides (class="heading") to indicate hierarchy.
    
    Args:
        url: URL of the RevealJS presentation
        output_path: Path to save the extracted content
        
    Returns:
        Path to the saved content file
    """
    import httpx
    from html.parser import HTMLParser
    
    logger.info(f"Extracting RevealJS slide content from: {url}")
    
    response = httpx.get(url, follow_redirects=True)
    html = response.text
    
    # Simple parser to extract slide content
    class SlideExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.slides = []
            self.current_slide = []
            self.in_slides = False
            self.in_section = False
            self.is_heading_slide = False
            self.section_depth = 0
            self.current_tag = None
            self.links = []
            
        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            self.current_tag = tag
            
            if tag == 'div' and 'slides' in attrs_dict.get('class', ''):
                self.in_slides = True
            elif tag == 'section' and self.in_slides:
                if self.section_depth == 0:
                    self.in_section = True
                    self.current_slide = []
                    self.links = []
                    # Check if this is a heading/section slide
                    classes = attrs_dict.get('class', '')
                    self.is_heading_slide = 'heading' in classes
                self.section_depth += 1
            elif tag == 'a' and self.in_section:
                href = attrs_dict.get('href', '')
                if href and not href.startswith('#'):
                    self.links.append(href)
            elif tag == 'img' and self.in_section:
                alt = attrs_dict.get('alt', '')
                if alt:
                    self.current_slide.append(f"[Image: {alt}]")
                    
        def handle_endtag(self, tag):
            if tag == 'section' and self.in_slides:
                self.section_depth -= 1
                if self.section_depth == 0 and self.in_section:
                    self.in_section = False
                    slide_content = ' '.join(self.current_slide).strip()
                    if slide_content or self.links:
                        self.slides.append({
                            'content': slide_content,
                            'links': self.links.copy(),
                            'is_heading': self.is_heading_slide
                        })
                    self.is_heading_slide = False
            elif tag == 'div':
                # Could be end of slides div, but we don't track that precisely
                pass
                
        def handle_data(self, data):
            if self.in_section:
                text = data.strip()
                if text:
                    self.current_slide.append(text)
    
    parser = SlideExtractor()
    parser.feed(html)
    
    # Format output
    lines = ["# RevealJS Slide Content\n"]
    for i, slide in enumerate(parser.slides, 1):
        slide_type = "SECTION HEADING" if slide['is_heading'] else "Slide"
        lines.append(f"## {slide_type} {i}\n")
        if slide['content']:
            lines.append(slide['content'])
            lines.append("")
        if slide['links']:
            lines.append("**Links:**")
            for link in slide['links']:
                lines.append(f"- {link}")
            lines.append("")
    
    content = '\n'.join(lines)
    Path(output_path).write_text(content)
    logger.info(f"Saved slide content to: {output_path}")
    return output_path


def fetch_revealjs_pdf(url: str, output_path: str) -> str:
    """
    Fetch a RevealJS presentation as PDF using Playwright.
    
    Appends ?print-pdf to the URL and uses the browser's print-to-PDF feature.
    
    Args:
        url: URL of the RevealJS presentation
        output_path: Path to save the PDF file
        
    Returns:
        Path to the saved PDF file
    """
    from playwright.sync_api import sync_playwright
    
    # Add ?print-pdf to the URL
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params['print-pdf'] = ['']
    new_query = urlencode(query_params, doseq=True).replace('print-pdf=', 'print-pdf')
    print_url = urlunparse(parsed._replace(query=new_query))
    
    logger.info(f"Fetching RevealJS PDF from: {print_url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load the page and wait for RevealJS to render
        page.goto(print_url, wait_until='networkidle')
        
        # Wait a bit more for any animations/transitions
        page.wait_for_timeout(2000)
        
        # Save as PDF with print settings optimized for slides
        page.pdf(
            path=output_path,
            format='Letter',
            print_background=True,
            prefer_css_page_size=True,
        )
        
        browser.close()
    
    logger.info(f"Saved PDF to: {output_path}")
    return output_path


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


def outline_slides(slide_path: str, image_dir: str, max_images_per_request: int = 50) -> str:
    """
    Generate a numbered outline of slides with one-sentence summaries.
    
    Args:
        slide_path: Path to the PDF file
        image_dir: Directory containing slide images (already converted)
        max_images_per_request: Maximum images per LLM request (default: 50)
        
    Returns:
        Numbered list of slides with summaries
    """
    # Get slide images from image_dir (assumes pdf2imgs was already called)
    image_path = Path(image_dir)
    image_files = sorted(image_path.glob("slide_*.png"), key=lambda x: int(x.stem.split("_")[-1]))
    
    if not image_files:
        raise ValueError(f"No slide images found in {image_dir}. Run pdf2imgs first.")
    
    # If we have more images than the limit, batch them
    if len(image_files) > max_images_per_request:
        logger.info(f"Batching {len(image_files)} slides into multiple requests (max {max_images_per_request} per request)")
        all_outlines = []
        
        for batch_start in range(0, len(image_files), max_images_per_request):
            batch_end = min(batch_start + max_images_per_request, len(image_files))
            batch_files = image_files[batch_start:batch_end]
            start_num = batch_start + 1
            end_num = batch_end
            
            logger.info(f"Processing slides {start_num}-{end_num}...")
            
            content = [
                {
                    "type": "text",
                    "text": f"Provide a numbered list of each slide with a one sentence summary of each. These are slides {start_num} through {end_num}. Start numbering at {start_num}. Just a numbered list please, no other asides or meta explanations of the task are required."
                }
            ]
            
            for img_path in batch_files:
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
            
            batch_outline = chat_completion(messages, temperature=0.3)
            all_outlines.append(batch_outline)
        
        return "\n".join(all_outlines)
    
    # Single request for <= max_images_per_request slides
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
    slides_html_content_path: str | None = None,
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
        slides_html_content_path: Optional path to extracted HTML content from RevealJS
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
    
    # Load HTML content if available
    slides_html_content = None
    if slides_html_content_path and Path(slides_html_content_path).exists():
        slides_html_content = Path(slides_html_content_path).read_text()
        logger.info(f"Loaded slide HTML content from {slides_html_content_path}")
    
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
    
    # Check if we have section headings from RevealJS
    has_section_headings = slides_html_content and "SECTION HEADING" in slides_html_content
    
    # Check if video_source is a local MP4 or YouTube URL
    is_local_video = Path(video_source).exists() and Path(video_source).suffix.lower() == '.mp4'
    
    # Load and render the prompt template
    from jinja2 import Environment, FileSystemLoader
    
    template_dir = Path(__file__).parent
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("writeup_prompt.jinja2")
    
    prompt = template.render(
        has_section_headings=has_section_headings,
        is_local_video=is_local_video,
        video_source=video_source,
        transcript=transcript,
        video_chapters=video_chapters,
        slide_outline=slide_outline,
        slides_html_content=slides_html_content,
        user_prompt=user_prompt,
    )
    
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
    
    writeup = chat_completion(messages, temperature=0.7)
    
    # Generate and insert table of contents
    writeup = insert_table_of_contents(writeup)
    
    return writeup


def insert_table_of_contents(markdown: str) -> str:
    """
    Parse markdown for ## headings and insert a table of contents after the first paragraph.
    
    Args:
        markdown: The markdown content
        
    Returns:
        Markdown with TOC inserted after the intro paragraph
    """
    import re
    
    # Find all ## headings
    headings = re.findall(r'^## (.+)$', markdown, re.MULTILINE)
    
    if not headings:
        return markdown
    
    # Generate TOC entries
    toc_lines = ["## Table of contents", ""]
    for heading in headings:
        # Convert heading to anchor link (lowercase, spaces to hyphens, remove special chars)
        anchor = heading.lower()
        anchor = re.sub(r'[^a-z0-9\s-]', '', anchor)
        anchor = re.sub(r'\s+', '-', anchor)
        anchor = re.sub(r'-+', '-', anchor).strip('-')
        toc_lines.append(f"- [{heading}](#{anchor})")
    toc_lines.append("")
    toc = "\n".join(toc_lines)
    
    # Find insertion point: after the first paragraph (after # heading and intro text)
    # Look for the first ## heading and insert TOC before it
    first_h2_match = re.search(r'^## ', markdown, re.MULTILINE)
    if first_h2_match:
        insert_pos = first_h2_match.start()
        return markdown[:insert_pos] + toc + "\n" + markdown[insert_pos:]
    
    return markdown
