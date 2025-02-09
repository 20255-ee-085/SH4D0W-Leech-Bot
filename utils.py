import re
import os
import logging
from typing import Optional
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def sanitize_filename(filename: str) -> str:
    """Sanitize filenames to prevent path traversal and invalid characters"""
    cleaned = re.sub(r'[^\w\-_. ()]', '', filename)
    cleaned = cleaned.replace('..', '')
    return cleaned[:220]  # Telegram filename length limit

def validate_url(url: str) -> bool:
    """Validate URL format and allowed domains"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        # Add domain allowlist if needed
        return True
    except:
        return False

async def generate_progress_bar(percentage: float, length: int = 20) -> str:
    """Generate visual progress bar"""
    filled = '█' * int(percentage / 100 * length)
    empty = '░' * (length - len(filled))
    return f"`[{filled}{empty}] {percentage:.1f}%`"

async def get_file_type(url: str) -> Optional[str]:
    """Detect file type from URL"""
    extensions = {
        '.pdf': 'document',
        '.mp4': 'video',
        '.m3u8': 'stream',
        '.jpg': 'photo',
        '.jpeg': 'photo',
        '.doc': 'document'
    }
    try:
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        return extensions.get(ext, 'unknown')
    except:
        return None

async def cleanup_temp_files():
    """Cleanup temporary download files"""
    try:
        for p in Path("downloads").glob("**/*"):
            if p.is_file():
                p.unlink()
        logger.info("Temporary files cleaned successfully")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")