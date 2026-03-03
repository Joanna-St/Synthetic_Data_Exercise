from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Customer:
    id: int
    name: str
    email: str
    age: int
    country: str = "Unknown"


class Customers(BaseModel):
    customers: list[Customer]


if __name__ == "__main__":
    c1 = Customer(1, "A", "A@mail.com", 20, "Georgia")
    c2 = Customer(2, "B", "B@mail.com", 21, "USA")
    c3 = Customer(3, "C", "C@mail.com", 22, "Philippines")

    for c in [c1, c2, c3]:
        print(c)
