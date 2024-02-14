"""
F:
|- dir1
   |- dir2
      |- file2.txt
   file1.txt
"""
import os

for root, dirs, files in os.walk(r"F:\dir1"):
    for file in files:
        print(root)
        print(dirs)
        print(file)
        print(os.path.join(root, file))
        print("-"*20)
# F:\dir1
# ['dir2']
# file1.txt
# F:\dir1\file1.txt
# --------------------
# F:\dir1\dir2
# []
# file2.txt
# F:\dir1\dir2\file2.txt
# --------------------
