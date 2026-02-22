from post_converter.parser import extract_blocks_from_markdown

def test_extract_blocks_simple():
    raw_body = """# Header
Some text.

```python
print("code")
```

More text.
"""
    blocks = extract_blocks_from_markdown(raw_body)
    assert len(blocks) == 3
    assert blocks[0]['type'] == 'markdown'
    assert "Header" in blocks[0]['content']
    assert blocks[1]['type'] == 'code'
    assert blocks[1]['content'].strip() == 'print("code")'
    assert blocks[2]['type'] == 'markdown'
    assert "More text" in blocks[2]['content']

def test_extract_blocks_multiple_codes():
    raw_body = """
```python
code1
```
text
```bash
code2
```
"""
    blocks = extract_blocks_from_markdown(raw_body.strip())
    assert len(blocks) == 3
    assert blocks[0]['type'] == 'code'
    assert blocks[0]['content'].strip() == 'code1'
    assert blocks[1]['type'] == 'markdown'
    assert blocks[1]['content'].strip() == 'text'
    assert blocks[2]['type'] == 'code'
    assert blocks[2]['content'].strip() == 'code2'
