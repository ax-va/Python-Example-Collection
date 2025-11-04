import os

dir = r"..."

# `os.listdir(dir)` returns all entries inside dir:
# files, directories, symlinks, etc. - without distinguishing between them.

for l1_entry in os.listdir(dir):
    l1_entry_path = os.path.join(dir, l1_entry)
    print("l1_entry_path:", l1_entry_path)
    if os.path.isdir(l1_entry_path):
        for l2_entry in os.listdir(l1_entry_path):
            l2_entry_path = os.path.join(l1_entry_path, l2_entry)
            print("l2_entry_path:", l2_entry_path)
    print("-" * 20)
