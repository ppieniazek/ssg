import sys

from copy_static import copy_directory_recursive
from generation import generate_pages_recursive

# Paths
dir_path_static = "static"
dir_path_output = "docs"
dir_path_content = "content"
template_path = "template.html"


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        if not basepath.startswith("/"):
            basepath = "/" + basepath
        if not basepath.endswith("/"):
            basepath += "/"

    if basepath == "//":
        basepath = "/"

    print("Starting static site generation with basepath: '{basepath}'")
    copy_directory_recursive(dir_path_static, dir_path_output)

    print(
        f"Generating pages from '{dir_path_content}' to '{dir_path_output}' using '{template_path}' template..."
    )
    generate_pages_recursive(dir_path_content, template_path, dir_path_output, basepath)
    print("Done!")


if __name__ == "__main__":
    main()
