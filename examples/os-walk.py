"""
dir1
|- dir2
   |- file2.txt
file1.txt
"""
import os

for root, dirs, files in os.walk("dir1"):
    print("root:", root)
    print("dirs:", dirs)
    print("files:", files)
    for file in files:
        print("relative filepath:", repr(os.path.join(root, file)))
    print("-" * 20)
"""
root: dir1
dirs: ['dir2']
files: ['file1.txt']
relative filepath: 'dir1\\file1.txt'
--------------------
root: dir1\dir2
dirs: []
files: ['file2.txt']
relative filepath: 'dir1\\dir2\\file2.txt'
--------------------
"""
