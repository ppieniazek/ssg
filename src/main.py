from copy_static import copy_directory_recursive
from generation import generate_pages_recursive

# Paths
dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"
template_path = "template.html"


def main():
    print("Starting static site generation...")
    copy_directory_recursive(dir_path_static, dir_path_public)

    print(
        f"Generating pages from '{dir_path_content}' to '{dir_path_public}' using '{template_path}' template..."
    )
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
