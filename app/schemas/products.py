from pydantic import BaseModel, Field, AnyUrl, field_validator, model_validator, computed_field, EmailStr
from typing import List, Optional, Annotated, Literal
from uuid import UUID
from datetime import datetime


class Seller(BaseModel):
    id: UUID
    name:Annotated[str, Field(min_length=3, max_length=50, description="Seller name (3-50 chars)",examples=["BestSeller", "TopShop"])]
    email: EmailStr
    website: AnyUrl

class Dimensions(BaseModel):
    length: Annotated[float, Field(gt=0, description="Length in cm")]
    width: Annotated[float, Field(gt=0,description="width in cm")]
    height: Annotated[float, Field(gt=0,description="height in cm")]

field_validator("email",mode="after")
@classmethod
def validate_email(cls,value: EmailStr):
    allowed_domains=["gmail.com","yahoo.cm","outlook.com"]
    domain=str(value).split("@")[-1].lower()
    if domain not in allowed_domains:
        raise ValueError(f"Seller email does not allowed: {domain}")
    return value

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
    seller: Seller
    dimensions: Dimensions

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
    
    @computed_field
    @property
    def volume(self) -> float:
        return round(self.dimensions.length*self.dimensions.width*self.dimensions.height,2)
    
class SellerUpdate(BaseModel):
    id: Optional[UUID]
    name:Optional[Annotated[str, Field(min_length=3, max_length=50, description="Seller name (3-50 chars)",examples=["BestSeller", "TopShop"])]]
    email: Optional[EmailStr]
    website: Optional[AnyUrl]

class DimensionsUpdate(BaseModel):
    length: Optional[Annotated[float, Field(gt=0, description="Length in cm")]]
    width: Optional[Annotated[float, Field(gt=0,description="width in cm")]]
    height: Optional[Annotated[float, Field(gt=0,description="height in cm")]]

class ProductsUpdate(BaseModel):
    id: Optional[UUID]
    sku: Optional[Annotated[str, Field(min_length=1,max_length=20,title="SKU",description="Stock keeping unit",examples=["SKU12345","SKU67890"])]]
    name: Optional[Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Readable product name (3-80 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]]

    description: Optional[Annotated[
        str,
        Field(max_length=200, description="Short product description"),
    ]]

    category: Optional[Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="Category like mobiles/laptops/electronics/accessories",
            examples=["mobiles", "laptops"],
        ),
    ]]

    brand: Optional[Annotated[
        str,
        Field(min_length=2, max_length=40, examples=["Xiaomi", "Apple"]),
    ]]

    price: Optional[Annotated[float, Field(gt=0, strict=True, description="Base price (INR)")]]
    currency:Optional[Literal["INR"]] = "INR"

    discount_percent:Optional[Annotated[
        int,
        Field(ge=0, le=90, description="Discount in percent (0-90)"),
    ]] = 0

    stock: Optional[Annotated[int, Field(ge=0, description="Available stock (>=0)")]]
    is_active: Optional[Annotated[bool, Field(description="Is product active?")]]           

    rating:Optional[Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]]
    tags: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=10, description="Up to 10 tags"),
    ]
    image_urls: Optional[Annotated[
        List[AnyUrl],
        Field(max_length=1, description="At least 1 image url"),
    ]]
    seller: SellerUpdate
    dimensions: DimensionsUpdate

    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_formate(cls,value: str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")
        
        last=value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("SKU must end with 3 digits sequence like -234")
        return value