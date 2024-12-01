import os

for filename in os.listdir("."):
    if os.path.isfile(filename):
        os.rename(filename, filename.replace("example-", ""))