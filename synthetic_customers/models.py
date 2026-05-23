from dataclasses import dataclass
from pydantic import BaseModel
import re


@dataclass
class Customer:
    """Core data model representing a single customer record."""

    id: int
    name: str
    email: str
    age: int
    country: str = "Unknown"

    def _has_valid_age(self):
        return self.age >= 18 and self.age <= 80

    def _has_valid_name(self):
        return self.name and isinstance(self.name, str) and len(self.name) > 0
    
    def _has_valid_email(self):
        # regex = "[\S]+@[\S]+.[\S]+"
        # return re.match(regex, self.email)
        return self.email and isinstance(self.email, str) and len(self.email) > 0
    
    def _has_valid_country(self):
        return self.country and isinstance(self.country, str) and len(self.country) > 0


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