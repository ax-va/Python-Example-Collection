#-*- conding: utf-8 -*-

# imports in 'my_imports_input/script1.py':
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import array, mean
from pandas import (
    DataFrame,
    Series,
)
from os import path

# imports in 'my_imports_input/__init__.py':
from . import script1
# import typing

# imports in 'my_imports_input/dir1/script2.py':
import pathlib

# imports in 'my_imports_input/dir1/__init__.py':
import script2
