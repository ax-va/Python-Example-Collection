import io
import os
import re
from typing import Tuple, List, Dict

import johnnydep.cli

DOWNLOADED_PCKGS_DIR = r"F:\ML_24_02\ML_24_02_new"
PATTERN = re.compile(r"(.*)-(\d+\.*\d+\.*\d*\.*\w*\d*).*")

temp_str = io.StringIO()


def get_pckgs_in_dir(pckgs_dir: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    pckgs_whl = []
    pckgs_tar_gz = []
    for root, dirs, files in os.walk(pckgs_dir):
        for file in files:
            pckg_name, pckg_ver = PATTERN.findall(file)[0]
            print(pckg_name, pckg_ver)
            if file.endswith(".whl"):
                pckgs_whl.append((pckg_name, pckg_ver))
            elif file.endswith(".tar.gz"):
                pckgs_tar_gz.append((pckg_name, pckg_ver))
            else:
                raise ValueError(f"Unknown file extension: {file}")

    print(f"Found {len(pckgs_whl)} .whl packages.")
    print(f"Found {len(pckgs_tar_gz)} .tar.gz packages.")
    return pckgs_whl, pckgs_tar_gz


def get_pckgs_deps(pckgs: List[Tuple[str, str]]) -> Dict[str, Dict[str, str]]:
    deps = {}
    for pckg_name, pckg_ver in pckgs:
        print(f"Searching dependencies for {pckg_name}")
        with open("pckg_deps.txt", "w") as file:
            johnnydep.cli.main(argv=[f"{pckg_name}=={pckg_ver}", "-o" "pinned", "-v" "0"], stdout=file)

        _deps = {}
        with open("pckg_deps.txt", "r") as file:
            for line in file:
                line = line[:-1]
                dep_pckg_name, dep_pckg_ver = line.split("==")  # --output-format pinned
                _deps[dep_pckg_name] = dep_pckg_ver

        deps[pckg_name] = _deps
    return deps


if __name__ == "__main__":
    pckgs_whl, pckgs_tar_gz = get_pckgs_in_dir(pckgs_dir=DOWNLOADED_PCKGS_DIR)
    pckgs_deps = get_pckgs_deps(pckgs_whl)

    for pckg_name, pckg_deps in pckgs_deps.items():
        print(f"Found dependencies for package {pckg_name}")
        for dep_pckg_name, dep_pckg_ver in pckg_deps.items():
            print(f"\t\t{dep_pckg_name} {dep_pckg_ver}")
        print("-"*30)
