from fastapi import APIRouter, Query, HTTPException
from os import getenv
import requests
from typing import Optional, Annotated, Literal
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
    sort_by: Optional[Literal["date", "revenue", "net_income"]] = "date",
    order: Annotated[
        Optional[Literal["asc", "desc"]], Query(description="Sort order (asc or desc)")
    ] = "desc",
):
    """Return the filtered and sorted income statement"""
    key = getenv("FMP_KEY")
    endpoint = f"https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&apikey={key}"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status() # Raise exception for bad status codes
        data = response.json()
        
        if not isinstance(data, list):
            raise HTTPException(status_code=500, detail="Unexpected API response format")
            
        result = []

        for item in data:
            if not isinstance(item, dict):
                continue
                
            try:
                date = item.get("date")
                if not date:
                    continue
                    
                # Apply date range filter
                year = datetime.strptime(date, "%Y-%m-%d").year
                if start_year and year < start_year:
                    continue
                if end_year and year > end_year:
                    continue

                # Apply revenue filter
                revenue = item.get("revenue")
                if revenue is None or (min_revenue and revenue < min_revenue) or (max_revenue and revenue > max_revenue):
                    continue

                # Apply net income filter
                net_income = item.get("netIncome")
                if net_income is None or (min_net_income and net_income < min_net_income) or (max_net_income and net_income > max_net_income):
                    continue

                result.append(
                    IncomeStatement(
                        date=date,
                        revenue=revenue,
                        net_income=net_income,
                        gross_profit=item.get("grossProfit", 0),
                        eps=item.get("eps", 0),
                        operating_income=item.get("operatingIncome", 0),
                    )
                )
            except (ValueError, KeyError) as e:
                print(f"Error processing item: {e}")
                continue

        # Apply sorting
        if sort_by:
            reverse = order == "desc"
            if sort_by == "date":
                result.sort(key=lambda x: x.date, reverse=reverse)
            elif sort_by == "revenue":
                result.sort(key=lambda x: x.revenue, reverse=reverse)
            elif sort_by == "net_income":
                result.sort(key=lambda x: x.net_income, reverse=reverse)

        return result
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from FMP API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
