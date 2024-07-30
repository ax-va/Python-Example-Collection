"""
Save package's dependencies in a StringIO instance
and read it for getting the Python list of dependencies
"""
import io
import johnnydep.cli
from pprint import pprint

temp_io = io.StringIO()
johnnydep.cli.main(
    argv=["pandas==2.2.0", "-o" "pinned",],
    stdout=temp_io,
)

deps = []
# Change the cursor position
temp_io.seek(0)
for line in temp_io:
    line = line[:-1]
    name, version = line.split("==")  # --output-format pinned
    deps.append((name, version))

temp_io.close()

print(deps[0])
# ('pandas', '2.2.0')
pprint(deps[1:])
# [('numpy', '1.26.4'),
#  ('python-dateutil', '2.8.2'),
#  ('pytz', '2024.1'),
#  ('tzdata', '2024.1'),
#  ('six', '1.16.0')]

with open("deps.txt", "wt") as f:
    f.write("\n".join(f"{p}=={v}" for p, v in deps[1:]))
