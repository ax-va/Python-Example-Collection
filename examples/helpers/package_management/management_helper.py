"""
This module offers helper functions for management of Python packages.
"""
import io
import os
import re
import johnnydep.cli
from typing import Tuple, List, Dict

# pattern to extract a name and version of a downloaded PyPI package
NAME_AND_VERSION_PATTERN = re.compile(r"^(.+)-([\d.]+(?:post|dev)?\d*).*(?:whl|tar\.gz)$")


def parse_name_and_version(filename: str) -> Tuple[str, str] | Tuple[None, None]:
    """
    Parses the name and version from the package filename.
    Args:
        filename: package filename
    Returns:
        (<package_name>, <package_version>) matching the pattern or (None, None)
    """
    match = re.match(NAME_AND_VERSION_PATTERN, filename)
    return (match.group(1), match.group(2)) if match else (None, None)


def list_packages_from_dir(
    dir_path: str,
    extension_split=True,
) -> (Tuple[List[Tuple[str, str]], List[Tuple[str, str]]] | List[Tuple[str, str]]):
    """
    Lists packages from the directory.
    Args:
        dir_path: directory that contains downloaded packages from PyPI
        extension_split: sets whether files should be split into `.whl` and `.tar.gz`
    Returns:
        lists or a list of packages with the entries (<package_name>, <package_version>)
    """
    pckgs_whl = []
    pckgs_tar_gz = []
    pckgs = []
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            pckg_name, pckg_ver = parse_name_and_version(filename)
            if (pckg_name, pckg_ver) == (None, None):
                print(f"Found not a package: {filename}")
            else:
                print(pckg_name, pckg_ver)
                if extension_split:
                    if filename.endswith(".whl"):
                        pckgs_whl.append((pckg_name, pckg_ver))
                    elif filename.endswith(".tar.gz"):
                        pckgs_tar_gz.append((pckg_name, pckg_ver))
                    else:
                        raise ValueError(f"Unknown file extension: {filename}")
                else:
                    pckgs.append((pckg_name, pckg_ver))

    if extension_split:
        print(f"Found {len(pckgs_whl)} .whl packages.")
        print(f"Found {len(pckgs_tar_gz)} .tar.gz packages.")
        return pckgs_whl, pckgs_tar_gz
    else:
        print(f"Found {len(pckgs)} packages.")
        return pckgs


def get_dependencies(
    package_list: List[Tuple[str, str]],
) -> Dict[Tuple[str, str], List[Tuple[str, str]]]:
    """
    Looks for dependencies of packages using the `johnnydep` package.
    Args:
        package_list: list of packages with entries (<package_name>, <package_version>)
    Returns:
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
    dep_dict = get_dependencies(package_list=[("pandas", "2.2.1")])
