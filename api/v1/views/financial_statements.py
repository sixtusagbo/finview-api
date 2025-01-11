from fastapi import APIRouter
from os import getenv
import requests

from api.models.income_statement import IncomeStatement

router = APIRouter(
    prefix="/statements",
    tags=["financial_statements"],
    responses={404: {"description": "Not found"}},
)


@router.get("/income")
def get_income_statement():
    """Return the income statement"""
    key = getenv("FMP_KEY")
    endpoint = f"https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={key}"
    response = requests.get(endpoint)
    data = response.json()
    result = []
    for item in data:
        result.append(
            IncomeStatement(
                date=item["date"],
                revenue=item["revenue"],
                net_income=item["netIncome"],
                gross_profit=item["grossProfit"],
                eps=item["eps"],
                operating_income=item["operatingIncome"],
            )
        )
    return result
