@echo off

:: Create directories
mkdir app\api
mkdir config
mkdir tests
mkdir resources

:: Initialize Git submodule for X-Plane Connect
if not exist "resources\XPlaneConnect" (
    git submodule add https://github.com/nasa/XPlaneConnect.git resources\XPlaneConnect
    git submodule update --init --recursive
)

:: Create empty files
type nul > app\__init__.py
type nul > app\main.py
type nul > app\api\__init__.py
type nul > app\api\endpoints.py
type nul > config\config.json
type nul > tests\__init__.py
type nul > tests\test_endpoints.py

:: Create .gitignore if it doesn't exist
if not exist .gitignore (
    echo venv>>.gitignore
    echo __pycache__>>.gitignore
    echo *.pyc>>.gitignore
    echo *.pyo>>.gitignore
    echo *.pyd>>.gitignore
    echo *.pdb>>.gitignore
    echo *.egg>>.gitignore
    echo *.egg-info>>.gitignore
    echo .build>>.gitignore
    echo dist>>.gitignore
    echo *.spec>>.gitignore
    echo resources/XPlaneConnect/.git>>.gitignore
)

:: Create README.md if it doesn't exist
if not exist README.md (
    echo # XPWeb > README.md
    echo XPWeb: A REST API for interfacing with X-Plane via X-Plane Connect.>> README.md
)

echo Project structure created successfully.
