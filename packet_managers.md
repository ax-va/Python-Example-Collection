- If you use Poetry:
```
[tool.poetry.dependencies]
python = "^3.10"

[tool.poetry.group.dev.dependencies]
ruff = "^0.6.9"
pytest = "^8.0"
```

Then install with:
```
poetry install --with dev
```

- If you use Hatch:
```
[tool.hatch.envs.default]
dependencies = [
  "ruff",
  "pytest",
]
```

- If you use PDM:
```
[tool.pdm.dependencies]
python = ">=3.10"

[tool.pdm.dev-dependencies]
dev = [
  "ruff",
  "pytest",
]
```

- If you use plain pyproject.toml + pip (no Poetry/PDM/Hatch):

There isn't a built-in way to separate dev dependencies. 
You usually create a `requirements-dev.txt`:
```
ruff
pytest
```
and install with:
```
$ pip install -r requirements-dev.txt
```
