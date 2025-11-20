from textnode import TextNode
from textnode import TextType

from directory_copy import directory_copy

SOURCE = "/home/matthew/Projects/BootDev/sitegen/static"
DEST = "/home/matthew/Projects/BootDev/sitegen/public"


def main():
    directory_copy(SOURCE, DEST)


if __name__ == "__main__":
    main()
