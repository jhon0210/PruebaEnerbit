from fastapi import FastAPI

from . import models
from .database import engine
from .routers import customer, work_order


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(customer.router)
app.include_router(work_order.router)

