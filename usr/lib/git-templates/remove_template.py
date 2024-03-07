import sys
import yaml
from pathlib import Path


def remove_template(ref):
    templates_path = Path('.git/templates/meta.yaml')

    if not templates_path.exists():
        print("No templates file found.")
        return

    with open(templates_path) as file:
        templates = yaml.safe_load(file) or {}

    if ref not in templates:
        print(f"Template '{ref}' does not exist.")
        return

    del templates[ref]

    with open(templates_path, 'w') as file:
        yaml.safe_dump(templates, file)

    print(f"Template '{ref}' removed successfully.")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python remove_template.py <ref>")
        sys.exit(1)

    _ref = sys.argv[1]
    remove_template(_ref)
