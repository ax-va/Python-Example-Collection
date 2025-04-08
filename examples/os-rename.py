import os

# This script should be in the same directory as the `matplotlib-examples` subdirectory
directory = "./matplotlib-examples"

for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        os.rename(filepath, filepath.replace("example-", ""))