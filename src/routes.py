import logging
from fastapi import Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from .config import Config
from src.db.database import Database
from src.utils.api import final_correcting

router = APIRouter()
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=Config.TEMPLATES_DIR) 


@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/login")
async def login(request: Request, login: str = Form(...), password: str = Form(...)):
    username = None
    db = request.app.state.db
    username = await db.check_auth(login=login, password=password)

    if username:
        logger.info(f'User -{username}- has successfully logged in')
        return RedirectResponse(url=f"/notes?username={username}", status_code=302)
    else:
        logger.warning(f'User -{username}- has input incorrect data')
        return templates.TemplateResponse("index.html", {"request": request, "error": "Неверный логин или пароль"})


@router.get("/notes", response_class=HTMLResponse)
async def notes(username: str, request: Request):
    db = request.app.state.db
    user, notes = await db.get_user_notes(username)

    if user:
        return templates.TemplateResponse("notes.html", {"request": request, "username": user.username, "notes": notes})
    else:
        return RedirectResponse(url="/")


@router.post("/add_note")
async def add_note(request: Request, content: str = Form(...), username: str = Form(...)):
    db = request.app.state.db
    correct_content = final_correcting(content)
    note = await db.add_note(username=username, content=correct_content)

    if not note:
        return {"error": "User not found"}

    logger.info(f'User -{username}- added a note: {correct_content}')
    return RedirectResponse(url=f"/notes?username={username}", status_code=303)
