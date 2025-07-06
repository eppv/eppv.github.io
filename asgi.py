from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.routing import Mount

def create_app(site_dir: str = "docs"):
    return Starlette(
        routes=[
            Mount("/", app=StaticFiles(directory=site_dir, html=True), name="static"),
        ]
    )
