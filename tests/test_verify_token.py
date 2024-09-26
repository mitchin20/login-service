from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.lib.auth import create_access_token

client = TestClient(app)

# Mock the login to return valid token
@patch("app.services.user_service.login_user")
def test_token_renewal(mock_login):
    token_data = {
        "sub": "example@gmail.com"
    }
    
    token = create_access_token(token_data)

    mock_login.return_value = {
        "access_token": token,
        "token_type": "Bearer"
    }
    
    response = client.post("/verify-token", json={"token": token})

    assert response.status_code == 200
    json = response.json()
    assert "token" in json
    assert "extended" in json
    assert json["extended"] == False