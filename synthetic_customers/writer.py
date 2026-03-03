import dataclasses
import csv
import json
from .faker_generator import generate_customers_faker
from .models import Customer


def write_csv(customers, filepath):
    fieldnames = [f.name for f in dataclasses.fields(Customer)]

    with open(filepath, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for cust in customers:
            writer.writerow(dataclasses.asdict(cust))


def write_json(customers, filepath):
    with open(filepath, "w") as jsonfile:
        json.dump([dataclasses.asdict(cust) for cust in customers], jsonfile)


if __name__ == "__main__":
    write_csv(generate_customers_faker(20), "output.csv")
    write_json(generate_customers_faker(20), "output.json")
