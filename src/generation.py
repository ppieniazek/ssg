import os
import pathlib

from block_markdown import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md:
        markdown_content = md.read()

    with open(template_path, "r") as template:
        template_content = template.read()

    html_content_string = markdown_to_html_node(markdown_content).to_html()

    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content_string)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as html:
        html.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for item in os.listdir(dir_path_content):
        src_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_item_path):
            if item.endswith(".md"):
                dest_html_path = pathlib.Path(dest_item_path).with_suffix(".html")
                generate_page(src_item_path, template_path, str(dest_html_path))
        elif os.path.isdir(src_item_path):
            generate_pages_recursive(src_item_path, template_path, dest_item_path)
