# Python-Example-Collection

## Install using `pip`

As of Python 3.3, the build-in `venv` package created a virtual environment
`python -m venv env_dir_name [--prompt my_proj]`.
The `--prompt` parameter is optional. If it is not supplied, the prompt will match the directory name.
As of Python 3.9, providing `--prompt .` will tell `venv` to use the parent directory as the prompt.

See also: https://docs.python.org/3/library/venv.html

Create a virtual environment, activate it on POSIX systems, and install a package
```unix
$ python3 -m venv venv_name
$ source venv_name/bin/activate
(venv_name) ...$ pip install pytest
```
or using `virtualenv`
```unix
$ python3 -m pip install virtualenv
$ python3 -m virtualenv venv_name
$ source venv_name/bin/activate
(venv_name) ...$ pip install pytest
```
Deactivate the venv
```unix
(venv_name) ...$ deactivate
```
Create a virtual environment, activate it on Windows systems, and install `pytest`
```windows
>python -m venv venv_name
>venv_name\Scripts\activate.bat
(venv_name) ...> pip install pytest
```
Activate in PowerShell
```windows
>venv_name\Scripts\Activate.ps1
```

## Install a local package

Install a local pacḱage located in the current directory
```unix
$ pip install ./my_package
```

## Install packages in editable mode

Editable mode refers to a way of installing a Python package such that any changes 
you make to the source code are immediately reflected without needing to reinstall the package.

Install in editable mode from the current directory
```unix
(venv_editable) ...$ pip install -e .
```

Install in editable mode with optional dependencies for testing
```unix
(venv_editable) ...$ pip install -e "./cards_proj_failed/[test]"
```
`[test]` in the `-e` parameters refers to optional dependencies for testing given in `pyproject.toml`.

## Other installation capabilities

Install from GitHub
```unix
$ pip install git+https://github.com/okken/pytest-skip-slow
```

Specify a version to install
```unix
$ pip install git+https://github.com/pytest-dev/pytest-cov@v2.12.1
```

Specify a branch to install
```unix
$ pip install git+https://github.com/pytest-dev/pytest-cov@master
```

Install from `.whl`
```unix
$ pip install <package> --no-index --find-links=<path/to/packages>
```

Download a bunch of various versions into a local cache of packages, 
and then point `pip` there instead of PyPI to install them into virtual environments later.
This is great for situations like running `tox` or CI test suites without needing to grab packages from PyPI.

```unix
(venv) ...$ mkdir ~/.pipcache
(venv) ...$ pip download -d ~/pipcache pytest
...
(venv) ...$ pip install --no-index --find-links=~/pipcache pytest
```

See also: https://pip.pypa.io/en/stable/

## Publish packages to PyPI

https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives

https://flit.pypa.io/en/latest/upload.html#controlling-package-uploads

## johnnydep
```unix
$ johnnydep pandas==2.2.0 --verbose 0
```
