"""Tests for the Mergington High School activity API using the AAA pattern."""

def test_get_activities(client, activities_snapshot):
    # Arrange: client fixture provided

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400


def test_signup_nonexistent_activity_returns_404(client, activities_snapshot):
    # Arrange
    activity = "No Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": "a@b.com"})

    # Assert
    assert response.status_code == 404


def test_unregister_removes_participant(client, activities_snapshot):
    # Arrange
    activity = "Chess Club"
    email = "tempstudent@mergington.edu"

    # Ensure signed up first
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup.status_code == 200

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
