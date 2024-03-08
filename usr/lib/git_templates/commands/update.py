import argparse
import sys
import yaml
import subprocess
from pathlib import Path
import shutil

from commands.utils import TemplateManager


def run_git_command(command, cwd=None):
    """Executes a Git command using subprocess."""
    try:
        subprocess.run(command, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command {' '.join(command)}: {e.stderr.decode()}")
        raise

def clone_or_pull_repository(url, clone_path, branch=None):
    """Clones a repository if it doesn't exist, or pulls updates if it does."""
    if clone_path.exists():
        # Pull the latest changes
        run_git_command(['git', 'pull'], cwd=str(clone_path))
    else:
        # Clone the repository
        clone_command = ['git', 'clone', url, str(clone_path)]
        if branch:
            clone_command += ['--branch', branch]
        run_git_command(clone_command)
        if branch:
            # Checkout the specific branch
            run_git_command(['git', 'checkout', branch], cwd=str(clone_path))

def copy_template_content_to_project_root(template_path, project_root):
    """Copies content from the cloned template to the project root directory."""
    for item in template_path.iterdir():
        dest = project_root / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy(item, dest)

def update_templates(refs=None):
    """Updates templates by cloning or pulling them and then copying their contents to the project root."""

    templates_to_update=TemplateManager.get_templates(refs=refs)
    if not templates_to_update:
        print("No templates")
        return
    for key,val in templates_to_update.items():
        clone_or_pull_repository(val.url, val.path, val.branch)
        copy_template_content_to_project_root(val.path,  project_root = Path('./')
    )

    print("Templates updated successfully.")

def update(*args):
    # Process the rest of the arguments using argparse
    parser = argparse.ArgumentParser(description="Pull and copy latest changes from templates, can specify refs.", add_help=False)
    # Check if the first argument is help
    if args and args[0] in ['-h', '--help']:
        parser.print_help()
        return

    print(args)
    update_templates(args)