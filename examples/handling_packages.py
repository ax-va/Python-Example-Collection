import io
import os
import re
import johnnydep.cli
from typing import Tuple, List, Dict
from pprint import pprint

# pattern to extract a name and version of a downloaded PyPI package
NAME_AND_VERSION = re.compile(r'^(.+)-([\d.]+(?:post|dev)?\d*).*(?:whl|tar\.gz)$')


def parse_name_and_version(filename: str) -> Tuple[str, str] | Tuple[None, None]:
    """
    Parses the name and version from filename.
    Args:
        filename: package filename
    Returns:
        (<package_name>, <package_version>) matching the pattern or (None, None)
    """
    match = re.match(NAME_AND_VERSION, filename)
    return (match.group(1), match.group(2)) if match else (None, None)


def list_packages_from_dir(
        from_dir: str,
        extension_split=True,
) -> (
        Tuple[List[Tuple[str, str]], List[Tuple[str, str]]] | List[Tuple[str, str]]
):
    """
    Lists packages from the directory.
    Args:
        from_dir: directory that contains downloaded packages from PyPI
        extension_split: sets whether files should be split into .whl and .tar.gz
    Returns:
        lists or a list of packages with the entries (<package_name>, <package_version>)
    """
    pckgs_whl = []
    pckgs_tar_gz = []
    pckgs = []
    for root, dirs, files in os.walk(from_dir):
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


def look_for_dependencies(
        package_list: List[Tuple[str, str]]
) -> Dict[Tuple[str, str], List[Tuple[str, str]]]:
    """
    Looks for dependencies of packages.
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


def write_only_package_names(
        input_filename: str,
        output_filename: str,
) -> None:
    """
    Write only the package names from input_file to output_file.

    Args:
        input_filename: input file with names and versions of packages
        output_filename: output file with only the package names
    """
    package_names = []
    with open(input_filename, "r") as f:
        for line in f:
            package_names.append(line.split("==")[0].strip())

    with open(output_filename, "w") as f:
        f.write("\n".join(package_names))


if __name__ == "__main__":

    """
    write_only_package_names(
        input_filename=r"...",
        output_filename=r"...",
    )
    """

    """
    pack_list_whl, pack_list_tar_gz = list_packages_from_dir(from_dir=r"...")
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

    pack_list_total = pack_list_whl + pack_list_tar_gz
    with open(r"...", "w") as f:
        f.write("\n".join([f"{pack[0]}=={pack[1]}" for pack in pack_list_total]))
    """

    """
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
    """

    """
    pack_list_total = list_packages_from_dir(from_dir=r"...", extension_split=False)
    with open(r"...", "w") as f:
        f.write("\n".join([f"{pack[0]}=={pack[1]}" for pack in pack_list_total]))
    """

    requirements_filenames = [
        r"...",
    ]

    lines = []
    for requirements_filename in requirements_filenames:
        with open(requirements_filename, "r") as f:
            for line in f:
                lines.append(line.strip() + "\n")

    with open(r"...", "w") as f:
        f.write("".join(sorted(lines, key=lambda x: re.sub(r"[#\s]+", "", x.lower()))))
