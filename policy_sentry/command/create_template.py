import click
from pathlib import Path
from policy_sentry.shared.template import create_actions_template, create_crud_template


@click.command(
    context_settings=dict(max_content_width=160),
    short_help='Create write-policy YML template files'
)
@click.option(
    '--output-file',
    type=str,
    required=True,
    help='Relative path to output file where we want to store policy_sentry YML files.'
)
@click.option(
    '--template-type',
    type=click.Choice(['actions', 'crud'], case_sensitive=False),
    required=True,
    help='Type of write_policy template to create - actions or CRUD. Case insensitive.'
)
@click.option(
    '--name',
    type=str,
    required=True,
    help='Name of the IAM role. This will be inside the resulting YML file.'
)
def create_template(output_file, template_type, name):
    """
    Writes YML file templates for use in the write-policy
    command, so users can fill out the fields
    without needing to look up the required format.
    """
    filename = Path(output_file).resolve()
    if template_type == "actions":
        actions_template = create_actions_template(name)
        with open(filename, 'a') as file_obj:
            for line in actions_template:
                file_obj.write(line)

    if template_type == "crud":
        crud_template = create_crud_template(name)
        with open(filename, 'a') as file_obj:
            for line in crud_template:
                file_obj.write(line)

    print("write-policy template file written to:" + str(filename))
