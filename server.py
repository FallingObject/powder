from fastapi import FastAPI
from os import getcwd
from fastapi.responses import FileResponse
import os, json
import uvicorn

CONFIG = json.load(open("config.json"))

app = FastAPI()


@app.get("/file/{name_file}")
async def get_file(name_file: str):
    return FileResponse(path=getcwd() + "\screenshots\\" + name_file)


@app.get("/file")
async def get_file():
    uri = f'http://{CONFIG["server"]["host"]}:{CONFIG["server"]["port"]}/file'
    images = [
        file.replace(".png", "")
        for file in os.listdir(getcwd() + "./screenshots")
        if file.endswith(".png")
    ]
    x = {}  # a werid way to do this, but it works
    for i in images:
        x[i] = uri + "/" + i + ".png"
    return x


@app.get("/")
async def read_root():
    return {"/root": "bruh moment here `/file` to see the screenshots"}


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=CONFIG["server"]["host"],
        port=CONFIG["server"]["port"],
        log_level="info",
    )
