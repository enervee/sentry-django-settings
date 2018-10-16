"""
This is the Django configuration file for Sentry.

To use:
1) Install `sentry_sdk` and `gitpython` libraries using pip/pipenv.

2) Add `sentry.apps.Sentry` to your INSTALLED_APPS.

3) Add a setting such as the following to you Django settings:

SENTRY = {
    'enabled': True,
    'dsn': "https://e7c7cbff64d34e4a95cd1d223e443464@sentry-dev.enervee.com/5",
    'environment': "dev"
}

- To find the DSN in Sentry:
    - Go to the project settings in Sentry
    - Under `Data`, select `Error Tracking`
    - Click "Get your DSN."
    - Use the "Public DSN" in all cases.
"""
from __future__ import unicode_literals
import logging

from django.apps import AppConfig
from django.conf import settings

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import git


logger = logging.getLogger("django.sentry_app")


class Sentry(AppConfig):
    name = ''

    def ready(self):
        if not getattr(settings, "SENTRY"):
            logger.warn("No SENTRY settings found.")
            return
        if not settings.SENTRY["enabled"]:
            logger.info("Sentry disabled.")
            return

        self.init_sentry(settings.SENTRY['dsn'], settings.SENTRY['environment'])
        logger.info("Sentry enabled.")

    def init_sentry(self, dsn, environment):
        """
        Sets up Sentry to send errors to the Sentry server.
        """
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha

        sentry_sdk.init(
            dsn=dsn,
            integrations=[DjangoIntegration()],
            environment=environment,
            release=sha,
        )
