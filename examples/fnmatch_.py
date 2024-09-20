"""
See also:
https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch
"""
import fnmatch
import os

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.py'):
        print(file)
