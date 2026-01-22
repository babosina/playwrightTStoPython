import pathlib
import json

from genson import SchemaBuilder
from jsonschema import validate, ValidationError

SCHEMA_BASE_PATH = pathlib.Path(__file__).parent.parent / 'response_schemas'


def load_schema(schema_path: pathlib.Path) -> dict:
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return json.loads(content)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Failed to read schema file at: {schema_path}")


def validate_schema(directory_name: str,
                    file_name: str,
                    response_body: dict,
                    create_schema_flag: bool = False):
    schema_path = SCHEMA_BASE_PATH / directory_name / f'{file_name}_schema.json'

    if create_schema_flag:
        generate_new_schema(schema_path, response_body)

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


def generate_new_schema(schema_path: pathlib.Path, response_body: dict):
    builder = SchemaBuilder()
    builder.add_object(response_body)
    # Explicitly specify the metaschema URI to stop the DeprecationWarning
    schema = builder.to_schema()
    schema['$schema'] = 'http://json-schema.org/draft-07/schema#'

    try:
        # Create the parent directory if it doesn't exist
        # parents=True: creates all missing parent directories (like mkdir -p)
        # exist_ok=True: doesn't raise an error if the directory already exists
        schema_path.parent.mkdir(parents=True, exist_ok=True)

        with open(schema_path, 'w') as f:
            json.dump(schema, f, indent=2)
    except PermissionError:
        raise PermissionError(f"Don't have permissions to write to: {schema_path}")
    except OSError as e:
        raise OSError(f"Failed to create schema file at: {schema_path}")
