from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Base route for the API"""
    return {"Hello": "World"}
