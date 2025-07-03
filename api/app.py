from fastapi import FastAPI
from api.messages import router

app = FastAPI()
app.include_router(router)
