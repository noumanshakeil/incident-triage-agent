import pytest
@pytest.mark.asyncio
async def test_triage(client):
    r = await client.post("/api/incidents", json={"title": "Checkout 5xx spike", "symptoms": "error rate 12%", "service": "checkout"})
    assert r.status_code == 200
    assert r.json()["severity"].startswith("sev")
