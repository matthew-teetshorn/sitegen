from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ):
        # LeafNode is not allowed to have children
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"

        # void tags do not get a closing tag and end with a /> for xhtml compliance
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}/>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
