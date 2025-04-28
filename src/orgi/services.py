
import datetime
import shutil
from pathlib import Path
from typing import List

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


def scanner(src: Path) -> List[Path]:
    """
    Scan `src` (a directory), print a Rich table classifying
    files by type: images, videos, documents, music, others,
    and return the list of all files found.
    """
    table = Table(title=f"Files Classified by Type ({src})")
    table.add_column("Image", style="cyan", no_wrap=True)
    table.add_column("Video", style="magenta")
    table.add_column("Document", style="green")
    table.add_column("Music", style="yellow")
    table.add_column("Others", style="red")

    # gather and classify
    all_files: List[Path] = [f for f in src.rglob("*") if f.is_file()]
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
    # YYYY-MM-DD today’s date
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
