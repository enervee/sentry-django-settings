"""
This is the Django configuration file for Sentry.
"""
import logging
import warnings

from django.apps import AppConfig
from django.conf import settings

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

logger = logging.getLogger("django.sentry_django_settings")


class Sentry(AppConfig):
    name = "sentry_django_settings"

    extra_config_options = {"enabled", "git_sha_path"}

    def ready(self):
        warnings.warn(
            "sentry_django_settings is no longer supported. See "
            "https://github.com/enervee/sentry-django-settings/issues/12 for more information.",
            FutureWarning,
            stacklevel=2,
        )
        sentry_setting = getattr(settings, "SENTRY", None)
        if not sentry_setting:
            logger.warning("No SENTRY settings found.")
            return

        sentry_django_config = SentryDjangoConfig(sentry_setting)

        if not sentry_django_config.enabled():
            logger.info("Sentry disabled.")
            return

        converted_config = sentry_django_config.sentry_config()
        sentry_sdk.init(**converted_config)


class SentryDjangoConfig:
    EXTRA_CONFIG_OPTIONS = {"enabled", "git_sha_path"}

    def __init__(self, config):
        self.config = config

    def sentry_config(self):
        """Creates the Sentry config based on default values and the configuration
        in the settings.

        Returns:
            dict: a collection of Sentry configuration options
        """
        config = self.default_config()
        config.update(self.config)
        self.remove_extra_options(config)
        return config

    def enabled(self):
        return self.config.get("enabled", False)

    @staticmethod
    def default_config():
        return {"integrations": [DjangoIntegration()]}

    @classmethod
    def remove_extra_options(cls, config):
        for extra_key in cls.EXTRA_CONFIG_OPTIONS:
            if extra_key == "git_sha_path" and extra_key in config:
                warnings.warn(
                    "`git_sha_path` is no longer supported and has no effect. "
                    "See https://docs.sentry.io/platforms/python/configuration/options/#release"
                    " on how to set the release directly.",
                    FutureWarning,
                    stacklevel=4,
                )
            config.pop(extra_key, None)
