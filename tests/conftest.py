"""Pytest configuration and fixtures for activity management API tests."""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def activities_snapshot():
    """Snapshot and restore activities state between tests for isolation."""
    snapshot = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
