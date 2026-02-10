from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field
from typing import List, Optional, Annotated, Literal
from uuid import UUID
from datetime import datetime




class Products(BaseModel):
    id: UUID
    sku: Annotated[str, Field(min_length=1,max_length=20,title="SKU",description="Stock keeping unit",examples=["SKU12345","SKU67890"])]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Readable product name (3-80 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]

    description: Annotated[
        str,
        Field(max_length=200, description="Short product description"),
    ]

    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobiles/laptops/electronics/accessories",
            examples=["mobiles", "laptops"],
        ),
    ]

    brand: Annotated[
        str,
        Field(min_length=2, max_length=40, examples=["Xiaomi", "Apple"]),
    ]

    price: Annotated[float, Field(gt=0, strict=True, description="Base price (INR)")]
    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[
        int,
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ] = 0

    stock: Annotated[int, Field(ge=0, description="Available stock (>=0)")]
    is_active: Annotated[bool, Field(description="Is product active?")]

    rating: Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]
    tags: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=10, description="Up to 10 tags"),
    ]
    image_urls: Annotated[
        List[AnyUrl],
        Field(max_length=1, description="At least 1 image url"),
    ]

    #dimension

    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_formate(cls,value: str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")
        
        last=value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("SKU must end with 3 digits sequence like -234")
        return value
    
    @model_validator(mode="after")
    @classmethod
    def validate_buisness_rule(cls, model:"Products"):
        if model.stock==0 and model.is_active is True:
            raise ValueError("If stock is 0, is activate must be false")

        if model.discount_percent >0 and model.rating==0:
            raise ValueError("Discount product must have a rating (rating!=0)")
        return model 
    
    @computed_field
    @property # used to create new field which is not provided by user but calculated based on other fields
    def final_price(self) -> float:
        return round(self.price * (1-self.discount_percent/100),2)