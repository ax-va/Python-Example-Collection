import logging
import sys

terminal_info_logger = logging.getLogger(__name__)
terminal_handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
terminal_handler.setFormatter(formatter)
terminal_info_logger.addHandler(terminal_handler)
terminal_info_logger.setLevel(logging.INFO)
