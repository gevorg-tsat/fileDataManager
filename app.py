import uvicorn
import fastapi
import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from config import HOST, PORT, FILES_STORAGE_DIRECTORY

app = fastapi.FastAPI()

origins = [
    "*"
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"]
)


@app.get("/")
async def root():
    return RedirectResponse(f"http://{HOST}:{PORT}/docs")



@app.post("/uploadfile/")
async def create_upload_file(in_file: UploadFile):
    out_file_path = FILES_STORAGE_DIRECTORY + "/" + in_file.filename
    try:
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await in_file.read(1024):  # async read chunk
                await out_file.write(content)
    except:
        return HTTPException(500)
    return {"STATUS": "OK"}

@app.get("/files")
async def get_files() -> list[str]:
    return os.listdir(FILES_STORAGE_DIRECTORY)

if __name__ == "__main__":
    uvicorn.run("app:app", port=PORT, host=HOST, reload=False)
