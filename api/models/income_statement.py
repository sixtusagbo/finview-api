from datetime import date
from pydantic import BaseModel


class IncomeStatement(BaseModel):
    date: date
    revenue: float
    net_income: float
    gross_profit: float
    eps: float
    operating_income: float
