import datetime
from pathlib import Path

import typer

from .services import (DOCUMENT_EXTS, IMAGE_EXTS, MUSIC_EXTS, VIDEO_EXTS,
                       display_files_by_type, is_date_like_dir,
                       organize_files_by_date, scan_files_for_organization)

app = typer.Typer()
DEFAULT_DOWNLOADS = Path.home() / "Downloads"


@app.command("sort-home")
def sort_home(
    src: Path = typer.Option(
        DEFAULT_DOWNLOADS,
        "--src",
        "-s",
        help="Source folder (defaults to your Downloads).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Sort files into home directory.
    Creates subdirectories for images, videos, documents, and music in the Home directory.
    Files with unrecognized extensions are left untouched.
    """
    try:
        # Scan files, skipping date-like directories
        typer.echo(f"Scanning files in {src}...")
        files = scan_files_for_organization(src)

        if not files:
            typer.echo("No files found to organize.")
            raise typer.Exit()

        # Display files to be organized
        display_files_by_type(files)

        # Confirm with user
        confirm = typer.confirm(
            "Do you want to organize these files into your Home directory?"
        )
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()

        # Set up destination in home directory
        home = Path.home()

        # Create category directories in home
        category_dirs = {
            "images": home / "images",
            "videos": home / "videos",
            "documents": home / "documents",
            "music": home / "music",
        }

        # Make sure category directories exist
        for dir_path in category_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        # Get today's date for subdirectories
        today = datetime.date.today().isoformat()

        # Create date subdirectories in each category
        date_dirs = {}
        for category, dir_path in category_dirs.items():
            date_dir = dir_path / today
            date_dir.mkdir(parents=True, exist_ok=True)
            date_dirs[category] = date_dir

        # Organize files into date subdirectories in each category
        moved_count = 0
        skipped_count = 0

        for file in typer.progressbar(files, label="Organizing files..."):
            # Skip if somehow not a file
            if not file.is_file():
                skipped_count += 1
                continue

            ext = "".join(file.suffixes).lower()

            # Determine the appropriate category
            if ext in IMAGE_EXTS:
                dest_dir = date_dirs["images"]
            elif ext in VIDEO_EXTS:
                dest_dir = date_dirs["videos"]
            elif ext in DOCUMENT_EXTS:
                dest_dir = date_dirs["documents"]
            elif ext in MUSIC_EXTS:
                dest_dir = date_dirs["music"]
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
                import shutil

                shutil.move(str(file), str(dest_path))
                moved_count += 1
            except Exception as e:
                typer.echo(f"Error moving {file}: {e}")
                skipped_count += 1

        typer.secho(
            f"✅ Organized {moved_count} files into your Home directory!",
            fg=typer.colors.GREEN,
        )
        if skipped_count > 0:
            typer.echo(f"Skipped {skipped_count} files (unrecognized types or errors)")
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()


@app.command("sort-here")
def sort_here(
    src: Path = typer.Option(
        ...,
        "--src",
        "-s",
        help="Source folder (it organizes files in here and skips if the folder name is date like name).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
):
    """
    Sort files in the current location.
    Creates a date-named folder with subdirectories for images, videos, documents, and music.
    Files with unrecognized extensions are left untouched.
    """
    try:
        # Check if the source directory itself is date-like
        if is_date_like_dir(src.name):
            typer.echo(
                f"The directory '{src.name}' appears to be a date-formatted directory. Skipping."
            )
            raise typer.Exit()

        # Create today's date folder within the source directory
        today = datetime.date.today().isoformat()
        date_dir = src / today

        # Scan files, skipping date-like directories
        typer.echo(f"Scanning files in {src}...")
        files = scan_files_for_organization(src)

        if not files:
            typer.echo("No files found to organize.")
            raise typer.Exit()

        # Display files to be organized
        display_files_by_type(files)

        # Confirm with user
        confirm = typer.confirm(f"Do you want to organize these files into {date_dir}?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()

        # Organize files
        organize_files_by_date(files, date_dir)
        typer.secho("✅ Files organized successfully!", fg=typer.colors.GREEN)
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()


@app.command("sort-to")
def sort_to(
    src: Path = typer.Option(
        ...,
        "--src",
        "-s",
        help="Source folder to organize files from.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    dest: Path = typer.Option(
        ...,
        "--dest",
        "-d",
        help="Destination folder where organized files will be placed.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
    ),
):
    """
    Sort files to a specific destination.
    Creates a date-named folder with subdirectories for images, videos, documents, and music.
    Files with unrecognized extensions are left untouched.
    """
    try:
        # Create today's date folder within the destination directory
        today = datetime.date.today().isoformat()
        date_dir = dest / today

        # Scan files, skipping date-like directories
        typer.echo(f"Scanning files in {src}...")
        files = scan_files_for_organization(src)

        if not files:
            typer.echo("No files found to organize.")
            raise typer.Exit()

        # Display files to be organized
        display_files_by_type(files)

        # Confirm with user
        confirm = typer.confirm(f"Do you want to organize these files into {date_dir}?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()

        # Organize files
        organize_files_by_date(files, date_dir)
        typer.secho("✅ Files organized successfully!", fg=typer.colors.GREEN)
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()


if __name__ == "__main__":
    app()
