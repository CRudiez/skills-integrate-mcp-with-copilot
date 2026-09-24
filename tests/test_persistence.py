import json

from fastapi.testclient import TestClient

import src.app as app_module


def test_activity_signup_persists_to_disk(tmp_path, monkeypatch):
    data_file = tmp_path / "activities.json"
    initial_data = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 2,
            "participants": ["alice@example.com"],
        }
    }
    data_file.write_text(json.dumps(initial_data), encoding="utf-8")

    monkeypatch.setattr(app_module, "DATA_FILE", data_file)
    app_module.activities = app_module.load_activities()

    client = TestClient(app_module.app)
    response = client.post("/activities/Chess Club/signup?email=bob@example.com")

    assert response.status_code == 200
    assert "bob@example.com" in app_module.load_activities()["Chess Club"]["participants"]
    saved = json.loads(data_file.read_text(encoding="utf-8"))
    assert "bob@example.com" in saved["Chess Club"]["participants"]
