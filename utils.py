# classify.py
import datetime
from pathlib import Path

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


def scanner(src: Path) -> None:
    """
    Scan `src` (a directory) and print a Rich table classifying
    files by type: images, videos, documents, music, others.
    """
    table = Table(title=f"file Classified by Type ({src})")
    table.add_column("Image", style="cyan", no_wrap=True)
    table.add_column("Video", style="magenta")
    table.add_column("Document", style="green")
    table.add_column("Music", style="yellow")
    table.add_column("Others", style="red")

    all_files = [f for f in src.rglob("*") if f.is_file()]
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
