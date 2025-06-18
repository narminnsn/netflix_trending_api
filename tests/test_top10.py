def test_top10_success(client):
    response = client.get("/v1/top10?locale=en&window=WEEKLY")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Test Movie"
    assert data[1]["type"] == "season"

def test_top10_invalid_locale(client):
    response = client.get("/v1/top10?locale=zz")
    assert response.status_code == 404

def test_top10_as_of_filter(client):
    response = client.get("/v1/top10?locale=en&as_of=2025-06-02")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_top10_include_movie_only(client):
    response = client.get("/v1/top10?locale=en&include=movie")
    assert response.status_code == 200
    data = response.json()
    assert all(item["type"] == "movie" for item in data)

def test_top10_include_season_only(client):
    response = client.get("/v1/top10?locale=en&include=season")
    assert response.status_code == 200
    data = response.json()
    assert all(item["type"] == "season" for item in data)