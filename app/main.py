from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from service.products import get_all_products

app=FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Products(BaseModel):
    id: str
    sku: Annotated[str, Field(min_length=1,max_length=20,title="SKU",description="Stock keeping unit",examples=["SKU12345","SKU67890"])]
    name: str

@app.post("/products",status_code=201)
def create_product(product: Products):
    return product

