from fastapi import APIRouter, Query
from os import getenv
import requests
from typing import Optional, Annotated
from datetime import datetime

from api.models.income_statement import IncomeStatement

router = APIRouter(
    prefix="/statements",
    tags=["financial_statements"],
    responses={404: {"description": "Not found"}},
)


@router.get("/income")
def get_income_statement(
    start_year: Annotated[
        Optional[int],
        Query(ge=1900, le=2100, description="Filter statements from this year"),
    ] = None,
    end_year: Annotated[
        Optional[int],
        Query(ge=1900, le=2100, description="Filter statements until this year"),
    ] = None,
    min_revenue: Annotated[
        Optional[float], Query(ge=0, description="Minimum revenue value")
    ] = None,
    max_revenue: Annotated[
        Optional[float], Query(ge=0, description="Maximum revenue value")
    ] = None,
    min_net_income: Annotated[
        Optional[float], Query(description="Minimum net income value")
    ] = None,
    max_net_income: Annotated[
        Optional[float], Query(description="Maximum net income value")
    ] = None,
):
    """Return the filtered income statement"""
    key = getenv("FMP_KEY")
    endpoint = f"https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={key}"
    response = requests.get(endpoint)
    data = response.json()
    result = []

    for item in data:
        # Convert date string to year
        year = datetime.strptime(item["date"], "%Y-%m-%d").year

        # Apply date range filter
        if start_year and year < start_year:
            continue
        if end_year and year > end_year:
            continue

        # Apply revenue filter
        if min_revenue and item["revenue"] < min_revenue:
            continue
        if max_revenue and item["revenue"] > max_revenue:
            continue

        # Apply net income filter
        if min_net_income and item["netIncome"] < min_net_income:
            continue
        if max_net_income and item["netIncome"] > max_net_income:
            continue

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
