from fastapi import FastAPI
from app.routers.notes import router
from app.db import connect_to_db


# برای مدیریت چرخش کار API
def lifespan(app: FastAPI):
    connect_to_db()  # راه اندازی دیتابیس
    yield
    pass


app = FastAPI(
    name= "Note Taking API",
    description= "This is a simple RESTful API service to take notes",
    lifespan=lifespan
)


# add endpoints
app.include_router(router)


@app.get("/")
def root():
    return {"Message: API is running 🌪️"}
