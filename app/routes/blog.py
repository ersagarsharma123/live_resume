from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/blog")
async def blog(request: Request):
    return templates.TemplateResponse("blog.html", {"request": request})