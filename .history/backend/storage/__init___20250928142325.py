"""
Storage management for CSV Chunking Optimizer Pro.
"""

import os

# Storage directories
TEMP_FILES_DIR = os.path.join(os.path.dirname(__file__), "temp_files")
DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), "downloads")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), ".chroma")
FAISS_DIR = os.path.join(os.path.dirname(__file__), ".faiss")

# Ensure directories exist
for directory in [TEMP_FILES_DIR, DOWNLOADS_DIR, CHROMA_DIR, FAISS_DIR]:
    os.makedirs(directory, exist_ok=True)

__all__ = [
    "TEMP_FILES_DIR",
    "DOWNLOADS_DIR", 
    "CHROMA_DIR",
    "FAISS_DIR"
]
