from .writer import write_csv, write_json
from . import transformations
from .faker_generator import generate_customers_faker
from .llm_generator import generate_customers_llm
from . import constants
import argparse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=constants.LOGFILE,
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%d-%m-%Y %H:%M:%S",
)


def run_pipeline(n, filepath, method, transforms: list):
    logger.info("Generating %d customers to %s", n, filepath)

    customers = []

    if method == "faker":
        customers = generate_customers_faker(n)
    elif method == "llm":
        customers = generate_customers_llm(n)
    else:
        raise ValueError(f"Unknown method: {method}")

    for trs in transforms:
        func = getattr(transformations, trs, None)
        if func is None:
            raise ValueError(f"Unknown transform: {trs}")

        customers = [func(cust) for cust in customers]

    write_csv(customers, f"{filepath}.csv")
    write_json(customers, f"{filepath}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, default=constants.DEFAULT_COUNT, help="Number of entries to produce.")
    parser.add_argument("-o", "--output", default=constants.DEFAULT_OUTPUT, help="Output file name.")
    parser.add_argument("-m", "--method", default="faker", help="Method to use.")
    parser.add_argument("-tr", "--transforms", nargs="*", default=None, help="Transformations to apply.")
    args = parser.parse_args()

    run_pipeline(args.count, args.output, args.method, args.transforms)
