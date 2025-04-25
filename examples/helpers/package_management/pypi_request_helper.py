"""
This module offers helper functions for requesting PyPI to obtain information about packages.
"""
import re
import requests
from typing import Tuple, Any

from helpers.logger_helper import NoOpLogger
from helpers.proxy import set_default_proxy_and_ssl_certificates


BASE_URL = "https://pypi.org/pypi/"
REQUIREMENTS_PATTERN = re.compile(r"(?:(\S+)==(\S+)|(?!\S+==\S+)(\S+)).*")


def write_package_info_to_file(
    input_file_path: str = "requirements.txt",
    output_file_path: str = "requirements_info.txt",
    logger: Any = NoOpLogger(),
) -> None:
    """
    Collects the information about packages
    using requests to PyPI and save it in file.
    Args:
        input_file_path: file where packages are listed
        output_file_path: file where the information is collected
        logger: logger
    """
    set_default_proxy_and_ssl_certificates()

    # Clean up output_file_path before appending info
    open(output_file_path, "w").close()

    with open(input_file_path, "r") as input_file:
        for line in input_file:
            if not line.lstrip().startswith("#"):
                match = REQUIREMENTS_PATTERN.match(line)
                if match:
                    match_group1 = match.group(1)
                    match_group2 = match.group(2)
                    match_group3 = match.group(3)
                    if match_group1:
                        package_name = match_group1
                        logger.info(f"PACKAGE: {package_name}")
                        package_version = match_group2
                        logger.info(f"VERSION: {package_version}")
                    elif match_group3:
                        package_name = match_group3
                        logger.info(f"PACKAGE: {package_name}")
                        package_version = None
                        logger.info("VERSION: No version specified")

                    json, url = _get_json(
                        package_name,
                        package_version,
                        logger,
                    )

                    with open(output_file_path, "a", encoding="utf-8") as output_file:
                        json_info = json.get("info")

                        package_name_row = f"PACKAGE: {json_info.get('name')}"
                        output_file.write(package_name_row + "\n")
                        logger.info(package_name_row)

                        package_version_row = f"VERSION: {json_info.get('version')}"
                        output_file.write(package_version_row + "\n")
                        logger.info(package_version_row)

                        request_url_row = f"REQUEST: {url}"
                        output_file.write(request_url_row + "\n")
                        logger.info(request_url_row)

                        home_page_url_row = (
                            f"HOME_PAGE_URL: {json_info.get('home_page') or None}"
                        )
                        output_file.write(home_page_url_row + "\n")
                        logger.info(home_page_url_row)

                        json_info_project_urls = json_info.get("project_urls") or {
                            "Repository": None
                        }
                        json_info_project_url_repository = json_info_project_urls.get(
                            "Repository"
                        )
                        repository_url_row = (
                            f"REPOSITORY: {json_info_project_url_repository}"
                        )
                        output_file.write(repository_url_row + "\n")
                        logger.info(repository_url_row)

                        release_url_row = (
                            f"RELEASE_URL: {json_info.get('release_url') or None}"
                        )
                        output_file.write(release_url_row + "\n")
                        logger.info(release_url_row)

                        requires_python_row = f"REQUIRES_PYTHON: {json_info.get('requires_python') or None}"
                        output_file.write(requires_python_row + "\n")
                        logger.info(requires_python_row)

                        license_row = f"LICENSE: {json_info.get('license') or None}"
                        output_file.write(license_row + "\n")
                        logger.info(license_row)

                        summary_row = f"SUMMARY: {json_info.get('summary') or None}"
                        output_file.write(summary_row + "\n")
                        logger.info(summary_row)

                        vulnerabilities_row = "VULNERABILITIES:"
                        vuls = json.get("vulnerabilities", [])
                        if vuls:
                            vulnerabilities_row += (
                                vulnerabilities_row + "\n" + "\t\n".join(vuls)
                            )
                        else:
                            vulnerabilities_row += " None"

                        output_file.write(vulnerabilities_row + "\n")
                        logger.info(vulnerabilities_row)
                        output_file.write("\n")
                        logger.info("- " * 50)

                else:
                    logger.info(f"Not a package: `{repr(line)}`")
            else:
                logger.info(f"Not a package: `{repr(line)}`")


def _get_json(
    package: str,
    version: str = None,
    logger: Any = NoOpLogger(),
) -> Tuple[dict, str]:
    """
    Requests PyPI to obtain package's json.
    Args:
        package: package's name
        version: package's version
        logger: logger
    Returns:
        (JSON dict, request URL)
    """
    url = BASE_URL + f"{package}/{version + '/' if version is not None else ''}json"
    logger.info(f"Requesting {url}...")
    json: dict = requests.get(url).json()
    return json, url


def _get_json_info(package: str, version: str = None) -> Tuple[dict, str]:
    """
    Requests PyPI to obtain package's json["info"].
    Args:
        package: package's name
        version: package's version
    Returns:
        (dict with info, request URL)
    """
    json, url = _get_json(package, version)
    info: dict = json["info"]
    return info, url


def _get_json_info_requires_dist(
    package: str, version: str = None
) -> Tuple[list[str], str]:
    """
    Requests PyPI to obtain json["info"]["requires_dist"].
    Args:
        package: package's name
        version: package's version
    Returns:
        (list with requirements, request URL)
    """
    info, url = _get_json_info(package, version)
    reqs = info["requires_dist"]
    return reqs, url


if __name__ == "__main__":
    from helpers.logger_helper import terminal_info_logger
    
    write_package_info_to_file(logger=terminal_info_logger)
