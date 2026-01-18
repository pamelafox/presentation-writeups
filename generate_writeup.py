#!/usr/bin/env python3
"""
Generate an annotated presentation write-up from a folder containing raw materials.

This script uses the hamel package to process presentations and generate
annotated blog-style write-ups with embedded slide images. It reads from a 
presentation.yaml file that describes:
- Video source (YouTube URL or local MP4)
- Slides (PDF)
- Optional transcript file
- Additional context/notes

Usage:
    python generate_writeup.py <folder_path>
    
Example:
    python generate_writeup.py presentations/2026_01_06
"""

import argparse
import logging
import sys
from pathlib import Path
from dataclasses import dataclass

import yaml
from dotenv import load_dotenv
from rich.logging import RichHandler

from writing_utils import generate_annotated_talk_post

# Set up logger with RichHandler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)


@dataclass
class PresentationConfig:
    """Configuration for a presentation loaded from YAML."""
    title: str = ""
    date: str = ""
    video: str | None = None
    slides: str | None = None
    transcript: str | None = None
    notes: str = ""
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'PresentationConfig':
        """Load configuration from a YAML file."""
        with open(yaml_path) as f:
            data = yaml.safe_load(f) or {}
        
        return cls(
            title=data.get('title', ''),
            date=str(data.get('date', '')),
            video=data.get('video'),
            slides=data.get('slides'),
            transcript=data.get('transcript'),
            notes=data.get('notes', ''),
        )


def generate_writeup(
    folder: Path,
    output_file: str = 'writeup.md',
) -> str:
    """
    Generate an annotated presentation write-up from folder contents.
    
    Uses hamel.writing.generate_annotated_talk_post to create a blog-style
    write-up with embedded slide images and timestamps.
    
    Args:
        folder: Path to the folder containing presentation.yaml
        output_file: Name of the output file (default: writeup.md)
        
    Returns:
        The generated write-up content
    """
    yaml_path = folder / 'presentation.yaml'
    if not yaml_path.exists():
        raise FileNotFoundError(f"No presentation.yaml found in {folder}")
    
    # Load configuration
    config = PresentationConfig.from_yaml(yaml_path)
    logger.info(f"Loaded: {config.title or folder.name}")
    
    # Resolve video source (could be URL or local path)
    video_source = None
    if config.video:
        video_path = folder / config.video
        if video_path.exists():
            video_source = str(video_path)
            logger.info(f"Found local video: {video_path}")
        else:
            video_source = config.video
            logger.info(f"Using video URL: {video_source}")
    else:
        raise ValueError("No video source specified in presentation.yaml")
    
    # Resolve slides path
    slides_path = None
    if config.slides:
        slides_path = folder / config.slides
        if not slides_path.exists():
            raise FileNotFoundError(f"Slides not found: {slides_path}")
        logger.info(f"Found slides: {slides_path}")
    else:
        raise ValueError("No slides specified in presentation.yaml")
    
    # Resolve transcript path (optional - will fetch from video if not provided)
    transcript_path = None
    if config.transcript:
        transcript_path = folder / config.transcript
        if not transcript_path.exists():
            logger.warning(f"Transcript not found: {transcript_path}")
            transcript_path = None
        else:
            logger.info(f"Found transcript: {transcript_path}")
    
    # Set up outputs directory for all generated content
    output_dir = folder / 'outputs'
    output_dir.mkdir(exist_ok=True)
    
    # Generate the annotated write-up
    logger.info("Generating annotated write-up...")
    logger.info(f"Video: {video_source}")
    logger.info(f"Slides: {slides_path}")
    logger.info(f"Output dir: {output_dir}")
    if transcript_path:
        logger.info(f"Transcript: {transcript_path}")
    
    writeup = generate_annotated_talk_post(
        slide_path=str(slides_path),
        video_source=video_source,
        output_dir=str(output_dir),
        transcript_path=str(transcript_path) if transcript_path else None,
    )
    
    # Save the write-up in outputs folder
    output_path = output_dir / output_file
    output_path.write_text(writeup)
    logger.info(f"Write-up saved to: {output_path}")
    
    return writeup


def main():
    parser = argparse.ArgumentParser(
        description='Generate an annotated presentation write-up from a folder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'folder',
        type=Path,
        help='Path to the folder containing presentation.yaml'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='writeup.md',
        help='Output filename (default: writeup.md)'
    )
    
    args = parser.parse_args()
    
    if not args.folder.exists():
        logger.error(f"Folder not found: {args.folder}")
        sys.exit(1)
    
    yaml_path = args.folder / 'presentation.yaml'
    if not yaml_path.exists():
        logger.error(f"No presentation.yaml found in {args.folder}")
        sys.exit(1)
    
    try:
        generate_writeup(
            folder=args.folder,
            output_file=args.output,
        )
    except Exception as e:
        logger.error(f"{e}")
        sys.exit(1)


if __name__ == '__main__':
    load_dotenv()
    main()
