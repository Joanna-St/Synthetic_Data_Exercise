from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Customer:
    """Core data model representing a single customer record."""

    id: int
    name: str
    email: str
    age: int
    country: str = "Unknown"


class Customers(BaseModel):
    """Pydantic wrapper used for parsing structured LLM responses.
    Pydantic handles validation and deserialization; Customer itself
    stays a plain dataclass for use throughout the rest of the pipeline."""

    customers: list[Customer]


if __name__ == "__main__":
    c1 = Customer(1, "A", "A@mail.com", 20, "Georgia")
    c2 = Customer(2, "B", "B@mail.com", 21, "USA")
    c3 = Customer(3, "C", "C@mail.com", 22, "Philippines")

    for c in [c1, c2, c3]:
        print(c)
