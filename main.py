from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    content = {"request": request}
    return templates.TemplateResponse("index.html", content)


@app.post("/", response_class=HTMLResponse)
async def echo_text(request: Request):
    def format(msg: str):
        return [x.split("=") for x in msg.strip().split("")]

    form_data = await request.form()
    raw_message = form_data["message"]
    content = {
        "request": request,
        "raw_message": raw_message,
        "fix_data": format(raw_message),
    }
    return templates.TemplateResponse("index.html", content)
