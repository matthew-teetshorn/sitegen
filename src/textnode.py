from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, type: TextType, url: str | None = None):
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, other):
        equal = True
        if type(self) is not type(other):
            return False
        for attrname, attrvalue in vars(self).items():
            if getattr(self, attrname) != getattr(other, attrname):
                equal = False
        return equal

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.type not in TextType:
        raise TypeError("TextNode type is not of valid TextType")
    match text_node.type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Attempting to create link without valid URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Attempting to create image without valid URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
