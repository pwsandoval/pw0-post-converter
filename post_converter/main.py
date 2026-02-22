import typer
from pathlib import Path
from typing import Optional
from .parser import parse_file
from .downloader import parse_url
from .generators import write_python_script, write_jupyter_notebook

app = typer.Typer()

@app.command()
def process(
    input_dir: Path = typer.Option(Path("./inputs"), "--input-dir", "-i", help="Directory with MD files"),
    processed_dir: Path = typer.Option(Path("./processed"), "--processed-dir", "-p", help="Output directory"),
):
    """
    Process all Markdown files in the input directory and URLs in urls.txt.
    """
    if not input_dir.exists():
        typer.echo(f"Input directory {input_dir} does not exist.")
        raise typer.Exit(code=1)
        
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Process urls.txt if exists
    urls_file = input_dir / "urls.txt"
    if urls_file.exists():
        typer.echo("Processing urls.txt...")
        with open(urls_file, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if not url or url.startswith('#'):
                    continue
                try:
                    process_url(url, processed_dir)
                except Exception as e:
                    typer.echo(f"Failed to process {url}: {e}")
    
    # Process MD files
    for md_file in input_dir.glob("*.md"):
        try:
            process_file(md_file, processed_dir)
        except Exception as e:
            typer.echo(f"Failed to process {md_file}: {e}")

def process_url(url: str, output_base: Path):
    blocks, metadata = parse_url(url)
    title = metadata.get('title', 'output')
    safe_name = sanitize_filename(title)
    
    # Create project folder in processed
    project_dir = output_base / safe_name
    project_dir.mkdir(exist_ok=True)
    
    # Save content
    write_python_script(blocks, metadata, str(project_dir / f"{safe_name}.py"))
    write_jupyter_notebook(blocks, metadata, str(project_dir / f"{safe_name}.ipynb"))
    
    # Save a reference file just in case? Or just log.
    typer.echo(f"Processed URL: {url} -> {project_dir}")

def process_file(file_path: Path, output_base: Path):
    blocks, metadata = parse_file(str(file_path))
    
    # Determine folder name
    # If title in metadata, use it, else filename stem
    title = metadata.get('title', file_path.stem)
    safe_name = sanitize_filename(title)
    
    project_dir = output_base / safe_name
    project_dir.mkdir(exist_ok=True)
    
    # Generate outputs
    write_python_script(blocks, metadata, str(project_dir / f"{safe_name}.py"))
    write_jupyter_notebook(blocks, metadata, str(project_dir / f"{safe_name}.ipynb"))
    
    # Move source file
    dest_file = project_dir / file_path.name
    # Handle overwrite
    if dest_file.exists():
        dest_file.unlink()
    file_path.rename(dest_file)
    
    typer.echo(f"Processed File: {file_path.name} -> {project_dir}")

def sanitize_filename(name: str) -> str:
    name = name.lower().replace(' ', '-')
    return "".join([c for c in name if c.isalnum() or c in ('-', '_')]) or "output"


if __name__ == "__main__":
    app()
