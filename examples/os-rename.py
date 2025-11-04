import os

dir = r"..."

# `os.listdir(dir)` returns all entries inside `dir`:
# files, directories, symlinks, etc. - without distinguishing between them.

for entry in os.listdir(dir):
    entry_path = os.path.join(dir, entry)
    if os.path.isfile(entry_path):
        os.rename(entry_path, entry_path.replace("old_name", "new_name"))
