# downloader.py
from pathlib import Path

import typer

from utils import scanner

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
    src = Path.home() / src

    scanner(src)
    confirm = typer.confirm("Do you want to move these files?")
    if not confirm:
        typer.echo("Operation cancelled.")
        raise typer.Exit()


if __name__ == "__main__":
    app()
