"""
Cleanup utility script for temporary files
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def cleanup_files():
    """Clean up expired files"""
    try:
        from config.settings import settings
        from backend.services.file_handler import FileHandler
        
        print("🧹 Starting file cleanup...")
        
        file_handler = FileHandler()
        
        # Get file counts before cleanup
        temp_files_before = len(list(settings.TEMP_FILES_DIR.glob("*")))
        download_files_before = len(list(settings.DOWNLOADS_DIR.glob("*")))
        
        # Run cleanup
        file_handler.cleanup_expired_files()
        
        # Get file counts after cleanup
        temp_files_after = len(list(settings.TEMP_FILES_DIR.glob("*")))
        download_files_after = len(list(settings.DOWNLOADS_DIR.glob("*")))
        
        temp_cleaned = temp_files_before - temp_files_after
        download_cleaned = download_files_before - download_files_after
        total_cleaned = temp_cleaned + download_cleaned
        
        print(f"✅ Cleanup completed:")
        print(f"   📁 Temp files: {temp_files_before} → {temp_files_after} ({temp_cleaned} removed)")
        print(f"   📁 Download files: {download_files_before} → {download_files_after} ({download_cleaned} removed)")
        print(f"   📊 Total files removed: {total_cleaned}")
        
        if total_cleaned == 0:
            print("   ℹ️  No expired files found")
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        sys.exit(1)

def list_files():
    """List all files in storage directories"""
    try:
        from config.settings import settings
        
        print("📋 Listing storage files...")
        
        directories = [
            ("Temp Files", settings.TEMP_FILES_DIR),
            ("Download Files", settings.DOWNLOADS_DIR),
            ("ChromaDB", settings.CHROMA_DIR),
            ("FAISS", settings.FAISS_DIR)
        ]
        
        for name, directory in directories:
            if directory.exists():
                files = list(directory.rglob("*"))
                files = [f for f in files if f.is_file()]
                
                print(f"\n📁 {name} ({directory}):")
                if files:
                    total_size = sum(f.stat().st_size for f in files)
                    print(f"   Files: {len(files)}")
                    print(f"   Total size: {total_size / 1024 / 1024:.2f} MB")
                    
                    for file_path in files[:10]:  # Show first 10 files
                        size = file_path.stat().st_size
                        modified = datetime.fromtimestamp(file_path.stat().st_mtime)
                        print(f"   - {file_path.name} ({size} bytes, {modified.strftime('%Y-%m-%d %H:%M:%S')})")
                    
                    if len(files) > 10:
                        print(f"   ... and {len(files) - 10} more files")
                else:
                    print("   No files found")
            else:
                print(f"\n📁 {name}: Directory does not exist")
        
    except Exception as e:
        print(f"❌ List files failed: {e}")
        sys.exit(1)

def main():
    """Main cleanup script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CSV Chunking Optimizer Pro - File Cleanup Utility")
    parser.add_argument("--list", action="store_true", help="List files instead of cleaning")
    parser.add_argument("--force", action="store_true", help="Force cleanup all files regardless of age")
    
    args = parser.parse_args()
    
    if args.list:
        list_files()
    else:
        if args.force:
            print("⚠️  Force cleanup not implemented yet - use regular cleanup")
        cleanup_files()

if __name__ == "__main__":
    main()
