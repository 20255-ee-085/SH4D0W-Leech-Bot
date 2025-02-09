import asyncio
import aiohttp
import yt_dlp as youtube_dl
import re
from typing import Dict
from pathlib import Path
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

async def download_manager(links: list, user_data: Dict, progress_msg, semaphore):
async def download_manager(links: list, user_data: Dict, progress_msg, semaphore):
    results = {'success': 0, 'failed': 0, 'pdfs': 0, 'videos': 0}
    total = len(links)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for idx, url in enumerate(links):
            task = asyncio.create_task(
                download_file(
                    url,
                    idx+1,
                    total,
                    session,
                    user_data,
                    progress_msg,
                    semaphore
                )
            )
            tasks.append(task)
        
        for task in asyncio.as_completed(tasks):
            result = await task
            if result['status'] == 'success':
                results['success'] += 1
                if result['type'] == 'pdf':
                    results['pdfs'] += 1
                else:
                    results['videos'] += 1
            else:
                results['failed'] += 1
                
    return results

async def download_file(url, current, total, session, user_data, progress_msg, semaphore):
    async with semaphore:
        try:
            parsed = urlparse(url)
            filename = sanitize_filename(Path(parsed.path).name)
            
            if 'pdf' in filename.lower():
                file_type = 'pdf'
                async with session.get(url) as response:
                    content = await response.read()
                    Path(f"downloads/{user_data['batch_name']}").mkdir(exist_ok=True)
                    with open(f"downloads/{user_data['batch_name']}/{filename}", 'wb') as f:
                        f.write(content)
            else:
                file_type = 'video'
                ydl_opts = {
                    'format': f'bestvideo[height<={user_data["resolution"]}]+bestaudio/best[height<={user_data["resolution"]}]',
                    'outtmpl': f'downloads/{user_data["batch_name"]}/{filename}',
                    'progress_hooks': [lambda d: progress_hook(d, progress_msg, current, total)],
                }
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    await asyncio.to_thread(ydl.download, [url])
            
            return {'status': 'success', 'type': file_type}
        except Exception as e:
            logger.error(f"Download failed for {url}: {e}")
            return {'status': 'failed', 'type': None}

def progress_hook(d, progress_msg, current, total):
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        progress = f"""
        🔄 Downloading {current}/{total}
        📦 {d['filename']}
        🚀 Speed: {speed}
        ⏳ ETA: {eta}
        {generate_progress_bar(float(d['_percent']))}
        """
        asyncio.create_task(update_progress(progress_msg, progress))

async def update_progress(progress_msg, text):
    try:
        await progress_msg.edit_text(text)
    except Exception as e:
        logger.error(f"Progress update failed: {e}")

def generate_progress_bar(percentage: float, length: int = 20):
    filled = '█' * int(percentage / 100 * length)
    empty = '░' * (length - len(filled))
    return f"|{filled}{empty}| {percentage:.1f}%"

def validate_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r'[^\w\-_. ]', '', filename)
    return cleaned[:255]  # Limit filename length