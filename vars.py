import os
import re

API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))
MAX_CONCURRENT_DOWNLOADS = int(os.environ.get('MAX_CONCURRENT', 3))
MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 52428800))  # 50MB

class Config:
    DOWNLOAD_DIR = "downloads"
    ALLOWED_CONTENT_TYPES = [
        'text/plain',
        'application/pdf',
        'video/mp4',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]