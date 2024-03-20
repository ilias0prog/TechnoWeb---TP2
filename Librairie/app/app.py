from fastapi import FastAPI,Request,status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routes.books import router as book_router

from fastapi.staticfiles import StaticFiles


templates = Jinja2Templates(directory="Librairie\Templates")


app = FastAPI(title="My bookstore")
app.include_router(book_router)

@app.get("/")
def route(request: Request):
    return RedirectResponse("./books/all", status_code= status.HTTP_303_SEE_OTHER)

app.mount("/static", StaticFiles(directory="Librairie/static"), name="static")

@app.on_event('startup')
def on_startup():
    print("Server started.")
def on_shutdown():
    print("Bye bye!")




