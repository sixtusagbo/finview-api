from fastapi.testclient import TestClient
from api.v1.main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_cors_headers():
    """Test the CORS headers"""
    response = client.options(
        "/",
        headers={"Origin": "http://127.0.0.1", "Access-Control-Request-Method": "GET"},
    )
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1"
    assert response.headers["access-control-allow-credentials"] == "true"
