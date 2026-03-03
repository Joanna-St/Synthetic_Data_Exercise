from .models import Customer
import random
from faker import Faker


def generate_customers_faker(n: int):
    fake = Faker()
    for i in range(n):
        yield Customer(
            i, fake.name(), fake.email(), random.randint(18, 80), fake.country()
        )


if __name__ == "__main__":
    for c in generate_customers_faker(7):
        print(c)
