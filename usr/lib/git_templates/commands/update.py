import sys
import yaml
import subprocess
from pathlib import Path
import shutil

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
    templates_path = Path('.git/templates/meta.yaml')
    project_root = Path('./')

    if not templates_path.exists():
        raise FileNotFoundError("Templates file not found.")

    with open(templates_path) as file:
        templates = yaml.safe_load(file) or {}

    if refs:
        missing_refs = [ref for ref in refs if ref not in templates]
        if missing_refs:
            raise ValueError(f"Templates not found: {', '.join(missing_refs)}")
        templates_to_update = {ref: templates[ref] for ref in refs}
    else:
        templates_to_update = templates

    for ref, details in templates_to_update.items():
        url = details['url']
        branch = details.get('branch')
        clone_path = Path('.git/templates') / ref
        clone_or_pull_repository(url, clone_path, branch)
        copy_template_content_to_project_root(clone_path, project_root)

    print("Templates updated successfully.")

def update():
    ...