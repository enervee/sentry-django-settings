from unittest import mock

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

    def test_sentry_config_adds_default_release_from_git_repo(self, mock_get_from_repo):
        """
        If the release option is not specified, it will attempt to pull the release from
        the SHA commit hash for HEAD.
        """
        mock_get_from_repo.return_value = "HEAD SHA Value"

        sentry_config = SentryDjangoConfig({}).sentry_config()

        assert sentry_config["release"] == "HEAD SHA Value"

    def test_sentry_config_release_default_falls_back_to_specified_sha_file(
        self,
        mock_get_from_repo,
        mock_get_from_file,
    ):
        """
        If the git_sha_path option is specified and a release wasn't provided or discovered
        from the git repo, then the release is set to the contents of that file.
        """
        mock_get_from_repo.return_value = None  # get_from_repo couldn't find a commit
        mock_get_from_file.return_value = "SHA stored in file"

        sentry_config = SentryDjangoConfig(
            {"git_sha_path": "project_sha_file.txt"}
        ).sentry_config()

        assert sentry_config["release"] == "SHA stored in file"
        assert mock_get_from_file.mock_calls == [mock.call("project_sha_file.txt")]

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
