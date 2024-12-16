from fastapi.testclient import TestClient


def test_update_target_when_success(test_client: TestClient):
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
    test_client.post("/api/v1/missions", json=mission_data)

    target_data = {
        "notes": "Updated test note"
    }
    response = test_client.patch("/api/v1/targets/1", json=target_data)
    assert response.status_code == 200
    print(response.json())
    assert response.json() == {
        "id": 1,
        "name": "Just a test name of the target",
        "country": "Ukraine",
        "complete_state": False,
        "notes": "Updated test note",
        "mission_id": 1,
    }


def test_update_target_when_non_exists(test_client: TestClient):
    target_data = {
        "complete_state": False,
        "notes": "Updated test note"
    }
    response = test_client.patch("/api/v1/targets/2", json=target_data)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Target doesn't exist."
    }


def test_update_target_when_mission_is_completed(test_client: TestClient):
    mission_data = {
        "complete_state": True,
    }
    test_client.patch("/api/v1/missions/1", json=mission_data)

    target_data = {
        "notes": "Updated test note"
    }
    response = test_client.patch("/api/v1/targets/1", json=target_data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "You can't update it because of mission/target was completed."
    }


def test_update_target_when_target_is_completed(test_client: TestClient):
    test_client.patch(
        "/api/v1/missions/1",
        json={
            "complete_state": False,
        }
    )
    test_client.patch(
        "/api/v1/targets/1",
        json={
            "complete_state": True,
            "notes": "Updated test note"
        }
    )

    target_data = {
        "notes": "Updated test note"
    }
    response = test_client.patch("/api/v1/targets/1", json=target_data)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "You can't update it because of mission/target was completed."
    }
