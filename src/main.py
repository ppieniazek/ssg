from copy_static import copy_directory_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    copy_directory_recursive(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
