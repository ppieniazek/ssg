import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_block(self):
        md = """
This is _italic_ paragraph.

This is paragraph with **bolded** text.



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            blocks,
            [
                "This is _italic_ paragraph.",
                "This is paragraph with **bolded** text.",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraph(self):
        block = "This is a standard paragraph.\nIt can span multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "## This is a Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block_h6 = "###### Level 6"
        self.assertEqual(block_to_block_type(block_h6), BlockType.HEADING)
        # Test invalid heading (no space) - should be paragraph
        block_invalid = "#NoSpace"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)
        # Test invalid heading (too many #) - should be paragraph
        block_invalid2 = "####### Too Many Hashes"
        self.assertEqual(block_to_block_type(block_invalid2), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```python\ndef hello():\n  print('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        # Test code block without language hint
        block_no_hint = "```\nsome code\n```"
        self.assertEqual(block_to_block_type(block_no_hint), BlockType.CODE)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        # Test single item ordered list
        block_single = "1. Only one"
        self.assertEqual(block_to_block_type(block_single), BlockType.ORDERED_LIST)
        # Test invalid order - should be paragraph
        block_invalid = "1. First\n3. Third"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)
        # Test invalid format (no dot-space) - should be paragraph
        block_invalid2 = "1 First\n2 Second"
        self.assertEqual(block_to_block_type(block_invalid2), BlockType.PARAGRAPH)

    # Example tests for the other types (though only 4 were requested initially)
    def test_quote_block(self):
        block = "> This is a quote.\n> Spread across lines."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block_single = "> A single line quote"
        self.assertEqual(block_to_block_type(block_single), BlockType.QUOTE)
        # Test invalid quote (missing > on one line) - should be paragraph
        block_invalid = "> First line\nSecond line misses marker"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Item A\n- Item B"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block_single = "- Just one item"
        self.assertEqual(block_to_block_type(block_single), BlockType.UNORDERED_LIST)
        # Test invalid list (missing space) - should be paragraph
        block_invalid = "-Item A\n- Item B"
        self.assertEqual(block_to_block_type(block_invalid), BlockType.PARAGRAPH)
        # Test invalid list (mixed markers - although some parsers might allow)
        # According to strict rules, this should be paragraph
        block_mixed = "- Item A\n* Item B"
        self.assertEqual(block_to_block_type(block_mixed), BlockType.PARAGRAPH)

    # markdown to html nodes

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_md_to_html_heading_h1(self):
        md = """
# Heading 1

### Heading 3

Some text paragraph under H1.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading 3</h3><p>Some text paragraph under H1.</p></div>",
        )

    def test_md_to_html_quote(self):
        md = """
> This is a quote.
> It has **bold** text.

Another paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote. It has <b>bold</b> text.</blockquote><p>Another paragraph.</p></div>",
        )

    def test_md_to_html_unordered_list(self):
        md = """
- First item with `code`
- Second item _italic_
- Third item

Paragraph after list.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <code>code</code></li><li>Second item <i>italic</i></li><li>Third item</li></ul><p>Paragraph after list.</p></div>",
        )

    def test_md_to_html_ordered_list(self):
        md = """
1. One item **bold**
2. Two item `code`
3. Three item

Paragraph after list.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>One item <b>bold</b></li><li>Two item <code>code</code></li><li>Three item</li></ol><p>Paragraph after list.</p></div>",
        )
