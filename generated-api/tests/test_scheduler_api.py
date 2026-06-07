# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.error_response import ErrorResponse  # noqa: F401
from openapi_server.models.scheduler_run_response import SchedulerRunResponse  # noqa: F401
from openapi_server.models.scheduler_status import SchedulerStatus  # noqa: F401


def test_run_scheduler(client: TestClient):
    """Test case for run_scheduler

    Run scheduler manually
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/scheduler/run",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_scheduler_status(client: TestClient):
    """Test case for get_scheduler_status

    Get scheduler status
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/scheduler/status",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

