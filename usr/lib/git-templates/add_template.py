import sys
import yaml
from pathlib import Path


def add_template(ref, url, branch=None):
    templates_path = Path('.git/templates/meta.yaml')
    templates_path.parent.mkdir(parents=True, exist_ok=True)
    templates = {}

    if templates_path.exists():
        with open(templates_path) as file:
            templates = yaml.safe_load(file) or {}

    if ref in templates:
        raise ValueError(f"Template '{ref}' already exists.")

    templates[ref] = {'url': url, 'branch': branch}

    with open(templates_path, 'w') as file:
        yaml.safe_dump(templates, file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python add_template.py <ref> <url> [<branch>]")
        sys.exit(1)

    _ref = sys.argv[1]
    _url = sys.argv[2]
    _branch = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        add_template(_ref, _url, _branch)
        print(f"Template '{_ref}' added successfully.")
    except ValueError as e:
        print(e)
        sys.exit(1)
