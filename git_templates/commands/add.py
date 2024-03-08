import argparse

from .utils import TemplateManager


def add(git_url: str, *args_list):
    # Process the rest of the arguments using argparse
    parser = argparse.ArgumentParser(
        description="Add a git template to the .git/templates/meta.yaml file.",
        add_help=False,
    )
    parser.add_argument(
        "-r",
        "--ref",
        type=str,
        help="Reference name for the template. Defaults to the repo name extracted from the URL.",
    )
    parser.add_argument(
        "-b",
        "--branch",
        type=str,
        help="Branch name. If not specified, defaults to null in the YAML file.",
        default=None,
    )
    # Check if the first argument is help
    if git_url in ["-h", "--help"]:
        parser.print_help()
        return

    # Since the URL is already extracted, we parse the remaining args
    args = parser.parse_args(args_list)
    added = TemplateManager.add_template(ref=args.ref, branch=args.branch, url=git_url)
    if added:
        print(f"Successfully added {git_url}.")
        TemplateManager.write()


# Example usage:
# add(['https://github.com/example/repo.git', '-r', 'customRef', '-b', 'main'])
