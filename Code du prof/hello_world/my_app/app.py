from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()
app.mount("/files", StaticFiles(directory="static"))

@app.get("/say/hello")
def say_hello():
    response = {
        'message': 'Hello World!',
    }
    return JSONResponse(response)
