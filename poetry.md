1. Install Poetry (once on your system)

    Best practice is via pipx so it stays isolated:
    ```unix
    $ python -m pip install --user pipx
    $ pipx ensurepath
    $ pipx install poetry
    ```
    
    If you don't want pipx, you can also pip install `--user poetry`, but pipx is cleaner.

2. Initialize Poetry in your project

    From the root of your project (where `pyproject.toml` already exists):
    ```unix
    $ poetry init
    ```

    This asks a few questions about your project and creates a `[tool.poetry]` section in your `pyproject.toml`.

3. Declare Python version and dependencies

    Edit `pyproject.toml` and add something like:
    ```toml
    [tool.poetry.dependencies]
    python = "^3.12"
    
    [tool.poetry.group.dev.dependencies]
    pytest = "^8.0"
    ruff = "^0.12.0"
    ```

4. Install with Poetry

    Poetry will create its own virtualenv (separate from the one you manually made):
    ```unix
    $ poetry install --with dev
    ```
    
    Then use tools via:
    ```unix
    $ poetry run pytest
    $ poetry run ruff check
    ```

5. (Optional) Deactivate old venv

    Once Poetry manages everything, you don't need the old venv you created with `$ python -m venv`. You can delete it if you like.
    
    Poetry will now handle both your runtime and dev-only dependencies cleanly, and you can stop juggling pip install manually.
