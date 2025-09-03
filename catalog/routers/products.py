from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, File
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from .. import models, crud, schemas, database
import shutil
import os

UPLOAD_DIR = "catalog/static/images"

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=schemas.ProductListResponse)
def list_products(
    request: Request,
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    sort_by: str = Query("id", patter="^(id|name|price)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
):
    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    if search:
        search_pattern = f"%{search.lower()}%"
        query = query.filter(
            (models.Product.name.ilike(search_pattern)) |
            (models.Product.description.ilike(search_pattern))
        )

    sort_column = getattr(models.Product, sort_by)
    query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))

    count = query.count()
    products = query.offset(skip).limit(limit).all()

    base_url = str(request.base_url) + "/api/products/"
    next_url = f"{base_url}?skip={skip + limit}&limit={limit}" if skip + limit < count else None
    prev_url = f"{base_url}?skip={max(0, skip - limit)}&limit={limit}" if skip > 0 else None

    return {
        "count": count,
        "next": next_url,
        "previous": prev_url,
        "results": products
    }

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.get_product(db, product_id)

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    return crud.create_product(db, product)

@router.post("/{product_id}/upload-image")
def upload_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    db_product = crud.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_product.image = f"/static/images/{file.filename}"
    db.commit()
    db.refresh(db_product)

    return {"message": "Image uploaded successfully", "image_url": db_product.image}