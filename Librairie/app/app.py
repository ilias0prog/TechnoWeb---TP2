from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.routes.books import router as book_router

templates = Jinja2Templates(directory="Librairie\Templates")


app = FastAPI(title="My bookstore")
app.include_router(book_router)

@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    # Renvoyer la réponse HTML en utilisant le modèle index.html
    return templates.TemplateResponse("all_books.html", {"request": request})

@app.on_event('startup')
def on_startup():
    print("Server started.")
def on_shutdown():
    print("Bye bye!")