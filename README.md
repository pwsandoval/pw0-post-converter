# Post Converter CLI

Convert your Markdown blog posts (local files or URLs) into VSCode-ready Python scripts and Jupyter Notebooks.

## Features
- Preserves Markdown structure and titles.
- Converts Python code blocks to executable cells (`# %%`).
- Supports local Markdown files (with frontmatter support).
- Supports downloading posts from URLs (extracts content).
- Generates both `.py` and `.ipynb` by default.

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
# Convert a local file
post-converter my-post.md

# Convert directly from a URL
post-converter --url https://pw0.dev/posts/spark-101/delta-storage-layout-basics/

# Specify output directory
post-converter my-post.md --out-dir ./notebooks

# Only generate Python script
post-converter my-post.md --no-ipynb
```

## Development

Run tests (install `pytest` first):
```bash
pytest
```
