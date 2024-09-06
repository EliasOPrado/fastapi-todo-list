from db import models
from fastapi import FastAPI
from db.session import engine
from routers import todo

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(todo.router)
