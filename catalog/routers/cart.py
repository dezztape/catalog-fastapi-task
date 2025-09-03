from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .. import models, crud, schemas, database

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.post("/", response_model=schemas.CartItem)
def add_item(
    item: schemas.CartItemCreate, 
    session_id: str = Query(..., description="Unique session ID"),
    db: Session = Depends(database.get_db)
):
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.add_to_cart(db, session_id, item)

@router.get("/", response_model=schemas.Cart)
def get_cart(
    session_id: str = Query(..., description="ID сессии пользователя"),
    db: Session = Depends(database.get_db)
):
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    total = sum(item.product.price * item.quantity for item in cart.items)

    return schemas.Cart(
        id=cart.id,
        session_id=cart.session_id,
        items=cart.items,
        total_price=total
    )

@router.put("/{item_id}", response_model=schemas.CartItem)
def update_cart_item(
    item_id: int,
    new_item: schemas.CartItemCreate,
    db: Session = Depends(database.get_db)
):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = new_item.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.delete("/{item_id}")
def delete_cart_item(item_id: int, db: Session = Depends(database.get_db)):
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Cart item deleted"}
