from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    name: str
    price: float
    image: str
    category: str
    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[ProductOut]
   

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    product: Product
    class Config:
        from_attributes = True

class Cart(BaseModel):
    id: int
    session_id: str
    items: List[CartItem] = []
    total_price: float
    class Config:
        from_attributes = True
 
class User(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    disabled: bool | None = None
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

