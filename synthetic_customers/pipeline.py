from .writer import write_csv, write_json
from . import transformations
from .faker_generator import generate_customers_faker
from .llm_generator import generate_customers_llm
from . import constants
import argparse
import logging

logger = logging.getLogger(__name__)

# basicConfig is called once here at the entry point so all loggers
# across the package write to the same file with the same format.
logging.basicConfig(
    filename=constants.LOGFILE,
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%d-%m-%Y %H:%M:%S",
)


def run_pipeline(n, filepath, method, transforms: list):
    """Run the full data generation pipeline.

    Generates n customer records using the specified method, applies
    each transformation in order, then writes the result to CSV and JSON.
    """
    logger.info("Generating %d customers to %s", n, filepath)

    if method == "faker":
        customers = generate_customers_faker(n)
    elif method == "llm":
        customers = generate_customers_llm(n)
    else:
        raise ValueError(f"Unknown method: {method}")

    # Transforms are looked up by name on the transformations module,
    # so adding a new transformation function there makes it available
    # via CLI automatically without changing this file.
    for trs in transforms or []:
        func = getattr(transformations, trs, None)
        if func is None:
            raise ValueError(f"Unknown transform: {trs}")
        customers = [func(cust) for cust in customers]

    write_csv(customers, f"{filepath}.csv")
    write_json(customers, f"{filepath}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic customer data pipeline.")
    parser.add_argument("-c", "--count", type=int, default=constants.DEFAULT_COUNT, help="Number of entries to produce.")
    parser.add_argument("-o", "--output", default=constants.DEFAULT_OUTPUT, help="Output filename without extension.")
    parser.add_argument("-m", "--method", default="faker", help="Generation method: faker or llm.")
    parser.add_argument("-tr", "--transforms", nargs="*", default=None, help="Transformations to apply.")
    args = parser.parse_args()

    run_pipeline(args.count, args.output, args.method, args.transforms)
