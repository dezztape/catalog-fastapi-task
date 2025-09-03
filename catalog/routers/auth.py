from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import auth, database, models, schemas, crud

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(crud.models.User).filter(crud.models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = crud.create_user(db, user.username, user.password)
    return {"id": new_user.id, "username": new_user.username}

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

