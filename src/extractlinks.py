import re
from textnode import TextType, TextNode

# Find text items of the form '[link text](linkURL)'
# Screens for invalid characters in URL
REGEX_MARKDOWN_LINK = r'(?<!!)\[([^\[\]]+)\]\(([^"()\s{}<>|\\`[\]]+)\)'
# Find text items of the form '![alt text](linkToImage)'
REGEX_MARKDOWN_IMG = r'!\[([^[\]]+)\]\(([^"()\s{}<>|\\`[\]]+)\)'

# Tag representing regex matches which have been removed from a substrings
# used for splitting substrings
REMOVED_MD = "<R>"


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(REGEX_MARKDOWN_IMG, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(REGEX_MARKDOWN_LINK, text)
    return matches


def split_nodes_image(
    old_nodes: list[TextNode],
) -> list[TextNode]:
    new_nodes = []
    for current_node in old_nodes:
        # Pass on TextNodes of incorrect TextType
        if current_node.type != TextType.TEXT:
            new_nodes.append(current_node)
            continue

        current_img_nodes = extract_markdown_images(current_node.text)
        img_idx = 0

        # Pass on node with no img markdown tags
        if not current_img_nodes:
            new_nodes.append(current_node)
            continue

        # Passing on count from re.subn as we have already verified images exist
        no_images_string, _ = re.subn(REGEX_MARKDOWN_IMG, REMOVED_MD, current_node.text)
        substrings = no_images_string.split(REMOVED_MD)
        inserted_text = False  # Did we just insert a standard text node?

        for current_substring in substrings:
            if current_substring == "":  # Next insert should be image
                inserted_text = True
                continue
            if inserted_text:
                alt_text = current_img_nodes[img_idx][0]
                url = current_img_nodes[img_idx][1]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                img_idx += 1

            new_nodes.append(TextNode(current_substring, TextType.TEXT))
            inserted_text = True

        # Could have an extra image node left over
        if img_idx < len(current_img_nodes):
            alt_text = current_img_nodes[img_idx][0]
            url = current_img_nodes[img_idx][1]
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

    return new_nodes


def split_nodes_link(
    old_nodes: list[TextNode],
) -> list[TextNode]:
    new_nodes = []
    for current_node in old_nodes:
        # Pass on TextNodes of incorrect TextType
        if current_node.type != TextType.TEXT:
            new_nodes.append(current_node)
            continue

        current_link_nodes = extract_markdown_links(current_node.text)
        img_idx = 0

        # Pass on node with no img markdown tags
        if not current_link_nodes:
            new_nodes.append(current_node)
            continue

        # Passing on count from re.subn as we have already verified images exist
        no_links_string, _ = re.subn(REGEX_MARKDOWN_LINK, REMOVED_MD, current_node.text)
        substrings = no_links_string.split(REMOVED_MD)
        inserted_text = False  # Did we just insert a standard text node?

        for current_substring in substrings:
            if current_substring == "":  # Next insert should be image
                inserted_text = True
                continue
            if inserted_text:
                anchor_text = current_link_nodes[img_idx][0]
                url = current_link_nodes[img_idx][1]
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                img_idx += 1

            new_nodes.append(TextNode(current_substring, TextType.TEXT))
            inserted_text = True

        # Could have an extra link node left over
        if img_idx < len(current_link_nodes):
            alt_text = current_link_nodes[img_idx][0]
            url = current_link_nodes[img_idx][1]
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))

    return new_nodes
