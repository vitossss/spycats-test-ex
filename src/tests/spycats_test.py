from fastapi.testclient import TestClient


def test_create_new_spycat_when_success(test_client: TestClient):
    spycat_data = {
        "name": "Markiza",
        "years_of_exp": 2,
        "breed": "American Curl",
        "salary": 600.0
    }
    response = test_client.post(
        "/api/v1/spycats",
        json=spycat_data
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        **spycat_data
    }


def test_create_new_spycat_when_breed_failed(test_client: TestClient):
    spycat_data = {
        "name": "Markiza",
        "years_of_exp": 2,
        "breed": "Non existing breed",
        "salary": 600.0
    }
    response = test_client.post(
        "/api/v1/spycats",
        json=spycat_data
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Spycat with this breed doesn't exist."
    }


def test_get_spycat_when_exists(test_client: TestClient):
    response = test_client.get("/api/v1/spycats/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Markiza",
        "years_of_exp": 2,
        "breed": "American Curl",
        "salary": 600.0
    }


def test_get_spycat_when_non_exists(test_client: TestClient):
    response = test_client.get("/api/v1/spycats/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Spycat doesn't exist."
    }


def test_update_spycat_when_success(test_client: TestClient):
    spycat_data = {
        "salary": 255.0
    }
    response = test_client.patch(
        "/api/v1/spycats/1",
        json=spycat_data
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Markiza",
        "years_of_exp": 2,
        "breed": "American Curl",
        "salary": 255.0
    }


def test_update_spycat_when_non_exists(test_client: TestClient):
    spycat_data = {
        "salary": 255.0
    }
    response = test_client.patch(
        "/api/v1/spycats/2",
        json=spycat_data
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Spycat doesn't exist."
    }


def test_get_list_of_spycats_when_success(test_client: TestClient):
    response = test_client.get("/api/v1/spycats")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Markiza",
            "years_of_exp": 2,
            "breed": "American Curl",
            "salary": 255.0
        }
    ]


def test_delete_spycat_when_success(test_client: TestClient):
    response = test_client.delete("/api/v1/spycats/1")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Spycat successfully deleted."
    }


def test_delete_spycat_when_non_exists(test_client: TestClient):
    response = test_client.delete("/api/v1/spycats/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Spycat doesn't exist."
    }


def test_get_list_of_spycats_when_non_exist(test_client: TestClient):
    response = test_client.get("/api/v1/spycats")
    assert response.status_code == 200
    assert response.json() == []
