import os
import re

INPUT_DIR = r"my_imports_input"
OUTPUT_DIR = r"my_imports_output"
IMPORT_PATTERN = re.compile(
    r"([^\n]*from\s+\S+\s+import\s+\([^)]+\))"
    r"|([^\n]*from\s+\S+\s+import\s+[^\n]+)"
    r"|([^\n]*import\s[^\n]+)"
)

text = """
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import array, mean
from pandas import (
    DataFrame,
    Series,
)

# some code
a = 1 + 2
print(a)
"""
IMPORT_PATTERN.findall(text)
# [('', '', 'import re'),
#  ('', '', 'import numpy as np'),
#  ('', '', 'import pandas as pd'),
#  ('', '', 'import matplotlib.pyplot as plt'),
#  ('', 'from numpy import array, mean', ''),
#  ('from pandas import (\n    DataFrame,\n    Series,\n)', '', '')]

imports = ""
for root, dirs, files in os.walk(INPUT_DIR):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                imports += "\n# imports in '" + filepath + "':\n"
                content = f.read()
                import_list = IMPORT_PATTERN.findall(content)
                for entry in import_list:
                    imports += "".join(entry) + "\n"


with open(os.path.join(OUTPUT_DIR, "collected_imports.py"), "w", encoding="utf-8") as f:
    f.write("#-*- conding: utf-8 -*-\n" + imports)
