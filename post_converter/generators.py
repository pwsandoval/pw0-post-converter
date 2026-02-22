import nbformat as nbf
from typing import List, Dict, Any

def write_python_script(blocks: List[Dict[str, str]], metadata: Dict[str, Any], output_path: str):
    """Writes blocks to a .py file with VSCode cells."""
    lines = []
    
    # Header
    lines.append(f"# Title: {metadata.get('title', 'Converted Post')}")
    lines.append(f"# Generated from: {metadata.get('url', 'Local File')}")
    lines.append("")
    
    for block in blocks:
        if block['type'] == 'code':
            lines.append("# %%")
            lines.append(block['content'])
            lines.append("")
        else:
            # Markdown block
            # We can use # %% [markdown] to make it a markdown cell in VSCode
            lines.append("# %% [markdown]")
            content = block['content']
            # Comment each line
            for line in content.splitlines():
                lines.append(f"# {line}")
            lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))


def write_jupyter_notebook(blocks: List[Dict[str, str]], metadata: Dict[str, Any], output_path: str):
    """Writes blocks to a .ipynb file."""
    nb = nbf.v4.new_notebook()
    nb.metadata = {"title": metadata.get("title", "Converted Post")}
    
    # Add header cell
    header_md = f"# {metadata.get('title', 'Untitled')}\n\nGenerated from: {metadata.get('url', 'Local File')}"
    nb.cells.append(nbf.v4.new_markdown_cell(header_md))
    
    for block in blocks:
        if block['type'] == 'code':
            # Create a code cell
            cell = nbf.v4.new_code_cell(block['content'])
            nb.cells.append(cell)
        else:
            # Create a markdown cell
            cell = nbf.v4.new_markdown_cell(block['content'])
            nb.cells.append(cell)
            
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
