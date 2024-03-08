import dataclasses
import pprint
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

import yaml


@dataclasses.dataclass
class Template:
    branch: str
    url: str
    ref: str
    name:str
    def json(self):
        return dataclasses.asdict(self)
    @property
    def path(self) -> Path:
        return Path('.git/templates') / self.ref
    def __eq__(self, other):
        return self.url == other.url


class TemplateManager:
    templates: Dict[str,Template]={}
    file: Path

    def __init__(self,path:str='.git/templates/meta.yaml') -> None:
        self.file = Path(path)
        self.file.parent.mkdir(parents=True, exist_ok=True)
        self.file.touch(exist_ok=True)
        templates = yaml.safe_load(open(self.file)) or {}
        self.templates = templates
        for key,val in templates.items():
            self.templates[key]=Template(**val)

    def exists(self,ref,template:Template) -> bool:
        return template in self.templates.values() or ref in self.templates

    def add_template(self, url, ref=None,branch=None):
        name=self.get_repo_name_from_url(url)
        ref=ref or name
        template = Template(url=url, branch=branch,ref=ref,name=name)
        if TemplateManager.exists(ref, template):
            print(f"Template '{ref}':{template.url} already exists.")
            return
        TemplateManager.templates[ref] = template


    def get_repo_name_from_url(self,url):
        """Extracts the repository name from a Git URL."""
        path = urlparse(url).path
        ref = path.split('/')[-1].replace('.git', '') if path else None
        if not ref:
            raise ValueError(f"Ref not found from '{path}', set it manually with `-r`")
        return ref

    def write(self):
        yaml.dump(self.json(),open(self.file,'w'),default_flow_style=False)
        print('Templates written to file')

    def json(self):
        return {key:val.json() for key,val in self.templates.items()}

    def delete(self,ref,is_url=False):
        if is_url:
            for key,val in self.templates.items():
                if val.url==ref:
                    ref=key
                    is_url=False
        if is_url or ref not in self.templates:
            print(f"Ref not found: {ref}")
            print("Installed templates:")
            pprint.pp(self.json())
            return
        del self.templates[ref]
        print(f"Successfully removed: {ref}")

    def get_templates(self,refs:List[str]=None)->Optional[Dict[str, Template]]:
        return_refs=self.templates.keys()
        if refs:
            missing_refs = set(refs).difference(set(TemplateManager.templates.keys()))
            if missing_refs:
                print(f"Templates not found: {', '.join(missing_refs)}")
                return
            return_refs=missing_refs
        
        return {key:val for key ,val in self.templates.items() if key in return_refs}

TemplateManager = TemplateManager()
