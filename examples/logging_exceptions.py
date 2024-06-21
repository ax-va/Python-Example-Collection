import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# The output of the logger will be directed to stdout (the console)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    x = 10 / 0
except Exception as e:
    logger.error("Oh no, something wrong happened")
# 2024-03-17 16:03:28,056 - __main__ - ERROR - Oh no, something wrong happened

# If the module is imported, __main__ is replaced with the name of the module
