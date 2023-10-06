import os
import json
import argparse
import requests
import warnings
from jsonschema import validate, Draft202012Validator
from jsonschema.exceptions import ValidationError
from jsonschema._utils import find_additional_properties

def load_json_from_file(file_path):
    with open(file_path) as file:
        return json.load(file)

def merge_schemas(*schemas):
    merged_schema = {}
    for schema in schemas:
        merged_schema.update(schema)
    return merged_schema

def validate_json(json_data, schema):
    return list(Draft202012Validator(schema).iter_errors(json_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate JSON data against a schema.")
    parser.add_argument("-i", "--instance", type=str, required=True, help="Instance URL for validation")
    parser.add_argument("-s", "--schema", type=str, required=True, choices=["core", "concept", "digital", "event", "group", "image", "object", "place", "person", "provenance", "set", "text"], help="Schema to validate against")
    
    args = parser.parse_args()

    # Load the core schema and resolve references
    schema_dir = "schema"
    core_schema_contents = load_json_from_file(os.path.join(schema_dir, "core.json"))
    specified_schema_contents = load_json_from_file(os.path.join(schema_dir, f"{args.schema}.json"))

    # Merge the core and specified schemas
    merged_schema = merge_schemas(core_schema_contents, specified_schema_contents)

    # Load the instance data
    instance = args.instance
    resp = requests.get(instance)
    data = resp.json()

    print("-"*120)
    print("Processing: %s" % instance)

    # Validate JSON data against the merged schema
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        errs = validate_json(data, merged_schema)

    if not errs:
        print("  Validated!")
    else:
        print("  Validation failed. Validation errors:")

        for idx, error in enumerate(errs, start=1):
            print(f"  Error {idx}: /{'/'.join([str(x) for x in error.absolute_path])} --> {error.message}")
