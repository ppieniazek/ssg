import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 header found in markdown content")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                node = paragraph_to_html_node(block)
            case BlockType.HEADING:
                node = heading_to_html_node(block)
            case BlockType.CODE:
                node = code_block_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                node = ulist_to_html_node(block)
            case BlockType.ORDERED_LIST:
                node = olist_to_html_node(block)
            case BlockType.QUOTE:
                node = quote_block_to_html_node(block)

            case _:
                raise Exception("Invalid block type")

        children_nodes.append(node)

    return ParentNode("div", children_nodes)


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = [text_node_to_html_node(node) for node in text_nodes]
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    content = " ".join(lines)
    children = text_to_children(content)
    return ParentNode("p", children)


def heading_to_html_node(block):
    match = re.match(r"^(#{1,6})\s(.*)", block)
    level = len(match.group(1))
    content = match.group(2).strip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)


def code_block_to_html_node(block):
    content = "\n".join(block.split("\n")[1:-1]) + "\n"
    code_text_node = TextNode(content, TextType.TEXT)
    code_html_node = LeafNode("code", code_text_node.text)
    return ParentNode("pre", [code_html_node])


def quote_block_to_html_node(block):
    lines = block.split("\n")
    processed_lines = [line.lstrip(">").lstrip() for line in lines]
    content = " ".join(processed_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        item_content = line.lstrip("- ")
        item_children = text_to_children(item_content)
        list_items.append(ParentNode("li", item_children))
    return ParentNode("ul", list_items)


def olist_to_html_node(block):
    lines = block.split("\n")
    list_items = []
    for i, line in enumerate(lines, 1):
        item_content = line.lstrip(f"{i}. ")
        item_children = text_to_children(item_content)
        list_items.append(ParentNode("li", item_children))
    return ParentNode("ol", list_items)


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block]
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6}\s", lines[0]):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    if not lines:  # Handle empty block case if necessary, though usually a paragraph
        is_ordered_list = False
    else:
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                is_ordered_list = False
                break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
