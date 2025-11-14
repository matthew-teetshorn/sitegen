from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.type = text_type
        self.url = url

    def __eq__(self, other):
        equal = True
        for attrname, attrvalue in vars(self).items():
            if getattr(self, attrname) != getattr(other, attrname):
                equal = False
        return equal

    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"
