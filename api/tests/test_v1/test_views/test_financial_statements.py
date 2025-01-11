from fastapi.testclient import TestClient
from api.v1.main import app
from unittest.mock import patch

client = TestClient(app)

MOCK_INCOME_STATEMENTS = [
    {
        "date": "2022-12-31",
        "revenue": 1000000,
        "netIncome": 100000,
        "grossProfit": 400000,
        "eps": 2.5,
        "operatingIncome": 300000,
    },
    {
        "date": "2021-12-31",
        "revenue": 800000,
        "netIncome": 80000,
        "grossProfit": 350000,
        "eps": 2.0,
        "operatingIncome": 250000,
    },
    {
        "date": "2020-12-31",
        "revenue": 600000,
        "netIncome": 60000,
        "grossProfit": 300000,
        "eps": 1.5,
        "operatingIncome": 200000,
    },
]


def test_get_income_statement():
    """Test the get_income_statement endpoint"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENTS
        mock_get.return_value.status_code = 200

        response = client.get("/statements/income")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
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


def test_filter_by_year():
    """Test filtering income statements by year range"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENTS
        mock_get.return_value.status_code = 200

        response = client.get("/statements/income?start_year=2021&end_year=2022")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(2021 <= int(item["date"][:4]) <= 2022 for item in data)


def test_filter_by_revenue():
    """Test filtering income statements by revenue range"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENTS
        mock_get.return_value.status_code = 200

        response = client.get(
            "/statements/income?min_revenue=700000&max_revenue=900000"
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["revenue"] == 800000


def test_filter_by_net_income():
    """Test filtering income statements by net income range"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENTS
        mock_get.return_value.status_code = 200

        response = client.get("/statements/income?min_net_income=90000")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["net_income"] == 100000


def test_multiple_filters():
    """Test applying multiple filters simultaneously"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENTS
        mock_get.return_value.status_code = 200

        response = client.get(
            "/statements/income?start_year=2021&min_revenue=900000&max_net_income=150000"
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["date"] == "2022-12-31"


def test_no_results_with_filters():
    """Test when filters exclude all results"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = MOCK_INCOME_STATEMENTS
        mock_get.return_value.status_code = 200

        response = client.get("/statements/income?min_revenue=2000000")

        assert response.status_code == 200
        assert response.json() == []
