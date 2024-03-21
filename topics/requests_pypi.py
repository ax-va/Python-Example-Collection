"""
Make requests to PyPI to obtain information about packages.
"""
import re
import requests
from typing import Tuple
from pprint import pprint

BASE_URL = "https://pypi.org/pypi/"
PACKAGE_PATTERN = re.compile(r'(?:(\S+)==(\S+)|(?!\S+==\S+)(\S+)).*')


def request_requires_dist(package: str, version: str = None) -> Tuple[list[str], str]:
    """
    Requests json["info"]["requires_dist"] in PyPI.
    Args:
        package: package's name
        version: package's version
    Returns:
        (list with requirements, request URL)
    """
    info, url = request_info(package, version)
    reqs = info["requires_dist"]
    return reqs, url


def request_info(package: str, version: str = None) -> Tuple[dict, str]:
    """
    Requests package's json["info"] in PyPI.
    Args:
        package: package's name
        version: package's version
    Returns:
        (dict with info, request URL)
    """
    json, url = request_json(package, version)
    info: dict = json["info"]
    return info, url


def request_json(package: str, version: str = None) -> Tuple[dict, str]:
    """
    Requests package's json in PyPI.
    Args:
        package: package's name
        version: package's version
    Returns:
        (JSON dict, request URL)
    """
    url = BASE_URL + f"{package}/{version + '/' if version is not None else ''}json"
    print(f"Requesting PyPI {url}...")
    json: dict = requests.get(url).json()
    return json, url


def collect_info(
        input_filename: str = "requirements.txt",
        output_filename: str = "pypi_info.txt",
) -> None:
    """
    Collects the information about packages using requests to PyPI.
    Args:
        input_filename: file where packages are listed
        output_filename: file where the information is collected
    """
    # Clean up output_filename before appending info
    open(output_filename, "w").close()

    with open(input_filename, "r") as input_file:
        for line in input_file:
            if not line.lstrip().startswith("#"):
                match = PACKAGE_PATTERN.match(line)
                if match:
                    match_group1 = match.group(1)
                    match_group2 = match.group(2)
                    match_group3 = match.group(3)
                    if match_group1:
                        package_name = match_group1
                        print("PACKAGE:", package_name)
                        package_version = match_group2
                        print("VERSION:", package_version)
                    elif match_group3:
                        package_name = match_group3
                        print("PACKAGE:", package_name)
                        package_version = None
                        print("VERSION:", "No version specified")

                    json, url = request_json(package_name, package_version)
                    print()

                    with open(output_filename, "a") as output_file:
                        json_info = json.get("info")
                        output_file.write(f"NAME: {json_info.get('name')}\n")
                        output_file.write(f"VERSION: {json_info.get('version')}\n")
                        output_file.write(f"REQUEST: {url}\n")
                        output_file.write(f"HOME_PAGE: {json_info.get('home_page')}\n")
                        json_info_project_urls = json_info.get('project_urls') or {'Repository': ''}
                        json_info_project_urls_repository = json_info_project_urls.get('Repository', '')
                        output_file.write(f"REPOSITORY: {json_info_project_urls_repository}\n")
                        output_file.write(f"RELEASE_URL: {json_info.get('release_url')}\n")
                        output_file.write(f"REQUIRES_PYTHON: {json_info.get('requires_python')}\n")
                        output_file.write(f"LICENSE: {json_info.get('license')}\n")
                        output_file.write(f"SUMMARY: {json_info.get('summary')}\n")
                        output_file.write("VULNERABILITIES:\n")
                        vuls = json.get("vulnerabilities", [])
                        for vul in vuls:
                            output_file.write(str(vul))
                        output_file.write("-"*50 + "\n")
                else:
                    raise ValueError(f"Incorrect format in '{input_filename}': {line}.")


