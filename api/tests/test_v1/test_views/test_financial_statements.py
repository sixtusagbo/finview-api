from fastapi.testclient import TestClient
from api.v1.main import app
from unittest.mock import patch

client = TestClient(app)

MOCK_INCOME_STATEMENT = [
    {
        "date": "2022-12-31",
        "revenue": 1000000,
        "netIncome": 100000,
        "grossProfit": 400000,
        "eps": 2.5,
        "operatingIncome": 300000,
    }
]


def test_get_income_statement():
    """Test the get_income_statement endpoint"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENT
        mock_get.return_value.status_code = 200

        response = client.get("/statements/income")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["date"] == "2022-12-31"
        assert data[0]["revenue"] == 1000000
        assert data[0]["net_income"] == 100000
        assert data[0]["gross_profit"] == 400000
        assert data[0]["eps"] == 2.5
        assert data[0]["operating_income"] == 300000


def test_not_found_error():
    """Test the 404 response for an invalid URL"""
    response = client.get("/foo/incomes/bar")
    assert response.status_code == 404
