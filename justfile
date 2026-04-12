# Changes default behaviour
_default:
    @just -l

# Run GUI version of our project with UV
[group: 'build']
gui:
    @uv run main.py


# Run CLI version of our project
[group: 'build']
cli size difficulty algorithm heuristic="":
    @HEURISTIC_FLAG=""; \
    if [ "{{algorithm}}" = "astar" ] || [ "{{algorithm}}" = "greedy" ] || [ "{{algorithm}}" = "weighted-astar" ]; then \
        if [ -z "{{heuristic}}" ]; then \
            echo "Error: Algorithm {{algorithm}} requires a heuristic."; \
            exit 1; \
        fi; \
        HEURISTIC_FLAG="--heuristic {{heuristic}}"; \
    fi; \
    uv run solve.py --size {{size}} --board {{difficulty}} --algo {{algorithm}} $HEURISTIC_FLAG

# List all premade boards
[group: 'dev']
boards:
    @uv run $root/src/premade.py

# Check for linting errors
[group: 'dev']
lint:
    @uv run ruff check .

# Automatically fix linting and sort imports
[group: 'dev']
fix:
    @uv run ruff check . --fix

# Format the code
[group: 'dev']
format:
    @uv run ruff format .

# Export project dependencies
[group: 'dev']
dependencies:
    @uv export --no-hashes --no-dev --format requirements-txt > requirements.txt

# Build slides
[group: 'docs']
docs deliver:
    @typst compile docs/slides_{{ lowercase(deliver) }}.typ

# Gather all performance related data
[group: 'analysis']
perf:
    @chmod +x analysis/scripts/performance.sh
    @./analysis/scripts/performance.sh
