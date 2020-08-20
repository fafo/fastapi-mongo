from fastapi import FastAPI
from services.users import setup_users
from api import sandbox

app = FastAPI()
setup_users(app)

app.include_router(sandbox.router, prefix="/sandbox", tags=["sandbox"])
