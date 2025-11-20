import os
from directory_copy import directory_copy
from extract_title import extract_title
from md_to_html import markdown_to_html

SRC_CONTENT_DIR = "/home/matthew/Projects/BootDev/sitegen/static"
SRC_MARKDOWN_DIR = "/home/matthew/Projects/BootDev/sitegen/content"
SRC_TEMPLATE_DIR = "/home/matthew/Projects/BootDev/sitegen"
DEST_CONTENT_DIR = "/home/matthew/Projects/BootDev/sitegen/public"

TITLE_STR = "{{ Title }}"
CONTENT_STR = "{{ Content }}"

FILE_MARKDOWN = "index.md"
FILE_TEMPLATE = "template.html"
FILE_OUTPUT = "index.html"


def generate_page(from_path: str, template_path: str, dest_path: str):
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

    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    out_file = os.path.join(dest_path, FILE_OUTPUT)

    with open(out_file, "w") as f:
        f.write(new_page)

    return


def main():
    directory_copy(SRC_CONTENT_DIR, DEST_CONTENT_DIR)
    generate_page(SRC_MARKDOWN_DIR, SRC_TEMPLATE_DIR, DEST_CONTENT_DIR)


if __name__ == "__main__":
    main()
