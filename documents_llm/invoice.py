from pydantic import BaseModel,Field
from typing import List


class Item(BaseModel):
    description: str = Field("", description="The description of the purchased item.")
    unit_price: str = Field("", description="The unit price of the item.")
    quantity: str = Field("", description="The quantity of the item purchased.")
    net_amount: str = Field("", description="The net amount for the purchased items.")
    tax_rate: str = Field("", description="The tax rate applied to the purchase.")
    tax_type: str = Field("", description="The type of tax applied (e.g., IGST).")
    tax_amount: str = Field("", description="The total tax amount for the purchase.")
    total_amount: str = Field("", description="The total amount including tax.")

class InvoiceJson(BaseModel):
    quote_number: str = Field("", description="The quote number associated with the purchase.")
    order_number: str = Field("", description="The order number associated with the purchase.")
    invoice_number: str = Field("", description="The unique invoice number.")
    order_date: str = Field("", description="The date the order was placed.")
    invoice_date: str = Field("", description="The date the invoice was generated.")
    items: List[Item] = Field(default_factory=list, description="The list of purchased items.")
    amount_in_words: str = Field("", description="The total amount in words.")
    sold_by: str = Field("", description="The seller information.")
    billing_address: str = Field("", description="The billing address of the buyer.")
    shipping_address: str = Field("", description="The shipping address of the buyer.")
    gst_registration_no: str = Field("", description="The GST registration number of the seller.")
    pan_no: str = Field("", description="The PAN number of the seller.")