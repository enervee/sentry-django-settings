# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.1]

- Version bump to fix project description

## [0.6.0]

### Deprecated

- sentry-django-settings is deprecated and no longer supported, and the Django app will emit a FutureWarning if included in the `INSTALLED_APPS` setting.
  - [See here for more information](https://github.com/enervee/sentry-django-settings/issues/12)

### Removed

- Support for `git_sha_path` has been removed in favor of Sentry's default behavior for `release`.
  - If you previously used `release` directly, or supplied _neither_ `release` or `git_sha_path`,
    behavior will be unchanged
  - If you used `git_sha_path` and not `release`, then the library will warn you that `git_sha_path`
    no longer has any affect. Sentry will fall back to it's default behavior of naming the release
    (currently uses the current git commit's SHA hash).

## [0.5.0]

### Added

- Library now supports configuration that is passed directly onto Sentry's `init` method (https://docs.sentry.io/platforms/python/configuration/options/)

[unreleased]: https://github.com/enervee/sentry-django-settings/compare/v0.6.1...HEAD
[0.6.1]: https://github.com/enervee/sentry-django-settings/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/enervee/sentry-django-settings/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/enervee/sentry-django-settings/compare/v0.4.0...v0.5.0
