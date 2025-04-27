# downloader.py
from pathlib import Path

import typer

from .utils import move_files_by_type, scanner

app = typer.Typer()
DEFAULT_DOWNLOADS = Path.home() / "Downloads"


@app.command()
def auto(
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
    Organize (i.e. classify) files in the given folder.
    """
    try:
        src = Path.home() / src

        file = scanner(src)
        confirm = typer.confirm("Do you want to move these files?")
        if not confirm:
            typer.echo("Operation cancelled.")
            raise typer.Exit()
        move_files_by_type(file)
        typer.secho("✅ Done!", fg=typer.colors.GREEN)
    except Exception as e:
        typer.Abort(e)


if __name__ == "__main__":
    app()
