# Python-Example-Collection

## Install using `pip`

Create a virtual environment, activate it on POSIX systems, and install a package
```unix
$ python3 -m venv venv_name
$ source venv_name/bin/activate
(venv_name) $ pip install pytest
```
or using `virtualenv`
```unix
$ python3 -m pip install virtualenv
$ python3 -m virtualenv venv_name
$ source venv_name/bin/activate
(venv_name) $ pip install pytest
```
Deactivate the venv
```unix
(venv_name) $ deactivate
```
Create a virtual environment, activate it on Windows systems, and install `pytest`
```windows
C:\> python -m venv venv_name
C:\> venv_name\Scripts\activate.bat
(venv_name) C:\> pip install pytest
```
Activate in PowerShell
```windows
C:>venv_name\Scripts\Activate.ps1
```

## johnnydep
```ubuntu
$ johnnydep pandas==2.2.0 --verbose 0
```
