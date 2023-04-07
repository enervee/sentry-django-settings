import logging
from unittest import mock
import warnings

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_django_settings.apps import SentryDjangoConfig


class TestSentryDjangoConfig:
    def test_enabled_is_based_on_configuration(self):
        """
        The enabled method will return True if the configuration is considered enabled.
        """
        assert SentryDjangoConfig({"enabled": True}).enabled()

        assert not SentryDjangoConfig({"enabled": False}).enabled()
        assert not SentryDjangoConfig({}).enabled()

    def test_sentry_config_returns_a_dict_suitable_for_sentry(self):
        """
        The sentry_config method returns a dictionary that is compatible for use with
        the sentry_sdk.init method, removing any extra keys it uses for configuration and
        updating any dynamic values.
        """
        config = SentryDjangoConfig(
            {
                "enabled": True,
                "dsn": "Striestn1e33",
                "environment": "test_env",
                "integrations": [],
                "release": "current_release",
                "traces_sample_rate": 0.5,
            }
        )
        assert config.sentry_config() == {
            "dsn": "Striestn1e33",
            "environment": "test_env",
            "integrations": [],
            "release": "current_release",
            "traces_sample_rate": 0.5,
        }

    def test_sentry_config_adds_default_integration(self):
        """
        If the integration option is not specified, it will default to a list containing
        only the DjangoIntegration class.
        """
        sentry_config = SentryDjangoConfig({}).sentry_config()

        assert len(sentry_config["integrations"]) == 1
        assert isinstance(sentry_config["integrations"][0], DjangoIntegration)

    def test_sentry_config_warns_about_use_of_git_sha_path(self):
        """
        If the git_sha_path option is specified, the library will warn that the
        option is no longer supported and doesn't affect functionality.
        """
        with warnings.catch_warnings(record=True) as w:
            sentry_config = SentryDjangoConfig(
                {"git_sha_path": "project_sha_file.txt"}
            ).sentry_config()

            assert sentry_config.get("release") == None
            assert len(w) == 1
            assert issubclass(w[0].category, FutureWarning)
            assert str(w[0].message) == (
                "`git_sha_path` is no longer supported and has no effect. See "
                "https://docs.sentry.io/platforms/python/configuration/options/#release"
                " on how to set the release directly."
            )

    def test_sentry_config_removes_options_specific_to_library(self):
        """
        The result from sentry_config removes any options from the passed in
        configuration that are only relevant to this library.
        """
        sentry_config = SentryDjangoConfig(
            {
                "enabled": False,
                "git_sha_path": "project_sha_file.txt",
                "release": "current_release",
            }
        ).sentry_config()

        assert "enabled" not in sentry_config
        assert "git_sha_path" not in sentry_config
        assert "release" in sentry_config

    def test_sentry_config_receives_any_unrecognized_options(self):
        """
        Any options that aren't recognized by the class will remain untouched by
        the sentry_config method.
        """
        sentry_config = SentryDjangoConfig(
            {
                "enabled": True,
                "traces_sample_rate": 0.5,
                "extra_option_1": False,
                "extra_option_2": {"value1": "string", "value2": True},
            }
        ).sentry_config()

        assert "extra_option_1" in sentry_config
        assert sentry_config["extra_option_2"] == {"value1": "string", "value2": True}
