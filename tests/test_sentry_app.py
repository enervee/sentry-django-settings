import logging
from unittest import mock

from django.apps import AppConfig


class TestSentryApp:
    def test_ready_initializes_sentry(self, settings):
        """
        If the SENTRY setting is available and "enabled" is set to True, the App
        will initialize Sentry when ready() is called.
        """
        settings.SENTRY = {
            "enabled": True,
            "dsn": "Striestn1e33",
            "environment": "test_env",
            "integrations": [],
            "release": "current_release",
            "traces_sample_rate": 0.5,
        }
        app = AppConfig.create("sentry_django_settings.apps.Sentry")
        with mock.patch("sentry_django_settings.apps.sentry_sdk") as mocked_sentry:
            app.ready()
            mocked_sentry.init.assert_called_once_with(
                dsn="Striestn1e33",
                environment="test_env",
                integrations=[],
                release="current_release",
                traces_sample_rate=0.5,
            )

    def test_ready_skips_initialization_if_setting_missing(self, caplog):
        """
        If the SENTRY setting missing entirely, Sentry will not be initialized and a
        warning message will be logged.
        """
        app = AppConfig.create("sentry_django_settings.apps.Sentry")
        with mock.patch("sentry_django_settings.apps.sentry_sdk") as mocked_sentry:
            app.ready()
            mocked_sentry.init.assert_not_called()
            assert caplog.record_tuples == [
                (
                    "django.sentry_django_settings",
                    logging.WARNING,
                    "No SENTRY settings found.",
                )
            ]

    def test_ready_skips_initialization_if_not_enabled(self, caplog, settings):
        """
        If the SENTRY["enabled"] key is set to False, Sentry will not be initialized and
        a log message will be sent.
        """
        settings.SENTRY = {
            "enabled": False,
        }
        app = AppConfig.create("sentry_django_settings.apps.Sentry")
        with mock.patch("sentry_django_settings.apps.sentry_sdk") as mocked_sentry:
            app.ready()
            mocked_sentry.init.assert_not_called()
            assert caplog.record_tuples == [
                (
                    "django.sentry_django_settings",
                    logging.INFO,
                    "Sentry disabled.",
                )
            ]
