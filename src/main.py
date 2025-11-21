import sys
import os
from directory_copy import directory_copy
from extract_title import extract_title
from md_to_html import markdown_to_html

SRC_STATIC_DIR = "/home/matthew/Projects/BootDev/sitegen/static"
SRC_CONTENT_DIR = "/home/matthew/Projects/BootDev/sitegen/content"
SRC_PROJ_ROOT_DIR = "/home/matthew/Projects/BootDev/sitegen"
DEST_PUBLIC_DIR = "/home/matthew/Projects/BootDev/sitegen/docs"

TITLE_STR = "{{ Title }}"
CONTENT_STR = "{{ Content }}"

FILE_MARKDOWN = "index.md"
FILE_TEMPLATE = "template.html"
FILE_OUTPUT = "index.html"


def generate_pages_recursive(
    from_path: str, template_path: str, dest_path: str, base_path: str
):
    if not os.path.isdir(template_path):
        raise ValueError("Error: template_path must be a directory")
    template_file = os.path.join(template_path, FILE_TEMPLATE)

    if not os.path.exists(template_file):
        raise Exception(f"Error: file {FILE_TEMPLATE} not found at given path")
    with open(template_file, "r") as f:
        template = f.read()

    if TITLE_STR not in template or CONTENT_STR not in template:
        raise Exception("Error: Template does not have necessary fields")

    new_page = template

    if not os.path.isdir(from_path):
        raise ValueError("Error: from_path must be a directory")

    entries = os.listdir(from_path)
    for entry in entries:
        print(os.path.join(from_path, entry))
        if entry == FILE_MARKDOWN:
            from_file = os.path.join(from_path, FILE_MARKDOWN)
            if not os.path.isfile(from_file):
                continue  # Found a directory with the same name as FILE_MARKDOWN

            with open(from_file, "r") as f:
                markdown = f.read()

            html = markdown_to_html(markdown).to_html()
            title = extract_title(markdown)
            new_page = new_page.replace('href="/', f'href="{base_path}')
            new_page = new_page.replace('src="/', f'src="{base_path}')

            new_page = new_page.replace(TITLE_STR, title)
            new_page = new_page.replace(CONTENT_STR, html)

            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            out_file = os.path.join(dest_path, FILE_OUTPUT)

            with open(out_file, "w") as f:
                f.write(new_page)
        else:
            next_from = os.path.join(from_path, entry)
            next_dest = os.path.join(dest_path, entry)
            generate_pages_recursive(next_from, template_path, next_dest, base_path)

    return


def generate_page(from_path: str, template_path: str, dest_path: str, base_path: str):
    if not os.path.isdir(from_path):
        raise ValueError("Error: from_path must be a directory")
    from_file = os.path.join(from_path, FILE_MARKDOWN)

    if not os.path.exists(from_file):
        raise Exception(f"Error: file {FILE_MARKDOWN} not found at given from_path")
    with open(from_file, "r") as f:
        markdown = f.read()

    html = markdown_to_html(markdown).to_html()
    title = extract_title(markdown)

    if not os.path.isdir(template_path):
        raise ValueError("Error: template_path must be a directory")
    template_file = os.path.join(template_path, FILE_TEMPLATE)

    if not os.path.exists(template_file):
        raise Exception(f"Error: file {FILE_TEMPLATE} not found at given path")
    with open(template_file, "r") as f:
        template = f.read()

    if TITLE_STR not in template or CONTENT_STR not in template:
        raise Exception("Error: Template does not have necessary fields")
    new_page = template
    new_page = new_page.replace(TITLE_STR, title)
    new_page = new_page.replace(CONTENT_STR, html)
    new_page = new_page.replace('href="/', f'href="{base_path}')
    new_page = new_page.replace('src="/', f'src="{base_path}')

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    out_file = os.path.join(dest_path, FILE_OUTPUT)

    with open(out_file, "w") as f:
        f.write(new_page)

    return


def main(argv=sys.argv):
    base_path = "/"
    if len(argv) > 1:
        base_path = argv[1]

    directory_copy(SRC_STATIC_DIR, DEST_PUBLIC_DIR)
    # generate_page(SRC_CONTENT_DIR, SRC_PROJ_ROOT_DIR, DEST_PUBLIC_DIR)
    generate_pages_recursive(
        SRC_CONTENT_DIR, SRC_PROJ_ROOT_DIR, DEST_PUBLIC_DIR, base_path
    )


if __name__ == "__main__":
    main()
