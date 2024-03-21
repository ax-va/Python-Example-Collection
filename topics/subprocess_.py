import subprocess

process = subprocess.run(["python", "--version"], capture_output=True, text=True)
output = process.stdout.rstrip()  # rstrip() to remove the newline
print(output)
# Python 3.11.0rc1
