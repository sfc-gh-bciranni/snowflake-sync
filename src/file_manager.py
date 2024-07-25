import os
import yaml

from typing import Any, Dict

def make_dir(obj_name: str, root_dir: str) -> str:
    # Create Object Directory
    obj_dir = os.path.join(root_dir, obj_name)
    os.makedirs(obj_dir, exist_ok=True)
    return obj_dir

def write_object_yaml(obj: Dict[str, Any], obj_dir: str) -> None:
    obj_name = obj['name'].lower()
    obj_file = os.path.join(obj_dir, 'metadata', f'{obj_name}.yaml')
    os.makedirs(os.path.join(obj_dir, 'metadata'), exist_ok=True)
    with open(obj_file, 'w') as f:
        yaml.dump(obj, f, default_flow_style=False)

def write_object_ddl(ddl: str, obj_name: str, obj_dir: str) -> None:
    obj_ddl_file = os.path.join(obj_dir, f'{obj_name}.sql')
    with open(obj_ddl_file, 'w') as f:
        f.write(ddl)