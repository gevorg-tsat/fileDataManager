from pydantic import BaseModel

class ColumnData(BaseModel):
    column_name : str
    data : list