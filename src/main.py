from copy_static import copy_directory_recursive
from generation import generate_page

# Paths
dir_path_static = "static"
dir_path_public = "public"
index_md_path = "content/index.md"
template_path = "template.html"
index_html_path = "public/index.html"


def main():
    copy_directory_recursive(dir_path_static, dir_path_public)

    generate_page(
        from_path=index_md_path, template_path=template_path, dest_path=index_html_path
    )


if __name__ == "__main__":
    main()
