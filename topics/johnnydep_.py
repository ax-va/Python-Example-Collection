"""
Save package's dependencies in a file and read
the file for getting the Python list of dependencies
"""
import johnnydep.cli

with open("deps.txt", "w") as file:
    johnnydep.cli.main(argv=["pandas==2.2.0", "-o" "pinned", "-v" "0"], stdout=file)

deps = []
with open("deps.txt", "r") as file:
    for line in file:
        line = line[:-1]
        name, version = line.split("==")  # --output-format pinned
        deps.append((name, version))

print(deps)
"[('pandas', '2.2.0'), ('numpy', '1.26.4'), ('python-dateutil', '2.8.2'), ('pytz', '2024.1'), ('tzdata', '2024.1'), ('six', '1.16.0')]"
