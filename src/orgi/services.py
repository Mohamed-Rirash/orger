import datetime
import re
import shutil
from pathlib import Path
from typing import List, Union

from rich.console import Console
from rich.progress import track
from rich.table import Table

console = Console()

# Common file extension sets for quick membership tests
IMAGE_EXTS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
    ".webp",
    ".heic",
    ".ico",
    ".svg",
    ".raw",
    ".psd",
    ".ai",
    ".eps",
}
DOCUMENT_EXTS = {
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    ".txt",
    ".rtf",
    ".odt",
    ".ods",
    ".odp",
    ".csv",
    ".md",
    ".json",
    ".xml",
    ".yaml",
    ".yml",
}
VIDEO_EXTS = {
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".mpeg",
    ".mpg",
    ".3gp",
    ".m4v",
    ".ts",
    ".ogv",
}
MUSIC_EXTS = {
    ".mp3",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
    ".wma",
    ".m4a",
    ".opus",
    ".alac",
    ".aiff",
}


console = Console()

# (your IMAGE_EXTS, VIDEO_EXTS, DOCUMENT_EXTS, MUSIC_EXTS as before…)


def scanner(src: Union[Path, List[Path]]) -> List[Path]:
    """
    Scan `src` (a directory or list of files), print a Rich table classifying
    files by type: images, videos, documents, music, others,
    and return the list of all files found.
    """
    table = Table(title="Files Classified by Type")
    table.add_column("Image", style="cyan", no_wrap=True)
    table.add_column("Video", style="magenta")
    table.add_column("Document", style="green")
    table.add_column("Music", style="yellow")
    table.add_column("Others", style="red")

    # gather and classify
    all_files: List[Path] = []
    
    if isinstance(src, Path):
        # If src is a directory, scan it
        if src.is_dir():
            all_files = [f for f in src.rglob("*") if f.is_file()]
            table.title = f"Files Classified by Type ({src})"
    else:
        # If src is a list of files
        all_files = src
        table.title = f"Files Classified by Type ({len(all_files)} files)"
    
    for file in track(all_files, description="Scanning files...", total=len(all_files)):
        ext = "".join(file.suffixes).lower()
        created = datetime.datetime.fromtimestamp(file.stat().st_ctime)

        if ext in IMAGE_EXTS:
            col = 0
        elif ext in VIDEO_EXTS:
            col = 1
        elif ext in DOCUMENT_EXTS:
            col = 2
        elif ext in MUSIC_EXTS:
            col = 3
        else:
            col = 4

        row = ["", "", "", "", ""]
        row[col] = f"{file.name} ({created:%Y-%m-%d %H:%M:%S})"
        table.add_row(*row)

    console.print(table)
    return all_files


def move_files_by_type(files: List[Path]) -> None:
    """
    Move each Path in `files` into ~/images/<date>/, ~/videos/<date>/, etc.,
    based on its extension. Creates all dirs as needed.
    """
    # YYYY-MM-DD today's date
    date_str = datetime.date.today().isoformat()
    home = Path.home()

    # map category → destination base dir
    category_dirs = {
        "image": home / "images" / date_str,
        "video": home / "videos" / date_str,
        "document": home / "documents" / date_str,
        "music": home / "music" / date_str,
        "others": home / "others" / date_str,
    }

    # make sure all target dirs exist
    for dest in category_dirs.values():
        dest.mkdir(parents=True, exist_ok=True)

    for file in track(files, description="Moving files...", total=len(files)):
        # skip if somehow not a file
        if not file.is_file():
            continue

        ext = "".join(file.suffixes).lower()

        if ext in IMAGE_EXTS:
            category = "image"
        elif ext in VIDEO_EXTS:
            category = "video"
        elif ext in DOCUMENT_EXTS:
            category = "document"
        elif ext in MUSIC_EXTS:
            category = "music"
        else:
            category = "others"

        dest_dir = category_dirs[category]
        dest_path = dest_dir / file.name

        # move the file
        shutil.move(str(file), str(dest_path))


