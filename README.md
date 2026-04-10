# Group A1_37 - Top Spin

![Static Badge](https://img.shields.io/badge/Python-3.12%2B-blue)

|Name                             |Student Number|
|---------------------------------|--------------|
| Casemiro Melo Jorge de Medeiros | 202301897    |
| Mariana Almeida Cabral          | 202405731    |
| Pedro Andrade Castro            | 202200044    |

## Useful tools

### Just

This is a tool similar to Makefile, but way more modern. The installation instructions can be found [here](https://github.com/casey/just?tab=readme-ov-file).

For checking the available commands run:
```sh
just
```

### uv

This is a tool for managing python projects (i.e. handling dependencies, virtual enviroments, python version for a specific project, etc.). The installation instructions can be found [here](https://docs.astral.sh/uv/).

## Running with said tools
For running the project:
```sh
# runs the project in GUI version
just gui

# runs the project in CLI version
just cli
```

If you do not feel comfortable using Just, but you have uv available:
```sh
# runs the project in GUI version
uv run main.py

# runs the project in CLI version
uv run solve.py
```

_**DISCLAIMER:** You can use the flag `--help` for better understanding the CLI_

## What should I do if none is available?

If you do not have access to said tools, you can use old _pip_ and manually manage the python virtual environment. Beware our project is meant to be runned on python 3.12+.

Creating and activating the venv:
```sh
python -m venv .venv
source .venv/bin/activate
```

Installing dependencies:
```sh
pip install -r requirements.txt
```

Running:
```sh
# runs GUI version
python3 main.py

# runs CLI version
python3 solve.py
```

_**DISCLAIMER:** You can use the flag `--help` for better understanding the CLI_
