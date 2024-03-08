import argparse
import sys
import yaml
from pathlib import Path

from commands.utils import TemplateManager
def remove(ref:str,*args):
    # Process the rest of the arguments using argparse
    parser = argparse.ArgumentParser(description="Remove a git template by ref from the .git/templates/meta.yaml file."
                                                 "if arg contains `git@` will attempt to remove by url", add_help=False)

    # Check if the first argument is help
    if ref in ['-h', '--help']:
        parser.print_help()
        return
    # Since the URL is already extracted, we parse the remaining args
    result=TemplateManager.delete(ref,is_url='git@' in ref)
    if result:
        print(f"Successfully removed: {ref}")
        TemplateManager.write()
