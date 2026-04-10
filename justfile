# Changes default behaviour
_default:
    @just -l

# Run GUI version of our project with UV
[group: 'build']
run:
    @uv run main.py

# Run CLI version of our project
[group: 'build']
cli size difficulty algorithm:
    @uv run solve.py --size {{size}} --board {{difficulty}} --algo {{algorithm}}

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

# Build Checkpoint 1 slides
[group: 'docs']
cp1:
    @typst compile docs/slides_cp1.typ
    @echo "Created Slides for CP1!"

