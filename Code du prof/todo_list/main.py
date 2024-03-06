import uvicorn
from my_app.app import app


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
