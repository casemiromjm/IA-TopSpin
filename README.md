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

This is a tool for managing python projects (i.e. handling dependencies, virtual environments, python version for a specific project, etc.). The installation instructions can be found [here](https://docs.astral.sh/uv/).

## Running with said tools
For running the project:
```sh
# runs the project in GUI version
just gui

# runs the project in CLI version (size, board, algorithm, [heuristic])
just cli 10 easy bfs
just cli 10 hard:1 greedy adjacency
just cli 10 hard:1 astar adjacency
```

If you do not feel comfortable using Just, but you have uv available:
```sh
# runs the project in GUI version
uv run main.py

# runs the project in CLI version
uv run solve.py --size 10 --board easy --algo bfs
uv run solve.py --size 10 --board hard:1 --algo greedy --heuristic adjacency
uv run solve.py --size 10 --board hard:1 --algo astar --heuristic adjacency
```

_**DISCLAIMER:** You can use the flag `--help` for better understanding the CLI_

### CLI arguments

| Argument | Values |
|----------|--------|
| `--size` | `10`, `20` |
| `--board` | `random`, `easy`, `easy:2`, `medium`, `hard:1`, … |
| `--algo` | `bfs`, `dfs`, `ids`, `greedy`, `astar` |
| `--heuristic` | `adjacency`, `min_misplaced_slots` *(required for greedy / astar)* |

### In-game controls (GUI)

| Key / Button | Action |
|-------------|--------|
| `←` / `→` | Shift the ring left / right |
| `↑` or `R` | Rotate the spin window |
| `H` or "Get Hint" button | Request a hint (Greedy runs in the background) |
| `Q` | Return to the main menu |

## Compiling the slides

Requires [Typst](https://typst.app) — install with `brew install typst`.

```sh
just docs final   # final delivery slides → docs/slides_final.pdf
just docs cp1     # checkpoint 1 slides  → docs/slides_cp1.pdf
```

## What should I do if none of the tools are available?

If you do not have access to said tools, you can use old _pip_ and manually manage the python virtual environment. Beware our project is meant to be runned on python 3.12+.

<!-- First, generate `requirements.txt` (only needed once, requires uv):
```sh
just dependencies
# or: uv export --no-hashes --no-dev --format requirements-txt > requirements.txt
``` -->

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

_**DISCLAIMER:** You can use the flag `--help` for better understanding the CLI or check [this](#cli-arguments)_
