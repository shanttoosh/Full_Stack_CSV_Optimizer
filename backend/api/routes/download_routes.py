"""
File download routes
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse
from pathlib import Path
import logging
import mimetypes

from ...services.file_handler import FileHandler

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize file handler
file_handler = FileHandler()

@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Download processed files
    
    Downloads files generated during processing including:
    - chunks.csv: All chunks in CSV format
    - embeddings.json: Embeddings and metadata in JSON format
    - metadata.json: Processing metadata
    - summary.json: Processing summary
    - results.zip: All files in a ZIP archive
    
    Args:
        file_id: File identifier (without extension)
        
    Returns:
        File download response
    """
    try:
        # Try to find the file with any supported extension
        file_path = file_handler.get_file_path(file_id)
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_id}")
            raise HTTPException(status_code=404, detail="File not found or expired")
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type is None:
            mime_type = "application/octet-stream"
        
        # Log download
        logger.info(f"File download: {file_path.name}")
        
        # Return file response
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_path.name}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error for file {file_id}: {e}")
        raise HTTPException(status_code=500, detail="Download failed")

@router.get("/download/{file_id}.{extension}")
async def download_file_with_extension(file_id: str, extension: str):
    """
    Download file with specific extension
    
    Args:
        file_id: File identifier
        extension: File extension (csv, json, zip)
        
    Returns:
        File download response
    """
    try:
        # Validate extension
        if extension not in ["csv", "json", "zip"]:
            raise HTTPException(status_code=400, detail="Unsupported file extension")
        
        # Get file path with extension
        file_path = file_handler.get_file_path(file_id, extension)
        
        if not file_path.exists():
            logger.warning(f"File not found: {file_id}.{extension}")
            raise HTTPException(status_code=404, detail="File not found or expired")
        
        # Determine MIME type based on extension
        mime_types = {
            "csv": "text/csv",
            "json": "application/json",
            "zip": "application/zip"
        }
        mime_type = mime_types.get(extension, "application/octet-stream")
        
        # Log download
        logger.info(f"File download: {file_path.name}")
        
        # Return file response
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_path.name}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error for file {file_id}.{extension}: {e}")
        raise HTTPException(status_code=500, detail="Download failed")

@router.get("/downloads/list")
async def list_available_downloads():
    """
    List available download files (for debugging/admin)
    
    Returns:
        List of available files in downloads directory
    """
    try:
        files = []
        downloads_dir = file_handler.downloads_dir
        
        for file_path in downloads_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size_bytes": stat.st_size,
                    "created_at": stat.st_ctime,
                    "modified_at": stat.st_mtime
                })
        
        return {
            "total_files": len(files),
            "files": files
        }
        
    except Exception as e:
        logger.error(f"Error listing downloads: {e}")
        raise HTTPException(status_code=500, detail="Failed to list downloads")

@router.delete("/downloads/cleanup")
async def cleanup_expired_files():
    """
    Manually trigger cleanup of expired files (admin endpoint)
    
    Returns:
        Cleanup status
    """
    try:
        # Get file count before cleanup
        downloads_dir = file_handler.downloads_dir
        files_before = len(list(downloads_dir.iterdir()))
        
        # Run cleanup
        file_handler.cleanup_expired_files()
        
        # Get file count after cleanup
        files_after = len(list(downloads_dir.iterdir()))
        
        cleaned_count = files_before - files_after
        
        logger.info(f"Cleanup completed: {cleaned_count} files removed")
        
        return {
            "success": True,
            "files_before": files_before,
            "files_after": files_after,
            "files_cleaned": cleaned_count,
            "message": f"Cleanup completed: {cleaned_count} files removed"
        }
        
    except Exception as e:
        logger.error(f"Cleanup error: {e}")
        raise HTTPException(status_code=500, detail="Cleanup failed")
