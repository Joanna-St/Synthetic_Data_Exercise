import dataclasses
import logging
import functools

logger = logging.getLogger(__name__)


def log_transform(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Applying transform: %s", func.__qualname__)
        return func(*args, **kwargs)

    return wrapper


@log_transform
def anonymize(customer):
    initials = ".".join([name[0] for name in customer.name.split()])
    return dataclasses.replace(customer, name=initials, email="REDACTED")


@log_transform
def capitalize_country(customer):
    return dataclasses.replace(customer, country=customer.country.upper())
