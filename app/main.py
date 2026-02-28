from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Query, Path, Depends, Request
from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from app.schemas.products import Products,ProductsUpdate
from uuid import uuid4,UUID
from datetime import datetime
from app.service.products import add_product, change_product,get_all_products,delete_products,load_products
from typing import List,Dict

load_dotenv()
app=FastAPI()

@app.middleware("http")
async def lifecycle(request: Request, call_next):
    print("Before request")
    response=await call_next(request)
    #response["lifecycle"] = "was inside"
    print("After request")
    return response

def depends_logic():# this is dependency func 
    print("Executing Dependency")
    return "Dependency Logic Executed"

@app.get("/",response_model=dict)
def read_root(dependency_result=Depends(depends_logic)):# dependency is used in route para. not in the route, injestion of dependency takes place here
    DB_PATH=os.getenv("BASE_URL")
    return {"Hello": "World","dependency":dependency_result,"db_path":DB_PATH}




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

@app.delete("/products/{products_id}",response_model=dict)
def delete_product(products_id: UUID=Path(...,description="Product UUID")):
    try:
        res=delete_products(str(products_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))
    
@app.put("/products/{product_id}")
def update_product(
    product_id: UUID=Path(...,description="Product UUID"),
    payload: ProductsUpdate=...,):
    try:
        update_product=change_product(
            str(product_id),payload.model_dump(mode="json",exclude_unset=True)
        )
        return update_product
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))


