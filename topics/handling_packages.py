import io
import os
import re
from pprint import pprint

import johnnydep.cli
from typing import Tuple, List, Dict


PATTERN = re.compile(r'^(.+?)[-_]([\d.]+(?:\.post\d+)?)(?:-.+)?\.(?:whl|tar\.gz)$')


def parse_lib_and_ver(filename: str) -> Tuple[str, str] | Tuple[None, None]:
    """
    Parses the name and version from filename.
    Args:
        filename: package filename
    """
    match = re.match(PATTERN, filename)
    return (match.group(1), match.group(2)) if match else (None, None)


def list_packages(
        from_dir: str,
        extension_split=True,
) -> (
        Tuple[List[Tuple[str, str]], List[Tuple[str, str]]] | List[Tuple[str, str]]
):
    """
    Reads packages from the directory.
    Args:
        from_dir: directory that contains downloaded packages from PyPI
        extension_split: sets whether files should be split into .whl and .tar.gz
    Return:
        lists or a list of packages with the entries (<package_name>, <package_version>)
    """
    pckgs_whl = []
    pckgs_tar_gz = []
    pckgs = []
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            pckg_name, pckg_ver = parse_lib_and_ver(file)
            if (pckg_name, pckg_ver) == (None, None):
                print(f"Found not a package: {file}")
            else:
                print(pckg_name, pckg_ver)
                if extension_split:
                    if file.endswith(".whl"):
                        pckgs_whl.append((pckg_name, pckg_ver))
                    elif file.endswith(".tar.gz"):
                        pckgs_tar_gz.append((pckg_name, pckg_ver))
                    else:
                        raise ValueError(f"Unknown file extension: {file}")
                else:
                    pckgs.append((pckg_name, pckg_ver))

    if extension_split:
        print(f"Found {len(pckgs_whl)} .whl packages.")
        print(f"Found {len(pckgs_tar_gz)} .tar.gz packages.")
        return pckgs_whl, pckgs_tar_gz
    else:
        print(f"Found {len(pckgs)} packages.")
        return pckgs


def look_for_dependencies(
        package_list: List[Tuple[str, str]]
) -> Dict[Tuple[str, str], List[Tuple[str, str]]]:
    """
    Finds dependencies of packages
    Args:
        package_list: list of packages with entries (<package_name>, <package_version>)
    Return:
        dictionary with dependencies
    """
    deps = {}
    for pckg_name, pckg_ver in package_list:
        pckg_name = pckg_name.replace("_", "-")
        string_io = io.StringIO()
        print(f"Searching for dependencies of {pckg_name}")
        johnnydep.cli.main(
            argv=[f"{pckg_name}=={pckg_ver}", "-o" "pinned", "-v" "0"],
            stdout=string_io,
        )

        pckg_deps = []
        string_io.seek(0)  # Change the cursor position
        for line in string_io:
            line = line[:-1]
            dep_pckg_name, dep_pckg_ver = line.split("==")  # --output-format pinned
            dep_pckg_name = dep_pckg_name.replace("_", "-")
            if dep_pckg_name != pckg_name:
                pckg_deps.append((dep_pckg_name, dep_pckg_ver))

        string_io.close()
        deps[(pckg_name, pckg_ver)] = pckg_deps
    return deps


if __name__ == "__main__":
    pack_list_whl, pack_list_tar_gz = list_packages(from_dir=r"F:\...")
    # numpy 1.26.4
    # pandas 2.2.2
    # python_dateutil 2.9.0.post0
    # pytz 2024.1
    # six 1.16.0
    # tzdata 2024.1
    # Found 6 .whl packages.
    # Found 0 .tar.gz packages.
    print(".whl:")
    # .whl:
    pprint(pack_list_whl)
    # [('numpy', '1.26.4'),
    #  ('pandas', '2.2.2'),
    #  ('python_dateutil', '2.9.0.post0'),
    #  ('pytz', '2024.1'),
    #  ('six', '1.16.0'),
    #  ('tzdata', '2024.1')]
    print(".tar.gz:")
    # .tar.gz:
    pprint(pack_list_tar_gz)
    # []
    dep_dict = look_for_dependencies(package_list=pack_list_whl)
    # Searching for dependencies of numpy
    # Searching for dependencies of pandas
    # Searching for dependencies of python_dateutil
    # Searching for dependencies of pytz
    # Searching for dependencies of six
    # Searching for dependencies of tzdata
    print("dependencies:")
    # dependencies:
    pprint(dep_dict)
    # {('numpy', '1.26.4'): [],
    #  ('pandas', '2.2.2'): [('numpy', '1.26.4'),
    #                        ('python_dateutil', '2.9.0.post0'),
    #                        ('pytz', '2024.1'),
    #                        ('tzdata', '2024.1'),
    #                        ('six', '1.16.0')],
    #  ('python_dateutil', '2.9.0.post0'): [('six', '1.16.0')],
    #  ('pytz', '2024.1'): [],
    #  ('six', '1.16.0'): [],
    #  ('tzdata', '2024.1'): []}
