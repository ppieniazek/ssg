import re

from textnode import TextNode, TextType


def text_to_text_nodes(text):
    delimiters = (("`", TextType.CODE), ("_", TextType.ITALIC), ("**", TextType.BOLD))

    starting_node = TextNode(text, TextType.TEXT)
    nodes = [starting_node]

    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    for split_func in split_nodes_link, split_nodes_image:
        nodes = split_func(nodes)

    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes_helper(old_nodes, TextType.IMAGE)


def split_nodes_link(old_nodes):
    return split_nodes_helper(old_nodes, TextType.LINK)


def split_nodes_helper(old_nodes, text_type: TextType):
    match text_type:
        case TextType.IMAGE:
            extract_func = extract_markdown_images
        case TextType.LINK:
            extract_func = extract_markdown_links
        case _:
            raise Exception("invalid node type")

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        matches = extract_func(old_node.text)
        if not matches:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        node_string = old_node.text

        for text, url in matches:
            match text_type:
                case TextType.IMAGE:
                    split_pattern = f"![{text}]({url})"
                case TextType.LINK:
                    split_pattern = f"[{text}]({url})"
                case _:
                    raise Exception("invalid node type")

            sections = node_string.split(split_pattern, 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0]:
                text_node = TextNode(sections[0], TextType.TEXT)
                split_nodes.append(text_node)

            node = TextNode(text, text_type, url)
            split_nodes.append(node)

            node_string = sections[1]

        if node_string:
            split_nodes.append(TextNode(node_string, TextType.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
