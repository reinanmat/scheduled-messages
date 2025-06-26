from fastapi import FastAPI
from app.messages import router

app = FastAPI()
app.include_router(router)
