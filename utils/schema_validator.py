import pathlib
import json

from jsonschema import validate, ValidationError

SCHEMA_BASE_PATH = pathlib.Path(__file__).parent.parent / 'response-schemas'


def load_schema(schema_path: pathlib.Path) -> dict:
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return json.loads(content)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Failed to read schema file at: {schema_path}")


def validate_schema(directory_name: str,
                    file_name: str,
                    response_body: dict):
    schema_path = SCHEMA_BASE_PATH / directory_name / f'{file_name}_schema.json'
    schema = load_schema(schema_path)
    try:
        validate(instance=response_body, schema=schema)
    except ValidationError as e:
        # Extract key information for a clearer error message
        path = ".".join(str(p) for p in e.path) if e.path else "root"
        raise AssertionError(
            f"Schema validation failed at '{path}': {e.message}\n\n"
            f"Actual response body:\n{json.dumps(response_body, indent=2)}"
        ) from None
