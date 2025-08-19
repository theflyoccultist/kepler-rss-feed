import pytest
from src.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    # template is rendered
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data


def test_fetch_invalid_url(client):
    response = client.post("/fetch", data={"url": "not-a-url"})
    # expect either 400 or some error message
    assert response.status_code in (400, 500)
    assert b"error" in response.data.lower()


def test_fetch_empty_feed(client):
    # simulate giving it an empty feed
    response = client.post("/fetch", data={"url": "data://, "})
    assert response.status_code in (400, 500)
    assert b"error" in response.data.lower()


def test_fetch_broken_xml(client):
    # feedfetchr should throw an error or return empty
    broken_xml = "<rss><channel><title>Oops</title>"  # never closed properly
    response = client.post("/fetch", data={"url": "data://," + broken_xml})
    assert response.status_code in (400, 500)
    assert b"error" in response.data.lower()