if __name__ == "__main__":
    collect_info()

    requires_dist, _ = request_requires_dist("pandas", "2.2.0")
    pprint(requires_dist)
    """
    ['numpy<2,>=1.22.4; python_version < "3.11"',
     'numpy<2,>=1.23.2; python_version == "3.11"',
     'numpy<2,>=1.26.0; python_version >= "3.12"',
     'python-dateutil>=2.8.2',
     'pytz>=2020.1',
     'tzdata>=2022.7',
     'hypothesis>=6.46.1; extra == "test"',
     'pytest>=7.3.2; extra == "test"',
     'pytest-xdist>=2.2.0; extra == "test"',
     'bottleneck>=1.3.6; extra == "performance"',
     'numba>=0.56.4; extra == "performance"',
     'numexpr>=2.8.4; extra == "performance"',
     'scipy>=1.10.0; extra == "computation"',
     'xarray>=2022.12.0; extra == "computation"',
     'fsspec>=2022.11.0; extra == "fss"',
     's3fs>=2022.11.0; extra == "aws"',
     'gcsfs>=2022.11.0; extra == "gcp"',
     'pandas-gbq>=0.19.0; extra == "gcp"',
     'odfpy>=1.4.1; extra == "excel"',
     'openpyxl>=3.1.0; extra == "excel"',
     'python-calamine>=0.1.7; extra == "excel"',
     'pyxlsb>=1.0.10; extra == "excel"',
     'xlrd>=2.0.1; extra == "excel"',
     'xlsxwriter>=3.0.5; extra == "excel"',
     'pyarrow>=10.0.1; extra == "parquet"',
     'pyarrow>=10.0.1; extra == "feather"',
     'tables>=3.8.0; extra == "hdf5"',
     'pyreadstat>=1.2.0; extra == "spss"',
     'SQLAlchemy>=2.0.0; extra == "postgresql"',
     'psycopg2>=2.9.6; extra == "postgresql"',
     'adbc-driver-postgresql>=0.8.0; extra == "postgresql"',
     'SQLAlchemy>=2.0.0; extra == "mysql"',
     'pymysql>=1.0.2; extra == "mysql"',
     'SQLAlchemy>=2.0.0; extra == "sql-other"',
     'adbc-driver-postgresql>=0.8.0; extra == "sql-other"',
     'adbc-driver-sqlite>=0.8.0; extra == "sql-other"',
     'beautifulsoup4>=4.11.2; extra == "html"',
     'html5lib>=1.1; extra == "html"',
     'lxml>=4.9.2; extra == "html"',
     'lxml>=4.9.2; extra == "xml"',
     'matplotlib>=3.6.3; extra == "plot"',
     'jinja2>=3.1.2; extra == "output-formatting"',
     'tabulate>=0.9.0; extra == "output-formatting"',
     'PyQt5>=5.15.9; extra == "clipboard"',
     'qtpy>=2.3.0; extra == "clipboard"',
     'zstandard>=0.19.0; extra == "compression"',
     'dataframe-api-compat>=0.1.7; extra == "consortium-standard"',
     'adbc-driver-postgresql>=0.8.0; extra == "all"',
     'adbc-driver-sqlite>=0.8.0; extra == "all"',
     'beautifulsoup4>=4.11.2; extra == "all"',
     'bottleneck>=1.3.6; extra == "all"',
     'dataframe-api-compat>=0.1.7; extra == "all"',
     'fastparquet>=2022.12.0; extra == "all"',
     'fsspec>=2022.11.0; extra == "all"',
     'gcsfs>=2022.11.0; extra == "all"',
     'html5lib>=1.1; extra == "all"',
     'hypothesis>=6.46.1; extra == "all"',
     'jinja2>=3.1.2; extra == "all"',
     'lxml>=4.9.2; extra == "all"',
     'matplotlib>=3.6.3; extra == "all"',
     'numba>=0.56.4; extra == "all"',
     'numexpr>=2.8.4; extra == "all"',
     'odfpy>=1.4.1; extra == "all"',
     'openpyxl>=3.1.0; extra == "all"',
     'pandas-gbq>=0.19.0; extra == "all"',
     'psycopg2>=2.9.6; extra == "all"',
     'pyarrow>=10.0.1; extra == "all"',
     'pymysql>=1.0.2; extra == "all"',
     'PyQt5>=5.15.9; extra == "all"',
     'pyreadstat>=1.2.0; extra == "all"',
     'pytest>=7.3.2; extra == "all"',
     'pytest-xdist>=2.2.0; extra == "all"',
     'python-calamine>=0.1.7; extra == "all"',
     'pyxlsb>=1.0.10; extra == "all"',
     'qtpy>=2.3.0; extra == "all"',
     'scipy>=1.10.0; extra == "all"',
     's3fs>=2022.11.0; extra == "all"',
     'SQLAlchemy>=2.0.0; extra == "all"',
     'tables>=3.8.0; extra == "all"',
     'tabulate>=0.9.0; extra == "all"',
     'xarray>=2022.12.0; extra == "all"',
     'xlrd>=2.0.1; extra == "all"',
     'xlsxwriter>=3.0.5; extra == "all"',
     'zstandard>=0.19.0; extra == "all"']
    """