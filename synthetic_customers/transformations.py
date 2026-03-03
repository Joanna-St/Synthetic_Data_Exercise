import dataclasses
import logging
import functools

logger = logging.getLogger(__name__)


def log_transform(func):
    """Decorator that logs whenever a transformation function is called.

    functools.wraps preserves the original function's name and docstring,
    so decorated functions still appear under their own name in logs and tracebacks.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Applying transform: %s", func.__qualname__)
        return func(*args, **kwargs)

    return wrapper


@log_transform
def anonymize(customer):
    """Replace the customer's name with initials and redact the email."""
    initials = ".".join([name[0] for name in customer.name.split()])
    return dataclasses.replace(customer, name=initials, email="REDACTED")


@log_transform
def capitalize_country(customer):
    """Convert the country field to uppercase."""
    return dataclasses.replace(customer, country=customer.country.upper())
