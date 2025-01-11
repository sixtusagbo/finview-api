from datetime import date
import pytest
from pydantic import ValidationError
from api.models.income_statement import IncomeStatement


def test_valid_income_statement():
    """Test IncomeStatement creation with valid data"""
    data = {
        "date": date(2023, 1, 1),
        "revenue": 1000000.0,
        "net_income": 100000.0,
        "gross_profit": 500000.0,
        "eps": 2.5,
        "operating_income": 150000.0,
    }
    statement = IncomeStatement(**data)
    assert statement.date == data["date"]
    assert statement.revenue == data["revenue"]
    assert statement.net_income == data["net_income"]
    assert statement.gross_profit == data["gross_profit"]
    assert statement.eps == data["eps"]
    assert statement.operating_income == data["operating_income"]


def test_invalid_income_statement():
    """Test rejection of invalid date and revenue types"""
    with pytest.raises(ValidationError):
        IncomeStatement(
            date="invalid-date",
            revenue="not-a-number",
            net_income=100000.0,
            gross_profit=500000.0,
            eps=2.5,
            operating_income=150000.0,
        )


def test_missing_fields():
    """Test required fields validation"""
    with pytest.raises(ValidationError):
        IncomeStatement(date=date(2023, 1, 1), revenue=1000000.0)
