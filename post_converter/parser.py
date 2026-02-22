import re
import frontmatter
from typing import List, Dict, Any, Tuple

def extract_blocks_from_markdown(content: str) -> List[Dict[str, str]]:
    """
    Parses Markdown content and extracts blocks of Markdown and Code.
    
    Returns a list of dicts: {'type': 'code'|'markdown', 'language': str|None, 'content': str}
    """
    # Pattern to match fenced code blocks:
    # ^```(optional_lang)\n(content)\n```
    # We use non-greedy matching.
    pattern = re.compile(r'^```(\w*)\n(.*?)\n```', re.MULTILINE | re.DOTALL)
    
    blocks = []
    last_pos = 0
    
    for match in pattern.finditer(content):
        # Text before the code block
        md_text = content[last_pos:match.start()].strip()
        if md_text:
            blocks.append({
                'type': 'markdown',
                'content': md_text,
                'language': None
            })
            
        # The code block
        lang = match.group(1).strip().lower()
        code = match.group(2)
        blocks.append({
            'type': 'code',
            'content': code,
            'language': lang if lang else 'text'
        })
        
        last_pos = match.end()
        
    # Remaining text
    final_text = content[last_pos:].strip()
    if final_text:
        blocks.append({
            'type': 'markdown',
            'content': final_text,
            'language': None
        })
        
    return blocks

def parse_file(path: str) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
    """Reads a local file and parses it."""
    with open(path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    blocks = extract_blocks_from_markdown(post.content)
    return blocks, post.metadata
