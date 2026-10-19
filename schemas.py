"""
Pydantic Schemas for Input Validation and API Serialization
"""

from datetime import date
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class PurchaseCreate(BaseModel):
    product_id: int = Field(..., description="Selected appliance product ID")
    purchase_date: date = Field(..., description="Date goods arrived")
    quantity: int = Field(..., gt=0, description="Quantity received, must be greater than 0")
    unit_price: float = Field(..., ge=0, description="Purchase price per unit in PKR")
    transport_cost: float = Field(default=0.0, ge=0, description="Additional transport or delivery expense")
    notes: Optional[str] = Field(default="", description="Optional purchase remarks or invoice details")


class SaleCreate(BaseModel):
    product_id: int = Field(..., description="Selected appliance product ID")
    sale_date: date = Field(..., description="Date of sale")
    quantity: int = Field(..., gt=0, description="Quantity sold, must be greater than 0")
    unit_price: float = Field(..., ge=0, description="Selling price per unit in PKR")
    notes: Optional[str] = Field(default="", description="Optional sale remarks or customer details")


class ExpenseCreate(BaseModel):
    category: str = Field(..., description="Category: rent, salary, electricity, other")
    amount: float = Field(..., gt=0, description="Expense amount in PKR")
    expense_date: date = Field(..., description="Date expense occurred")
    for_month: Optional[str] = Field(default=None, description="Month in YYYY-MM format for rent/salary")
    description: Optional[str] = Field(default="", description="Optional expense description")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        valid = {"rent", "salary", "electricity", "other"}
        cleaned = v.strip().lower()
        if cleaned not in valid:
            raise ValueError(f"Invalid category '{v}'. Must be one of: {', '.join(valid)}")
        return cleaned


class ProductItem(BaseModel):
    id: int
    name_en: str
    name_ur: str
    category: str


class StockSummaryItem(BaseModel):
    product_id: int
    name_en: str
    name_ur: str
    total_purchased: int
    total_sold: int
    remaining_stock: int
    avg_unit_cost: float
    total_stock_value: float
    last_selling_price: float
    estimated_unit_profit: float


class DashboardMetrics(BaseModel):
    total_stock_units: int
    goods_received_today_units: int
    goods_sold_today_units: int
    today_sales_amount: float
    today_purchase_cost: float
    remaining_stock_value: float
    today_expenses: float
    this_month_expenses: float
    gross_profit_all_time: float
    net_profit_all_time: float
    product_stock: List[StockSummaryItem]
