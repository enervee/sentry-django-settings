"""
This is the Django configuration file for Sentry.
"""
from __future__ import unicode_literals
import logging

from django.apps import AppConfig
from django.conf import settings

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from sentry_django_settings.git_sha import get_from_repo, get_from_file

logger = logging.getLogger("django.sentry_django_settings")


class Sentry(AppConfig):
    name = "sentry_django_settings"

    extra_config_options = {"enabled", "git_sha_path"}

    def ready(self):
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
        config["release"] = self.get_release()
        self.remove_extra_options(config)
        return config

    def get_release(self):
        """Gets the "release" value. If one isn't given, it tries to get it
        from the project."""
        release = self.config.get("release")
        if not release:
            release = get_from_repo()
        if not release and self.config.get("git_sha_path"):
            release = get_from_file(self.config.get("git_sha_path"))

        return release

    def enabled(self):
        return self.config.get("enabled", False)

    @staticmethod
    def default_config():
        return {"integrations": [DjangoIntegration()]}

    @classmethod
    def remove_extra_options(cls, config):
        for extra_key in cls.EXTRA_CONFIG_OPTIONS:
            config.pop(extra_key, None)
