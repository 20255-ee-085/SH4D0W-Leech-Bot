import os
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class Config:
    """Central configuration class with security enhancements"""
    
    def __init__(self):
        self.API_ID: int = int(os.getenv('API_ID', 0))
        self.API_HASH: str = os.getenv('API_HASH', '')
        self.BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
        self.ADMIN_ID: int = int(os.getenv('ADMIN_ID', 0))
        
        # Security configurations
        self.MAX_CONCURRENT_DOWNLOADS: int = int(os.getenv('MAX_CONCURRENT', 3))
        self.MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', 52428800))  # 50MB
        self.ALLOWED_CONTENT_TYPES: List[str] = [
            'text/plain',
            'application/pdf',
            'video/mp4',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        # Directory configurations
        self.DOWNLOAD_DIR: Path = Path(os.getenv('DOWNLOAD_DIR', 'downloads'))
        self.TEMP_DIR: Path = Path(os.getenv('TEMP_DIR', 'temp'))
        self.LOG_DIR: Path = Path(os.getenv('LOG_DIR', 'logs'))
        
        self._create_directories()
        self._validate()

    def _create_directories(self) -> None:
        """Create required directories with secure permissions"""
        try:
            self.DOWNLOAD_DIR.mkdir(exist_ok=True, mode=0o755)
            self.TEMP_DIR.mkdir(exist_ok=True, mode=0o700)
            self.LOG_DIR.mkdir(exist_ok=True, mode=0o700)
        except OSError as e:
            logger.error(f"Directory creation failed: {e}")
            raise

    def _validate(self) -> None:
        """Validate critical configurations"""
        if not all([self.API_ID, self.API_HASH, self.BOT_TOKEN]):
            raise ValueError("Missing required API configurations")
        
        if self.ADMIN_ID <= 0:
            raise ValueError("Invalid ADMIN_ID configuration")

    @property
    def to_dict(self) -> Dict[str, Any]:
        """Return configuration as dictionary for debugging"""
        return {
            'API_ID': self.API_ID,
            'API_HASH': '***' + self.API_HASH[-4:] if self.API_HASH else '',
            'BOT_TOKEN': '***' + self.BOT_TOKEN[-4:] if self.BOT_TOKEN else '',
            'ADMIN_ID': self.ADMIN_ID,
            'MAX_CONCURRENT_DOWNLOADS': self.MAX_CONCURRENT_DOWNLOADS,
            'MAX_FILE_SIZE': self.MAX_FILE_SIZE
        }

# Initialize configuration
settings = Config()