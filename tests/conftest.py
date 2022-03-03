from unittest import mock
import pytest
from django.conf import settings


def pytest_configure():
    # Configure an empty settings object to use for tests.
    settings.configure()


@pytest.fixture
def mock_get_from_repo():
    with mock.patch("sentry_django_settings.apps.get_from_repo") as mocked_repo:
        yield mocked_repo


@pytest.fixture
def mock_get_from_file():
    with mock.patch("sentry_django_settings.apps.get_from_file") as mocked_file:
        yield mocked_file
