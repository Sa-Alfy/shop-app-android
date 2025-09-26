from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class StockItem(BaseModel):
    product_id: Optional[str] = Field(None, description="Unique product identifier")
    product_name: str
    date_added: datetime = Field(default_factory=datetime.now)
    purchase_price: float
    selling_price: float
    supplier: str
    quantity: int

class SaleRecord(BaseModel):
    product_id: str
    date_of_sale: datetime = Field(default_factory=datetime.now)
    quantity_sold: int
    total_price: float