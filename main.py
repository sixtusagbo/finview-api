from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Base route for the API"""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    """Route to get an item by ID"""
    return {"item_id": item_id, "q": q}
