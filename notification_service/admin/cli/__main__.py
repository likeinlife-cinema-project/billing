import typer

from cli import template

app = typer.Typer(name="cli")

app.add_typer(template.router, name="template")

if __name__ == "__main__":
    app()
