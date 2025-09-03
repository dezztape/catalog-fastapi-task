from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import products, cart, auth
from . import models, database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Catalog API", dependencies=[])

app.include_router(products.router)
app.include_router(cart.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="catalog/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)