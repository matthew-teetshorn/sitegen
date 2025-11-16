from typing import List
from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter
from extractlinks import split_nodes_image, split_nodes_link

# TEXT = "text"
# BOLD = "bold"
# ITALIC = "italic"
# CODE = "code"
# LINK = "link"
# IMAGE = "image"


class DelimiterType(Enum):
    BOLD = {"delimiter": "**", "text_type": TextType.BOLD}
    ITALIC = {"delimiter": "_", "text_type": TextType.ITALIC}
    CODE = {"delimiter": "`", "text_type": TextType.CODE}


def text_to_textnodes(text: str) -> list[TextNode | HTMLNode]:
    return_list: List[TextNode | HTMLNode] = []
    return_list.append(TextNode(text, TextType.TEXT))

    for delimiter in DelimiterType:
        return_list = split_nodes_delimiter(
            return_list, delimiter.value["delimiter"], delimiter.value["text_type"]
        )

    return_list = split_nodes_image(return_list)
    return_list = split_nodes_link(return_list)
    return return_list
