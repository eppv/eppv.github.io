import os
import subprocess
import typer
import uvicorn
from asgi import create_app
app = typer.Typer()

@app.command()
def build(src: str = ".", sitedir: str = "docs"):
    eng_dir = "docs_src/en"
    ru_dir = "docs_src/ru"
    typer.echo("Building main site (eng)...")
    subprocess.run(["mkdocs", "build","--config-file", f"{eng_dir}/mkdocs.yml", "--site-dir", f"../../{sitedir}"])
    typer.echo("Building ru site...")
    subprocess.run(["mkdocs", "build","--config-file", f"{ru_dir}/mkdocs.yml", "--site-dir", f"../../{sitedir}/ru/"])
    typer.echo("Done.")


@app.command()
def serve(site: str = "docs", host: str = "0.0.0.0", port: int = 8008, reload: bool = False):
    if not os.path.exists(site):
        typer.echo(f"Error: Directory '{site}' not found. Trying build a site first.")
        try:
            build(site)
        except Exception as e:
            typer.echo(f"Error: Failed to build site: {e}", err=True)
            raise typer.Exit(code=1)

    if reload:
        os.environ["SITE_DIR"] = os.path.abspath(site)
        uvicorn.run(
            "asgi:create_app",
            host=host,
            port=port,
            reload=reload,
            factory=True,
            env_file=".env"
        )
        typer.echo(f"Serving site on http://{host}:{port} with reload")
    else:
        app = create_app(site)
        typer.echo(f"Serving site on http://{host}:{port}")
        uvicorn.run(app, host=host, port=port)


@app.command()
def clean(site: str = "docs"):
    typer.echo("Cleaning site...")
    subprocess.run(["rm", "-rf", site])
    typer.echo("Done.")


if __name__ == "__main__":
    app()
