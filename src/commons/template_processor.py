import os
from jinja2 import Environment, FileSystemLoader

def generate_html_from_template(root_template_path, parameters, output_path):
    # Get the absolute path of the template directory
    template_dir = os.path.abspath(os.path.dirname(root_template_path))
    template_file = os.path.basename(root_template_path)

    print(f"Template directory: {template_dir}")
    print(f"Template file: {template_file}")

    # Create a Jinja2 environment with custom delimiters
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True,
        variable_start_string='[[',
        variable_end_string=']]'
    )

    # Load the template
    template = env.get_template(template_file)

    # Render the template with the parameters
    output_from_parsed_template = template.render(parameters)

    # Write the rendered HTML to the output path
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_from_parsed_template)
