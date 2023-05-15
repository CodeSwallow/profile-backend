import os
import json

import boto3
import pytest

from moto import mock_dynamodb

from projects import get_projects
from .mock_dynamodb import create_mock_ddb_table


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""

    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ['PROFILE_TABLE'] = 'PROFILE_TABLE'


def test_initialization(aws_credentials):
    event = {}
    context = None

    os.environ['PROFILE_TABLE'] = ''

    payload = get_projects.get_projects_handler(event, context)

    assert payload['statusCode'] == 500


@mock_dynamodb
def test_valid_request(aws_credentials):
    event = {}
    context = None

    create_mock_ddb_table()

    payload = get_projects.get_projects_handler(event, context)
    content = json.loads(payload['body'])[0]

    assert payload['statusCode'] == 200
    assert content['name'] == 'Django Blog'
