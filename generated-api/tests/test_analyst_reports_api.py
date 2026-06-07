# coding: utf-8

from fastapi.testclient import TestClient


from datetime import date  # noqa: F401
from pydantic import Field, StrictBytes, StrictStr  # noqa: F401
from typing import List, Tuple, Union  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.analyst_report import AnalystReport  # noqa: F401
from openapi_server.models.analyst_report_upload_response import AnalystReportUploadResponse  # noqa: F401
from openapi_server.models.company_sentiment import CompanySentiment  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401


def test_upload_analyst_report(client: TestClient):
    """Test case for upload_analyst_report

    Upload analyst report
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    data = {
        "file": '/path/to/file',
        "company": 'company_example',
        "broker": 'broker_example',
        "var_date": '2013-10-20'
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/analyst-reports",
    #    headers=headers,
    #    data=data,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_analyst_reports(client: TestClient):
    """Test case for get_analyst_reports

    Get analyst reports
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/companies/{symbol}/analyst-reports".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_company_sentiment(client: TestClient):
    """Test case for get_company_sentiment

    Get company sentiment
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/companies/{symbol}/sentiment".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