def is_date_like_dir(dirname: str) -> bool:
    """
    Check if a directory name appears to be a date format.
    Supports ISO format (YYYY-MM-DD) and other common date formats.
    
    Args:
        dirname: Name of the directory to check
        
    Returns:
        True if the directory name looks like a date, False otherwise
    """
    # ISO format YYYY-MM-DD
    if re.match(r'^\d{4}-\d{2}-\d{2}$', dirname):
        return True
    
    # Other common date formats
    patterns = [
        r'^\d{4}_\d{2}_\d{2}$',  # YYYY_MM_DD
        r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
        r'^\d{2}_\d{2}_\d{4}$',  # MM_DD_YYYY
        r'^\d{8}$',              # YYYYMMDD
    ]
    
    for pattern in patterns:
        if re.match(pattern, dirname):
            return True
    
    return False


def scan_files_for_organization(src: Path) -> List[Path]:
    """
    Scan files for organization, skipping date-like directories.
    
    Args:
        src: Source directory to scan
        
    Returns:
        List of files to be organized
    """
    files = []
    
    for item in src.iterdir():
        if item.is_dir():
            if is_date_like_dir(item.name):
                console.print(f"[yellow]Skipping previously organized directory: {item.name}[/yellow]")
                continue
            # Recursively scan non-date directories
            for file in item.rglob("*"):
                if file.is_file():
                    files.append(file)
        elif item.is_file():
            files.append(item)
    
    return files


def display_files_by_type(files: List[Path]) -> None:
    """
    Display files classified by type in a Rich table.
    
    Args:
        files: List of files to display
    """
    table = Table(title=f"Files Classified by Type ({len(files)} files)")
    table.add_column("Image", style="cyan", no_wrap=True)
    table.add_column("Video", style="magenta")
    table.add_column("Document", style="green")
    table.add_column("Music", style="yellow")
    table.add_column("Others", style="red")
    
    for file in track(files, description="Classifying files...", total=len(files)):
        ext = "".join(file.suffixes).lower()
        created = datetime.datetime.fromtimestamp(file.stat().st_ctime)

        if ext in IMAGE_EXTS:
            col = 0
        elif ext in VIDEO_EXTS:
            col = 1
        elif ext in DOCUMENT_EXTS:
            col = 2
        elif ext in MUSIC_EXTS:
            col = 3
        else:
            col = 4

        row = ["", "", "", "", ""]
        row[col] = f"{file.name} ({created:%Y-%m-%d %H:%M:%S})"
        table.add_row(*row)

    console.print(table)


def organize_files_by_date(files: List[Path], date_dir: Path) -> None:
    """
    Organize files into a date-named directory with subdirectories for different file types.
    Only moves files with recognized extensions to their respective subdirectories.
    
    Args:
        files: List of files to organize
        date_dir: Path to the date-named directory where files will be organized
    """
    # Create category subdirectories
    category_dirs = {
        "images": date_dir / "images",
        "videos": date_dir / "videos",
        "documents": date_dir / "documents",
        "music": date_dir / "music",
    }
    
    # Make sure all target dirs exist
    date_dir.mkdir(parents=True, exist_ok=True)
    for dest in category_dirs.values():
        dest.mkdir(parents=True, exist_ok=True)
    
    # Track files moved and skipped
    moved_count = 0
    skipped_count = 0
    
    for file in track(files, description="Organizing files...", total=len(files)):
        # Skip if somehow not a file
        if not file.is_file():
            skipped_count += 1
            continue
        
        ext = "".join(file.suffixes).lower()
        
        # Determine the appropriate category
        if ext in IMAGE_EXTS:
            dest_dir = category_dirs["images"]
        elif ext in VIDEO_EXTS:
            dest_dir = category_dirs["videos"]
        elif ext in DOCUMENT_EXTS:
            dest_dir = category_dirs["documents"]
        elif ext in MUSIC_EXTS:
            dest_dir = category_dirs["music"]
        else:
            # Skip files with unrecognized extensions
            skipped_count += 1
            continue
        
        dest_path = dest_dir / file.name
        
        # Handle filename conflicts
        if dest_path.exists():
            base_name = file.stem
            extension = file.suffix
            counter = 1
            while dest_path.exists():
                new_name = f"{base_name}_{counter}{extension}"
                dest_path = dest_dir / new_name
                counter += 1
        
        # Move the file
        try:
            shutil.move(str(file), str(dest_path))
            moved_count += 1
        except Exception as e:
            console.print(f"[red]Error moving {file}: {e}[/red]")
            skipped_count += 1
    
    console.print(f"[green]Organized {moved_count} files into {date_dir}[/green]")
    if skipped_count > 0:
        console.print(f"[yellow]Skipped {skipped_count} files (unrecognized types or errors)[/yellow]")
