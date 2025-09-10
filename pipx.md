# pipx

## Summary

- **pipx is designed for Python programs (e.g., formatters, linters) that you run from the command line.** Each tool is installed into its own virtual environment. The tools are globally available, fully isolated, and free of conflicts.

- **According to the official Poetry documentation, pipx is a recommended way to install Poetry.** This installs Poetry as a standalone, globally available command-line application—cleanly isolated in a virtual environment—ideal for avoiding conflicts with other Python projects. pipx automatically creates its own virtual environment for Poetry, so you can use the `poetry` command system-wide without manually activating environments.

- **pipx is tied to the Python interpreter with which it was installed.** For every Python version you want to use as the base for pipx, you must either install pipx under that version as well, or choose a different interpreter when installing the app using `--python`:
    ```unix
    $ pipx install <package> --python <executable name, version number, or full path>
    ```
    
    e.g.,
    ```unix
    $ pipx install poetry --python 3.11.
    ```
    Either Python 3.11 must already be installed on the system, or you must use the `--fetch-missing-python` option, which will automatically download and use a standalone Python build if needed.

- **The default path for virtual environments on Windows** is typically `~\pipx\venvs`, e.g., `C:\Users\<User>\pipx\venvs`. `PIPX_HOME` defines the base directory, e.g., `PIPX_HOME=/path/to/dir`; in that case, the virtual environments end up under `PIPX_HOME/venvs`.

- **Install Poetry from the GitLab registry with pipx:**

    ```unix
    $ pipx install poetry \
      --index-url "https://__token__:<TOKEN>@gitlab.your_company.cloud/api/v4/projects/1792/packages/pypi/simple" \
      --pip-args="--proxy http://your_company_proxy --no-cache-dir" \
      --python 3.11   # optional
    ```
