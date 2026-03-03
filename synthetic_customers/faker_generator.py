from .models import Customer
import random
from faker import Faker


def generate_customers_faker(n: int):
    """Generate n customers with random fake data.

    Uses Faker for names, emails and countries — note that these fields
    are generated independently so they won't be coherent (e.g. the email
    won't match the name). Use generate_customers_llm for coherent records.

    Yields one Customer at a time to avoid loading the full dataset into memory.
    """
    fake = Faker()
    for i in range(n):
        yield Customer(
            i, fake.name(), fake.email(), random.randint(18, 80), fake.country()
        )


if __name__ == "__main__":
    for c in generate_customers_faker(7):
        print(c)
