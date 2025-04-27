from pathlib import Path

import typer

app = typer.Typer()

DEFAULT_DOWNLOADS = Path.home() / "Downloads"


@app.command()
def auto(
    src: Path = typer.Option(
        DEFAULT_DOWNLOADS,
        "--src",
        "-s",
        help="Source folder (defaults to your Downloads).  You can also do `--src ~/Desktop` or give an absolute path.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,  # expanduser + realpath
    ),
):
    typer.echo(f"Organizing files in {Path.home() / src}")


if __name__ == "__main__":
    app()
