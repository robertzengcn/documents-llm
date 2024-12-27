from pydantic import BaseModel,Field
from typing import Optional,List
from typing_extensions import Annotated, TypedDict

class Product(TypedDict):

    sku: Annotated[Optional[str], ..., "The sku number of the item."]
    product_name: Annotated[Optional[str] , ...,"The product name/description of the item."]
    unit_price: Annotated[Optional[float] , ...,"The unit price of the item."]
    quantity: Annotated[Optional[int], ..., "The quantity of the item purchased."]
    
    
class ProductListJson(TypedDict): 
    """Product information"""
    products: Annotated[Optional[List[Product]], ..., "The product in document"]    