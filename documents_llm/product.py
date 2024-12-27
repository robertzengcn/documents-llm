from pydantic import BaseModel,Field
from typing import Optional,List

class Item(BaseModel):

    sku: str = Field("", description="The sku number of the item.")
    product_name: str = Field("", description="The product name/description of the item.")
    unit_price: float = Field("", description="The unit price of the item.")
    quantity: int = Field("", description="The quantity of the item purchased.")
    tax_rate: Optional[float] = Field(default=None, description="The tax rate applied to the purchase.")
    tax_type: Optional[str] = Field("", description="The type of tax applied (e.g., IGST).")
    tax_amount: Optional[float] = Field(default=None, description="The total tax amount for the purchase.")
    total_amount: Optional[float] = Field(default=None, description="The total amount including tax.")
    
class ProductJson(BaseModel): 
    """Item to return in the response."""
    items: List[Item] = Field(default_factory=list, description="The list of items.")   