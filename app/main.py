from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from app.schemas.products import Products
from uuid import uuid4,UUID
from datetime import datetime
from app.service.products import add_product,get_all_products,delete_products

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.post("/products",status_code=201)
def create_product(product: Products):
    product_dict=product.model_dump(mode="json")
    product_dict["id"]=str(uuid4())
    product_dict["created_at"]=datetime.utcnow().isoformat()+"Z"
    try:
        add_product(product_dict)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    return product.model_dump(mode="json")

@app.delete("/products/{products_id}")
def delete_product(products_id: UUID=Path(...,description="Product UUID")):
    try:
        res=delete_products(str(products_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


