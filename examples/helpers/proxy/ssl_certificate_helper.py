"""
This module offers helper functions for working with
SSL certificates for the company's proxy.
"""
import os
from pathlib import Path
from typing import Sequence, Any


from helpers.logger_helper.no_op_logger import NoOpLogger


def create_ssl_certificate_file(
    input_dir_paths: Sequence[str | Path] = None,
    output_file_path: str | Path = None,
    logger: Any = NoOpLogger(),
) -> str | Path:
    """
    Creates a file with the company's SSL certificates
    that are collected from intermediate and root certificate files.

    Args:
        input_dir_paths:
            paths to directories with SSL certificate files encoded in base64,
            by default `intermediate` and `root` subdirectories
            in the directory of this module
        output_file_path:
            path to the output file with collected SSL certificates,
            by default `.ssl_certificates.pem` in the directory of this module
        logger:
            logger, by default NoOpLogger() that does nothing
    """
    logger.info(f"Creating SSL certificate file...")

    if input_dir_paths is None:
        dir_path: Path = Path(__file__).resolve().parent
        input_dir_paths = (
            dir_path / "intermediate",
            dir_path / "root",
        )

    for input_dir_path in input_dir_paths:
        os.makedirs(input_dir_path, exist_ok=True)

    if output_file_path is None:
        dir_path: Path = Path(__file__).resolve().parent
        output_file_path = dir_path / ".ssl_certificate.pem"

    # Collect SSL certificates from input into list
    certificate_list = []
    for input_dir_path in input_dir_paths:
        for root, dirs, files in os.walk(input_dir_path):
            certificate_list.append(f"# {input_dir_path}\n")
            for file in files:
                if not file.startswith("#"):  # Ignore filenames starting with "#"
                    file_path: str = os.path.join(root, file)
                    logger.info(f"Handling: `{file_path}`...")
                    with open(file_path, "r") as f:
                        certificate_list.append(f"# {file_path}\n{f.read()}")

    # Transform the collected certificate list to text and save in file
    with open(output_file_path, "w") as f:
        f.write("\n".join(certificate_list))

    logger.info(f"SSL certificate file was created: `{output_file_path}`.")

    return output_file_path


def set_ssl_certificate_file(ssl_certificate_file_path: str | Path) -> None:
    """
    Sets the company's SSL certificates to the OS environment variables.

    Args:
        ssl_certificate_file_path: file with SSL certificates encoded in base64
    """
    # Check if the SSL certificate file exists
    if not Path(ssl_certificate_file_path).is_file():
        raise FileNotFoundError(
            f"SSL certificate file not found: `{ssl_certificate_file_path}`."
        )

    # Set environment variables to use the specified SSL certificate file
    os.environ["REQUESTS_CA_BUNDLE"] = str(ssl_certificate_file_path)
    os.environ["SSL_CERT_FILE"] = str(ssl_certificate_file_path)


def set_default_ssl_certificates() -> None:
    """
    Sets the company's SSL certificates to the OS environment variables
    using the `.ssl_certificates.pem` file in the directory of this module.

    """
    dir_path: Path = Path(__file__).resolve().parent
    # Construct the absolute path to the `ssl_certificates.pem` file
    ssl_certificate_file_path: Path = dir_path / ".ssl_certificates.pem"
    set_ssl_certificate_file(ssl_certificate_file_path)


if __name__ == "__main__":
    from helpers.logger_helper import terminal_info_logger
    
    create_ssl_certificate_file(logger=terminal_info_logger)
    
