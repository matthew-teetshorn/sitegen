import regex
from textnode import TextType, TextNode
import itertools
import re_defs

# Tag representing regex matches which have been removed from a substrings
# used for splitting substrings
REMOVED_MD = "<R>"


def extract_markdown_images(text: str) -> list[tuple[str, str]] | None:
    matches = regex.findall(re_defs.REGEX_MARKDOWN_IMG, text)
    return matches


# Extracting links is more complicated than regex.findall()
# Links can contain matched pairs of parentheses which requires a recursive regex
# The recursive regex does not work with the static lead in '[link]' construction
# Therefore, they are broken down into two regex's that are scanned sequentially
#
# Function returns a tuple with the matched text, url, start_idx, end_idx of the matched regex
def extract_markdown_links(text: str) -> list[tuple[str, str, int, int]] | None:
    matches = []
    re_link_text = regex.compile(re_defs.REGEX_LINK_FRONT)
    re_link_url = regex.compile(re_defs.REGEX_LINK_URL)
    link_text = None
    link_url = None
    start = 0
    end = len(text)

    while start < end:
        match = re_link_text.search(text, start, end)
        if match is None:
            break
        else:
            link_text = match.group(1)
            s_idx, e_idx = match.span()
            # REGEX_MD_LINK_FRONT captures the following '(': go back one
            start = e_idx - 1
            match = re_link_url.search(text, start, end)

            if match is None:
                break
            _, e_idx = match.span()

            # if [link](url) are not directly next to one another continue
            link_url = match.group(1)
            matches.append((link_text, link_url, s_idx, e_idx))

            start = e_idx

    # matches = regex.findall(REGEX_MARKDOWN_LINK, text)
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

        # Pass on node with no img markdown tags
        if not current_img_nodes:
            new_nodes.append(current_node)
            continue

        # Passing on count from regex.subn as we have already verified images exist
        no_images_string, _ = regex.subn(
            re_defs.REGEX_MARKDOWN_IMG, REMOVED_MD, current_node.text
        )
        substrings = no_images_string.split(REMOVED_MD)

        zipped = list(
            itertools.chain.from_iterable(
                itertools.zip_longest(substrings, current_img_nodes, fillvalue="")
            )
        )
        for item in zipped:
            if type(item) is str:
                if item != "":
                    new_nodes.append(TextNode(item, TextType.TEXT))
            elif type(item) is tuple:
                alt_text = item[0]
                url = item[1]
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

        # Pass on node with no img markdown tags
        if not current_link_nodes:
            new_nodes.append(current_node)
            continue

        # Passing on count from regex.subn as we have already verified images exist
        substrings = []
        i = 0
        for link in current_link_nodes:
            substrings.append(current_node.text[i : link[2]])
            i = link[3]
        substrings.append(current_node.text[i : len(current_node.text)])
        zipped = list(
            itertools.chain.from_iterable(
                itertools.zip_longest(substrings, current_link_nodes, fillvalue="")
            )
        )
        for item in zipped:
            if type(item) is str:
                if item != "":
                    new_nodes.append(TextNode(item, TextType.TEXT))
            elif type(item) is tuple:
                anchor_text = item[0]
                url = item[1]
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
    return new_nodes
