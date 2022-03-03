from unittest import mock
import pytest


@pytest.fixture
def mock_get_from_repo():
    with mock.patch("sentry_django_settings.apps.get_from_repo") as mocked_repo:
        yield mocked_repo


@pytest.fixture
def mock_get_from_file():
    with mock.patch("sentry_django_settings.apps.get_from_file") as mocked_file:
        yield mocked_file
