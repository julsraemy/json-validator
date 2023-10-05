# json-validator

json-schema validation of linked.art resources

## Validation

`schema-test.py` shows how to validate records. 

To validate JSON data against a specific Linked Art schema, use the following command:

```bash
python schema-test.py -i "INSTANCE" -s "SCHEMA_NAME"
```

Replace `INSTANCE` with the URL or the path to the JSON instance to validate, and `SCHEMA_NAME` with the name of the schema to validate against (e.g., "core", "concept", "digital", etc.).

### Schemas

Schemas are stored in the `schema` directory.
- concept
- digital
- event
- group
- image
- object
- place
- person
- provenance
- set
- text

## Example

To validate a JSON instance against the "set" schema:

```bash
python schema-test.py -i "https://data.participatory-archives.ch/set/12.json" -s set
```

Output from the script is, for example:

```
------------------------------------------------------------------------------------------------------------------------
Processing: ../linked.art/content/example/person/12.json
  /member_of/0 --> 'id' is a required property 
  /member_of/0 --> Additional properties are not allowed ('member_of', 'classified_as' were unexpected) 
------------------------------------------------------------------------------------------------------------------------
Processing: ../linked.art/content/example/person/13.json
  Validated!
```


## Documentation Generator

Install the generator:

`pip install json-schema-for-humans`

Run the generator:

`generate-schema-doc --config no_show_breadcrumbs --config description_is_markdown --config template_folder=$PWD/template --config template_name=la schema/object.json html/object.html`

The options I use:

* `no_show_breadcrumbs`: this prevents it from showing the path through the schema at each stage. We don't care about the structure of the schema in the API docs.
* `description_is_markdown`: parses the `description` field in the schemas as markdown not plain text, allowing links and basic formatting
* `template_folder` is where templates are available
* `template_name` is the name of the template within the above folder (another directory, with the HTML, CSS and JS files in it)

