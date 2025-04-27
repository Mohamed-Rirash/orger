import typer

app = typer.Typer()


@app.command(help="starting")
def hello():
    typer.echo("hello")


if __name__ == "__main__":
    typer.run(hello)
