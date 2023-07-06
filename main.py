from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from routes.auth_routes import auth_router
from routes.contact_routes import contacts_router
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(contacts_router)


@app.get("/", tags=["HELLO"])
async def hello():

    """
        ## Hello endpoint
        Simple endpoint to say hello :)
    """

    return jsonable_encoder({
        "author": "Karol Kowalik",
        "message": "Hello, it is my contacts book API written in FastAPI. Go to localhost:8000/docs for more informations "
    })
