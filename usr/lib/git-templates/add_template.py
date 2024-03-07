import sys
import yaml
import argparse
from pathlib import Path
from urllib.parse import urlparse

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
        yaml.safe_dump(templates, file, default_flow_style=False)

def get_repo_name_from_url(url):
    """Extracts the repository name from a Git URL."""
    path = urlparse(url).path
    ref=path.split('/')[-1].replace('.git', '') if path else None
    if not ref:
        raise ValueError(f"Ref not found from '{path}', set it manually with `-r`")
    return ref

def main():
    parser = argparse.ArgumentParser(description="Add a git template to the .git/templates/meta.yaml file.")
    parser.add_argument('-r', '--ref', type=str, help="Reference name for the template. Defaults to the repo name extracted from the URL.")
    parser.add_argument('url', type=str, help="URL of the git repository.")
    parser.add_argument('-b', '--branch', type=str, help="Branch name. If not specified, defaults to null in the YAML file.", default=None)
    parser.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

    args = parser.parse_args()

    ref = args.ref if args.ref else get_repo_name_from_url(args.url)

    try:
        add_template(ref, args.url, args.branch)
        print(f"Template '{ref}' added successfully.")
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
