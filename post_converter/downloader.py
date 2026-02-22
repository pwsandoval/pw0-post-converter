import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from typing import List, Dict, Tuple, Any

def fetch_url(url: str) -> str:
    """Fetches key content from a URL."""
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text

def html_to_blocks(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Heuristic extraction of Code and Markdown blocks from soup.
    We look for a main content container and then iterate elements.
    """
    # Potential content selectors
    selectors = [
        'article',
        '.post-content',
        '.entry-content',
        'main',
        '.content',
        '#content'
    ]
    
    content_node = None
    for sel in selectors:
        content_node = soup.select_one(sel)
        if content_node:
            break
            
    if not content_node:
        # Fallback: body
        content_node = soup.body

    blocks = []
    current_md = []

    def flush_md():
        if current_md:
            text = "\n\n".join(current_md).strip()
            if text:
                blocks.append({'type': 'markdown', 'content': text, 'language': None})
            current_md.clear()

    # Recursive logic or flat iteration?
    # Flat iteration over direct children is often safest for blogs
    # but sometimes content is wrapped.
    # Let's try to identify 'pre' tags specifically.
    
    # We will traverse ALL descendants. If we hit a PRE, we handle it as code.
    # If we hit text/other, we accumulate text.
    # NOTE: This is tricky because PREs are inside other tags.
    # Simpler: Iterate over all elements. If element is PRE, it's code.
    # BUT we need to preserve order.
    
    # Improved approach:
    # 1. Convert the entire content_node to a string.
    # 2. Use a library like `markdownify`? 
    # Since I cannot install new libs easily without editing pyproject and waiting, 
    # I will try to use a "chunks" approach with BS4 if possible.
    
    # Iterating top-level children of the article is usually the structure for blogs.
    for child in content_node.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:
                current_md.append(text)
            continue
            
        if isinstance(child, Tag):
            # Check if it is a code block
            if child.name == 'pre':
                flush_md()
                # code often in <code class="language-xyz"> inside pre
                code_tag = child.find('code')
                if code_tag:
                    # check class for language
                    classes = code_tag.get('class', [])
                    lang = 'text'
                    for c in classes:
                        if c.startswith('language-'):
                            lang = c.replace('language-', '')
                            break
                    blocks.append({
                        'type': 'code', 
                        'content': code_tag.get_text(), 
                        'language': lang
                    })
                else:
                    blocks.append({
                        'type': 'code', 
                        'content': child.get_text(), 
                        'language': 'text'
                    })
            elif child.name in ['div', 'section'] and child.find('pre'):
                # Recursive handle? Or just simple text extraction?
                # If a div contains pre, we might want to recurse?
                # For now, treat as text to avoid complexity, 
                # or let the user know this limitation. A generic HTML->MD is complex.
                # Simplest fallback for a CLI:
                # "Please provide local Markdown or ensuring site structure is simple".
                # But I'll try to extract text.
                current_md.append(child.get_text(separator='\n\n'))
            else:
                # Headers, paragraphs, etc.
                # Get text with some structure
                text = child.get_text(separator=' ')
                # Add basic markdown formatting for headers?
                if child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    level = int(child.name[1])
                    text = f"{'#' * level} {text}"
                current_md.append(text)

    flush_md()
    return blocks

def parse_url(url: str) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
    html = fetch_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Metadata extraction
    title = soup.title.string if soup.title else "Untitled"
    metadata = {'title': title, 'url': url}
    
    blocks = html_to_blocks(soup)
    return blocks, metadata
