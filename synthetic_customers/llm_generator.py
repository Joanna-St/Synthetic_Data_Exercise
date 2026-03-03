import os
from dotenv import load_dotenv
from anthropic import Anthropic
from .models import Customers

load_dotenv()

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)


def generate_customers_llm(n):
    response = client.messages.parse(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate a random set of customers. {n} entries.",
            }
        ],
        temperature=0.75,
        output_format=Customers,
    )

    return response.parsed_output.customers


if __name__ == "__main__":
    print(generate_customers_llm(2))
