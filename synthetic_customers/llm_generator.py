import os
from dotenv import load_dotenv
import anthropic
from .models import Customers
import logging

load_dotenv()
logger = logging.getLogger(__name__)

# Client is initialized at module level so it's reused across calls
# rather than recreated on every function invocation.
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

def validate_customer(customer):
    return customer._has_valid_age() and customer._has_valid_name() and customer._has_valid_email() and customer._has_valid_country()

def generate_customers_llm(n):
    """Generate n customers using the Anthropic API.

    Unlike the Faker-based generator, this produces coherent records where
    name, email and country are consistent with each other.

    Returns a list rather than a generator since the entire API response
    is received at once anyway.

    Requires ANTHROPIC_API_KEY to be set in the environment or .env file.
    """
    
    try:
        response = client.messages.parse(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Generate a random set of customers. {n} entries. Deliberately introduce one entry with age under 18 and one with empty country field.",
                }
            ],
            # Higher temperature produces more varied output across runs.
            temperature=0.75,
            # Structured output format — Pydantic model handles validation
            # and deserialization of the response.
            output_format=Customers,
        )
    except anthropic.APIConnectionError as e:
        logger.error("The server could not be reached")
        logger.error(e.__cause__)
        return []
    except anthropic.APIStatusError as e:
        if e.status_code < 500:
            logger.error(f"Client error. {e.response}")
        else:
            logger.error(f"Server error. {e.response}")
        return []

    customers_lst = response.parsed_output.customers
    
    for cust in customers_lst[:]:
        if not validate_customer(cust):
            customers_lst.remove(cust)
            logger.warning(f"Customer {cust.name} with age {cust.age}, email {cust.email} from {cust.country} has invalid field(s) and has been skipped.")

    return customers_lst


if __name__ == "__main__":
    print(generate_customers_llm(10))
