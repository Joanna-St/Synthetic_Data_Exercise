# Synthetic Customer Data Pipeline

A learning project — a command-line tool that generates synthetic customer datasets and exports them to CSV and JSON.

Built with Python, using [Faker](https://faker.readthedocs.io/) and the Anthropic Claude API for data generation.

## Setup

```bash
pip install faker anthropic pydantic python-dotenv
```

For LLM-based generation, create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

Run from the project root:

```bash
python -m synthetic_customers.pipeline
```

Optional arguments:

- `-c / --count` — number of records to generate (default: 30)
- `-o / --output` — output filename without extension (default: `my_output`)
- `-m / --method` — `faker` or `llm` (default: `faker`)
- `-tr / --transforms` — transformations to apply, e.g. `anonymize capitalize_country`
