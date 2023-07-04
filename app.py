import uvicorn
import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from fastapi.responses import RedirectResponse
from typing import Annotated
from fastapi import UploadFile, HTTPException, Query, File
import os
import pandas
from typing import Annotated

from config import HOST, PORT, FILES_STORAGE_DIRECTORY
from models import ColumnData

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
async def create_uploaded_file(in_file: Annotated[UploadFile, File(description="CSV file")]):
    if in_file.content_type != "text/csv":
        return HTTPException(400, detail="Wrong data type")
    out_file_path = FILES_STORAGE_DIRECTORY + "/" + in_file.filename
    try:
        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await in_file.read(1024):  # async read chunk
                await out_file.write(content)
    except:
        return HTTPException(500)
    return {"STATUS": "OK"}

@app.post("/uploadfiles")
async def create_uploaded_files(files: list[Annotated[UploadFile, File(description="CSV file")]]):
    for file in files:
        result = await create_uploaded_file(file)
        if isinstance(result, HTTPException):
            return result
    return {"STATUS": "OK"}
    
@app.delete("/deletefile")
async def delete_file(filename: str):
    uploaded_files = await get_filenames()
    if filename in uploaded_files:
        os.remove(FILES_STORAGE_DIRECTORY + "/" + filename)
        return {"STATUS": "OK"}
    return HTTPException(404)
    

@app.get("/files")
async def get_filenames() -> list[str]:
    return [f for f in os.listdir(FILES_STORAGE_DIRECTORY) if not f.startswith('.')]


@app.get("/file")
async def get_file_data(
        filename : str,
        limits : Annotated[int | None, Query(gt=0)] = None,
        columns : Annotated[str | None, Query(description="Column names that will be shown. Separated by commas")] = None,
        sortby : Annotated[str | None, Query(description="Columns which by to sort. Separated by commas")] = None,
        separator : Annotated[str, Query(description="separator in csv file")] = ","
    ) -> list[ColumnData]:

    if columns:
        columns = set(map(str.strip, columns.split(",")))
    
    if sortby:
        sortby = list(map(str.strip, sortby.split(",")))
    df = pandas.read_csv(
        filepath_or_buffer=FILES_STORAGE_DIRECTORY + "/" + filename,
        sep=separator
    )
    if columns:
        response = [] * len(columns)
    else:
        response = [] * len(df.columns)
    
    if sortby:
        df = df.sort_values(by = sortby)
    
    for clm in df.columns:
        if columns and clm not in columns:
            continue
        data = df[clm].tolist()
        if limits:
            data = data[:limits]
        response.append(ColumnData(column_name=clm, data=data))
        
    return response

if __name__ == "__main__":
    uvicorn.run("app:app", port=PORT, host=HOST, reload=False)
