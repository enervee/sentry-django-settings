from unittest import mock
import pytest
from django.conf import settings


def pytest_configure():
    # Configure an empty settings object to use for tests.
    settings.configure()
