from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=False)
