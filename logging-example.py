"""
This example is based on the book:
"Python How-To: 63 Techniques to Improve Your Python Code",
Yong Cui, Manning Publications Co., 2023
"""
import logging

# # # logging and execution handling

# bad way: multiple distinct loggers in multiple places
logger0_not_good = logging.Logger("task_app")
logger1_not_good = logging.Logger("task_app")
assert logger0_not_good is not logger1_not_good

# good way: a shared instance of the Logger class
logger0_good = logging.getLogger("task_app")
logger1_good = logging.getLogger("task_app")
assert logger0_good is logger1_good

# best practice
logging.getLogger(__name__)

# # # using files to store application events


def check_log_content(filename):
    with open(filename) as file:
        return file.read()


class Task:
    def __init__(self, title):
        self.title = title

    def remove_from_db(self):
        # operations to remove the task from the database
        task_removed = True
        return task_removed


# File handlers can log the records in an interactive console.
# Specifies the file handler.
file_handler = logging.FileHandler("logs/taskier.log")
logger = logging.getLogger(__name__)
# Adds the handler to the logger.
logger.addHandler(file_handler)
# Check whether the logger has a handler
print(logger.hasHandlers())
# True

task = Task("Laundry")
if task.remove_from_db():
    logger.warning(f"removed the task {task.title} from the database")

# log_records = check_log_content("logs/taskier.log")
# print(log_records)

# # # adding multiple handlers to the logger

# Stream handlers can log the records in an interactive console
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.warning("Just a random warning event.")

# Get the list of all the handlers of the logger
print(logger.handlers)
# [<FileHandler /home/delorian/PycharmProjects/Python-Topics-Cui-2023/logs/taskier.log (NOTSET)>, <StreamHandler <stderr> (NOTSET)>]

logger.handlers = []
print(logger.handlers)
# []
print(logger.hasHandlers())
# False

# You can set multiple file handlers to a logger.

# More information about the handlers: http://mng.bz/E0pD

# Some notable handlers:
# - StreamHandler       sends events to the console;
# - FileHandler         saves events to a file;
# - SMTPHandler         sends events to an email address;
# - HTTPHandler         sends events to a web server;
# - QueueHandler        sends events to a different thread.
