# tests/test_api.py
import requests
import pytest
from jsonschema import validate, ValidationError
import responses

# 1) Simple schema for jsonplaceholder /posts/1
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "userId": {"type": "number"},
        "id": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"}
    },
    "required": ["userId", "id", "title", "body"]
}

def test_public_api_happy_path():
    """200 happy path and response schema validation"""
    url = "https://jsonplaceholder.typicode.com/posts/1"
    r = requests.get(url, timeout=10)
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    # Validate schema (will raise jsonschema.ValidationError if invalid)
    validate(instance=data, schema=POST_SCHEMA)
    # spot-check field types
    assert isinstance(data["id"], int)
    assert isinstance(data["userId"], int)
    assert isinstance(data["title"], str)

def test_error_responses():
    """Check 4xx and 5xx behavior from httpbin endpoints"""
    url_404 = "https://httpbin.org/status/404"
    r404 = requests.get(url_404, timeout=10)
    assert r404.status_code == 404

    # httpbin can return 500:
    url_500 = "https://httpbin.org/status/500"
    r500 = requests.get(url_500, timeout=10)
    assert r500.status_code == 500

    # Also ensure the client code handles it: example of raising (not done here)
    # For tests, ensure we can detect non-2xx responses
    assert r404.status_code // 100 in (4,)
    assert r500.status_code // 100 in (5,)

@responses.activate
def test_local_mock_schema_and_error():
    """Use responses to simulate a local service returning 500 and a JSON error schema."""
    mock_url = "http://localhost:5000/mock"
    # Add mocked 500 error with JSON body
    responses.add(
        responses.POST,
        mock_url,
        json={"error": "internal server error"},
        status=500
    )

    # Client call
    r = requests.post(mock_url, json={"any": "payload"})
    assert r.status_code == 500

    # Validate response schema for the error
    ERROR_SCHEMA = {
        "type": "object",
        "properties": {
            "error": {"type": "string"}
        },
        "required": ["error"]
    }
    data = r.json()
    validate(instance=data, schema=ERROR_SCHEMA)
    assert "server" in data["error"].lower()
