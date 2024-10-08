import os
import re
import chardet

INPUT_DIR = r"my_imports_input"
OUTPUT_DIR = r"my_imports_output"
IMPORT_PATTERN = re.compile(
    r"([^\n]*from\s+\S+\s+import\s+\([^)]+\))"
    r"|([^\n]*from\s+\S+\s+import\s+[^\n]+)"
    r"|([^\n]*import\s[^\n]+)"
)

imports = ""
for root, dirs, files in os.walk(INPUT_DIR):
    for file in files:
        if file.endswith(".py"):
            filepath = os.path.join(root, file)
            print("filepath:", filepath)
            with open(filepath, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result["encoding"]

            with open(filepath, "r", encoding=encoding) as f:
                imports += "\n# imports in '" + filepath + "':\n"
                content = f.read()
                import_list = IMPORT_PATTERN.findall(content)
                for entry in import_list:
                    imports += ("".join(entry)).strip() + "\n"


with open(os.path.join(OUTPUT_DIR, "collected_imports.py"), "w", encoding="utf-8") as f:
    f.write("#-*- conding: utf-8 -*-\n" + imports)
