from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from app.service.products import get_all_products
from app.schemas.products import Products

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.post("/products",status_code=201)
def create_product(product: Products):
    return product.model_dump(mode="json")

