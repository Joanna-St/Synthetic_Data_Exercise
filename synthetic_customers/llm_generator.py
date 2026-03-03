import os
from dotenv import load_dotenv
from anthropic import Anthropic
from .models import Customers

load_dotenv()

# Client is initialized at module level so it's reused across calls
# rather than recreated on every function invocation.
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


def generate_customers_llm(n):
    """Generate n customers using the Anthropic API.

    Unlike the Faker-based generator, this produces coherent records where
    name, email and country are consistent with each other.

    Returns a list rather than a generator since the entire API response
    is received at once anyway.

    Requires ANTHROPIC_API_KEY to be set in the environment or .env file.
    """
    response = client.messages.parse(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate a random set of customers. {n} entries.",
            }
        ],
        # Higher temperature produces more varied output across runs.
        temperature=0.75,
        # Structured output format — Pydantic model handles validation
        # and deserialization of the response.
        output_format=Customers,
    )

    return response.parsed_output.customers


if __name__ == "__main__":
    print(generate_customers_llm(2))
