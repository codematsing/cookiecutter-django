"""Set up virtual environments
"""
#!/usr/bin/env python
import os
from pathlib import Path
import shutil
import argparse

def create_virtual_environment(env_name, src_path):
    CWD = Path(__file__).parent.resolve()
    src_path = CWD / src_path
    env_path = CWD / env_name

    if env_path.exists():
        print(f"{env_path} exists")
    else:
        print("Creating Local Venv")
        os.system(f"virtualenv {env_path}")

        print(f"Copying activate file to {env_path}")
        shutil.copy(src_path / 'activate', env_path / 'bin' / 'activate' )

        print(f"Copying postactivate file to {env_path}")
        shutil.copy(src_path / 'postactivate', env_path / 'bin' / 'postactivate' )

        print(f"Copying predeactivate file to {env_path}")
        shutil.copy(src_path / 'predeactivate', env_path / 'bin' / 'predeactivate' )

    print(f"""
    Virtual environment script improves activation to include env variables.
    Environments are preloaded upon activation and reset upon deactivation

    You may now activate {env_path} by running command:
    source {env_path}/bin/activate

    NOTE: Virtual environment still requires installation of dependencies:
    ({env_name}))$ pip install -r requirements/<path/to/requirements>
    """)

if __name__ == "__main__":
    source_path = {
        'local' : '.envs/.local',
        'prod' : '.envs/.production',
    }
    parser = argparse.ArgumentParser(description="Creates virtual envs")
    parser.add_argument("--type", choices=["local", "prod", "all"], default="all", help="Specify the environment")

    args = parser.parse_args()
    if args.type == "all":
        envs = ["local", "prod"]
    else:
        envs = [args.type]

    for env in envs:
        env_name = f".{env}_venv"
        create_virtual_environment(env_name, source_path[env])
