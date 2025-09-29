"""
Application settings and configuration
"""

import os
from pathlib import Path
from typing import Optional

class Settings:
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "CSV Chunking Optimizer Pro API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Complete CSV processing, chunking, embedding, and retrieval API"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))  # 100MB default
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS: list = [".csv"]
    
    # Storage Configuration
    BASE_DIR: Path = Path(__file__).parent.parent
    TEMP_FILES_DIR: Path = BASE_DIR / "backend" / "storage" / "temp_files"
    DOWNLOADS_DIR: Path = BASE_DIR / "backend" / "storage" / "downloads"
    CHROMA_DIR: Path = BASE_DIR / "backend" / "storage" / ".chroma"
    FAISS_DIR: Path = BASE_DIR / "backend" / "storage" / ".faiss"
    
    # Processing Configuration
    DEFAULT_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    DEFAULT_BATCH_SIZE: int = 32
    DEFAULT_TOP_K: int = 5
    DEFAULT_SIMILARITY_METRIC: str = "cosine"
    
    # File Retention (in hours)
    FILE_RETENTION_HOURS: int = int(os.getenv("FILE_RETENTION_HOURS", "24"))
    
    # Rate Limiting (requests per minute)
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # CORS Configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    
    # Layer Default Configurations
    LAYER_1_DEFAULTS = {
        "preprocessing": {
            "remove_duplicates": True,
            "text_processing": "skip"
        },
        "chunking": {
            "method": "fixed",
            "chunk_size": 100,
            "overlap": 0
        },
        "embedding": {
            "model": "all-MiniLM-L6-v2",
            "batch_size": 32
        },
        "storage": {
            "type": "chroma",
            "similarity_metric": "cosine"
        }
    }
    
    LAYER_2_DEFAULTS = {
        "preprocessing": {
            "remove_duplicates": True,
            "remove_stopwords": False,
            "text_processing": "skip"
        },
        "chunking": {
            "method": "semantic",
            "n_clusters": 5
        },
        "embedding": {
            "model": "all-MiniLM-L6-v2",
            "batch_size": 64
        },
        "storage": {
            "type": "chroma",
            "similarity_metric": "cosine"
        }
    }
    
    LAYER_3_DEFAULTS = {
        "preprocessing": {
            "type_conversions": {},
            "null_handling": {},
            "remove_duplicates": False,
            "remove_stopwords": False,
            "text_processing": "skip"
        },
        "chunking": {
            "method": "document_based",
            "token_limit": 2000,
            "key_column": None
        },
        "embedding": {
            "model": "BAAI/bge-small-en-v1.5",
            "batch_size": 64
        },
        "storage": {
            "type": "faiss",
            "similarity_metric": "cosine"
        }
    }
    
    def __init__(self):
        # Ensure directories exist
        for directory in [self.TEMP_FILES_DIR, self.DOWNLOADS_DIR, self.CHROMA_DIR, self.FAISS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_layer_defaults(self, layer_mode: str) -> dict:
        """Get default settings for a layer mode"""
        if layer_mode == "fast":
            return self.LAYER_1_DEFAULTS.copy()
        elif layer_mode == "config":
            return self.LAYER_2_DEFAULTS.copy()
        elif layer_mode == "deep":
            return self.LAYER_3_DEFAULTS.copy()
        else:
            raise ValueError(f"Unknown layer mode: {layer_mode}")

# Global settings instance
settings = Settings()
