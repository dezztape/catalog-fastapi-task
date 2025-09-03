from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def add_to_cart(db: Session, session_id: str, item: schemas.CartItemCreate):
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if not cart:
        cart = models.Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    db_item = models.CartItem(product_id=item.product_id, quantity=item.quantity, cart_id=cart.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_cart(db: Session, session_id: str):
    return db.query(models.Cart).filter(models.Cart.session_id == session_id).first()

def create_user(db: Session, username: str, password: str):
    hashed_password = auth.get_password_hash(password)
    db_user = models.User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user and auth.verify_password(password, user.hashed_password):
        return user
    return None