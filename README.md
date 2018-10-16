# Django Sentry

This is a package for Django that allows you to add Sentry integration by adding a Django setting.

## Installation

`pip install django_sentry`

Add `sentry` to your `INSTALLED_APPS`.

Add a setting like the following to your `settings.py` file:

```python
SENTRY = {
    'enabled': True,
    'dsn': "https://2e2ac79f64d34e4b85c3a3173e343464@sentry.mysite.com/5",
    'environment': "dev"
}
```

To find the DSN in Sentry:

- Go to the project settings in Sentry
- Under `Data`, select `Error Tracking`
- Click "Get your DSN."
- Use the "Public DSN" in all cases.

The `environment` should be appropriate to environment where the server will be running.