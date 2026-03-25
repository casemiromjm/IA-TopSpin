# Changes default behaviour
_default:
    @just -l

# Run project with UV
run:
    @uv run main.py

# Check for linting errors
lint:
    @uv run ruff check .

# Automatically fix linting and sort imports
fix:
    @uv run ruff check . --fix

# Format the code
format:
    @uv run ruff format .

# Build Checkpoint 1 slides
[group: 'docs']
cp1:
    @typst compile docs/slides_cp1.typ
    @echo "Created Slides for CP1!"

