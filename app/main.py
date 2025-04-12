from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routes import index, blog, game
from app.routes.state import game_state

app = FastAPI(title="Live Resume")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(index.router)
app.include_router(blog.router)
app.include_router(game.router)

# Expose the app instance at the module level
__all__ = ["app"]