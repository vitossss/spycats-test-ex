from fastapi.testclient import TestClient


def test_create_mission_when_success(test_client: TestClient):
    mission_data = {
        "complete_state": False,
        "spycat_id": None,
        "targets": [
            {
                "name": "Just a test name of the target",
                "country": "Ukraine",
                "complete_state": False,
                "notes": "Just simple test note"
            }
        ]
    }
    response = test_client.post(
        "/api/v1/missions",
        json=mission_data
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        **mission_data
    }


def test_create_mission_when_targets_non_exist(test_client: TestClient):
    mission_data = {
        "complete_state": False,
        "spycat_id": None,
        "targets": []
    }
    response = test_client.post(
        "/api/v1/missions",
        json=mission_data
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Amount of mission targets must be from 1 to 3."
    }


def test_create_mission_when_targets_more_than_3(test_client: TestClient):
    mission_data = {
        "complete_state": False,
        "spycat_id": None,
        "targets": [
            {
                "name": "Target 1",
                "country": "Ukraine",
                "complete_state": False,
                "notes": "Note 1"
            },
            {
                "name": "Target 2",
                "country": "Greece",
                "complete_state": False,
                "notes": "Note 2"
            },
            {
                "name": "Target 3",
                "country": "UK",
                "complete_state": False,
                "notes": "Note 3"
            },
            {
                "name": "Target 4",
                "country": "Serbia",
                "complete_state": False,
                "notes": "Note 4"
            }
        ]
    }
    response = test_client.post(
        "/api/v1/missions",
        json=mission_data
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Amount of mission targets must be from 1 to 3."
    }


def test_get_mission_when_success(test_client: TestClient):
    response = test_client.get("/api/v1/missions/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "complete_state": False,
        "spycat_id": None,
        "targets": [
            {
                "name": "Just a test name of the target",
                "country": "Ukraine",
                "complete_state": False,
                "notes": "Just simple test note"
            }
        ]
    }


def test_get_mission_when_non_exists(test_client: TestClient):
    response = test_client.get("/api/v1/missions/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Mission doesn't exist."
    }


def test_update_mission_when_success(test_client: TestClient):
    spycat_data = {
        "name": "Markiza",
        "years_of_exp": 2,
        "breed": "American Curl",
        "salary": 600.0
    }
    test_client.post("/api/v1/spycats", json=spycat_data)

    mission_data = {
        "complete_state": True,
        "spycat_id": 1,
    }
    response = test_client.patch("/api/v1/missions/1", json=mission_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "complete_state": True,
        "spycat_id": 1
    }


def test_update_mission_when_non_exists(test_client: TestClient):
    mission_data = {
        "complete_state": True,
        "spycat_id": 1,
    }
    response = test_client.patch("/api/v1/missions/2", json=mission_data)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Mission doesn't exist."
    }


def test_get_list_of_missions_when_success(test_client: TestClient):
    response = test_client.get("/api/v1/missions")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "complete_state": True,
            "spycat_id": 1,
            "targets": [
                {
                    "name": "Just a test name of the target",
                    "country": "Ukraine",
                    "complete_state": False,
                    "notes": "Just simple test note"
                }
            ]
        }
    ]


def test_delete_mission_when_spycat_is_assigned(test_client: TestClient):
    response = test_client.delete("/api/v1/missions/1")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "You can't delete missions with assigned spycat to it."
    }


def test_delete_mission_when_success(test_client: TestClient):
    mission_data = {
        "complete_state": True,
        "spycat_id": None,
    }
    test_client.patch("/api/v1/missions/1", json=mission_data)

    response = test_client.delete("/api/v1/missions/1")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "Mission successfully deleted."
    }


def test_delete_mission_when_non_exists(test_client: TestClient):
    response = test_client.delete("/api/v1/missions/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Mission doesn't exist."
    }


def test_get_list_of_missions_when_not_exist(test_client: TestClient):
    response = test_client.get("/api/v1/missions")
    assert response.status_code == 200
    assert response.json() == []
