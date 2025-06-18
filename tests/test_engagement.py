def test_engagement_movie(client):
    response = client.get("/v1/title/1/engagement")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "movie"
    assert len(data["timeline"]) == 1
    assert data["timeline"][0]["hours_viewed"] == 50000000

def test_engagement_season(client):
    response = client.get("/v1/title/2/engagement")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "season"
    assert data["title"] == "Test Show •S1"
    assert data["timeline"][0]["view_rank"] == 2

def test_engagement_date_filter(client):
    response = client.get("/v1/title/1/engagement?from=2025-06-02&to=2025-06-02")
    assert response.status_code == 200
    assert len(response.json()["timeline"]) == 1

def test_engagement_not_found(client):
    response = client.get("/v1/title/999/engagement")
    assert response.status_code == 404
