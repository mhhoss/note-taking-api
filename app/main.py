from fastapi import FastAPI
from app.routers.notes import router
from app.db import init_db, logger


# برای مدیریت چرخش کار API
def lifespan(app: FastAPI):
    init_db()  # راه اندازی دیتابیس
    logger.info("API startup... 📡")
    yield
    logger.info("API shutdown... 👾")


app = FastAPI(
    title= "Note Taking API",
    description= "This is a simple RESTful API service to take notes",
    lifespan=lifespan
)


# add endpoints
app.include_router(router)


@app.get("/")
def root():
    return {"Message: API is running... 🌪️"}
