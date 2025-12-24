from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AI Quiz Backend")

app.include_router(router)
