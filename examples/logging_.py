"""
This example is based on:
- "Python How-To: 63 Techniques to Improve Your Python Code", Yong Cui, Manning Publications Co., 2023;
- https://docs.python.org/3/library/logging.handlers.html.
"""
import logging

# # # How monitor programs with logging

# bad way: multiple distinct loggers in multiple places
logger0_not_good = logging.Logger("task_app")
logger1_not_good = logging.Logger("task_app")
assert logger0_not_good is not logger1_not_good

# good way: a shared instance of the Logger class
logger0_good = logging.getLogger("task_app")
logger1_good = logging.getLogger("task_app")
assert logger0_good is logger1_good

# best practice / best way
logging.getLogger(__name__)

# # # Use files to store application events

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


# File handlers can log the records in a file.
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

# # # Add multiple handlers to the logger

# Stream handlers can log the records in an interactive console
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.warning("Just a random warning event.")

# Get the list of all the handlers of the logger
print(logger.handlers)
# [<FileHandler /home/delorian/PycharmProjects/Python-Topics-Cui-2023/logs/taskier.log (NOTSET)>, <StreamHandler <stderr> (NOTSET)>]

# Remove the handlers from the logger
logger.handlers = []
print(logger.handlers)
# []
print(logger.hasHandlers())
# False

# You can set multiple file handlers to a logger.

# Some notable handlers:
# - StreamHandler       sends events to the console;
# - FileHandler         saves events to a file;
# - SMTPHandler         sends events to an email address;
# - HTTPHandler         sends events to a web server;
# - QueueHandler        sends events to a different thread.

# More information about the logging handlers:
# https://docs.python.org/3/library/logging.handlers.html

# # # Save log records properly

# # # Categorize application events with levels

# The logging package has five levels
# (DEBUG, INFO, WARNING, ERROR, and CRITICAL)
# and a base level NOTSET with a numeric value of 0:

# Numeric values            Logging levels          Intended usages
# 10                        DEBUG                   for diagnosis of problems
# 20                        INFO                    informational for expected behaviors
# 30                        WARNING                 unexpected behaviors that can lead to errors
# 40                        ERROR                   errors in some functionalities
# 50                        CRITICAL                serious errors in core functionalities

# When we set a specific level of a logger, all logging records
# at this level or more serious will be captured by the logger

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
print(logger.level)
# 30
print(logging._levelToName[logger.level])
# WARNING


def logging_messages_all_levels():
    logger.critical("--Critical message")
    logger.error("--Error message")
    logger.warning("--Warning message")
    logger.info("--Info message")
    logger.debug("--Debug message")


logging_messages_all_levels()
# In the console:
# --Critical message
# --Error message
# --Warning message

# # # Set a handler’s level

# Set the logger’s level to DEBUG.
# The logger sends messages to a handler only if the level of logger is less than or equal to the level of handler.
logger.setLevel(logging.DEBUG)

handler_warning = logging.FileHandler("logs/taskier_warning.log")
# Add the handler at the WARNING level
handler_warning.setLevel(logging.WARNING)
logger.addHandler(handler_warning)

handler_critical = logging.FileHandler("logs/taskier_critical.log")
# Add the handler at the CRITICAL level
handler_critical.setLevel(logging.CRITICAL)
logger.addHandler(handler_critical)

logging_messages_all_levels()
# In the console:
# <empty>

# In taskier_warning.log:
# --Critical message
# --Error message
# --Warning message

# In taskier_critical.log:
# --Critical message

# # # Set formats to the handler

# Retrieve the logger and set the level
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Remove previously set handlers
logger.handlers = []

# Creates a formatter.
# The formatter uses % style instead of f-strings.
formatter = logging.Formatter("%(asctime)s [%(levelname)s] – %(name)s - %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
# Configures the handler with formatter
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def log_some_records():
    logger.info("App is starting")
    logger.error("Failed to save the task to the db")
    logger.info("Created a task by the user")
    logger.critical("Cannot update the status of the task")


log_some_records()
# 2023-09-22 06:50:25,472 [INFO] – __main__ - App is starting
# 2023-09-22 06:50:25,472 [ERROR] – __main__ - Failed to save the task to the db
# 2023-09-22 06:50:25,472 [INFO] – __main__ - Created a task by the user
# 2023-09-22 06:50:25,472 [CRITICAL] – __main__ - Cannot update the status of the task

# Always format the log records to make it easier to locate pertinent problems
