"""
Data Models and Application Constants
Defines core product definitions and category helpers.
"""

from typing import Dict, List

# Four required Home Appliances
APPLIANCES: List[Dict[str, str]] = [
    {"id": 1, "name_en": "Refrigerator", "name_ur": "ریفریجریٹر", "category": "Cooling"},
    {"id": 2, "name_en": "Air Cooler", "name_ur": "ایئر کولر", "category": "Cooling"},
    {"id": 3, "name_en": "Air Conditioner (AC)", "name_ur": "ایئر کنڈیشنر (اے سی)", "category": "Cooling"},
    {"id": 4, "name_en": "Washing Machine", "name_ur": "واشنگ مشین", "category": "Laundry"}
]

# Shop Expense Categories
EXPENSE_CATEGORIES = {
    "rent": {"en": "Monthly Shop Rent", "ur": "دکان کا ماہانہ کرایہ", "is_monthly": True},
    "salary": {"en": "Employee Salary", "ur": "ملازمین کی تنخواہ", "is_monthly": True},
    "electricity": {"en": "Electricity Bill", "ur": "بجلی کا بل", "is_monthly": False},
    "other": {"en": "Other Expenses", "ur": "دیگر متفرق اخراجات", "is_monthly": False}
}
