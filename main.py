from fastapi import FastAPI
from routes.auth_routes import auth_router
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


