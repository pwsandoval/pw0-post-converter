# Post Converter CLI

Convert Markdown blog posts (local files or URLs) into Python scripts and Jupyter Notebooks.

## Features
- Preserves Markdown structure and titles.
- Converts Python code blocks to executable cells (`# %%`).
- Supports local Markdown files (with frontmatter support).
- Supports downloading posts from URLs (extracts content).
- Generates both `.py` and `.ipynb` by default.
- Keeps original markdown files by default.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   # or with uv/ruff if preferred
   uv venv
   ```

2. Activate the environment:
   ```bash
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

```bash
# Process markdown files from a folder
post-converter process --input-dir ./content/posts --processed-dir ./processed

# Process recursively (default)
post-converter process -i ./content/posts -p ./processed --recursive

# Move source markdown files to output folder (optional)
post-converter process -i ./inputs -p ./processed --move-source

# Write execution log
post-converter process -i ./inputs -p ./processed --log-file ./processed/run.log
```

## Development

Run tests (install `pytest` first):
```bash
pytest
```
