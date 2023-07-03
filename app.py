import uvicorn
import fastapi
import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import json
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi import FastAPI, File, UploadFile

HOST = "0.0.0.0"
PORT=8081

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
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}



if __name__ == "__main__":
    uvicorn.run("app:app", port=PORT, host=HOST, reload=False)
