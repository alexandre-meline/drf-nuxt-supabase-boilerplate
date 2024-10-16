import sentry_sdk
from .base import env

sentry_sdk.init(
    dsn=env.str('SENTRY_DSN'),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=env.float('SENTRY_TRACES_SAMPLE_RATE', default=1.0),
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=env.float('SENTRY_PROFILES_SAMPLE_RATE', default=1.0),
)