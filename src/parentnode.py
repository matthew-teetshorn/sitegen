from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        # ParentNode is not allowed to have a value
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have at least one child")

        ret_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            ret_str += child.to_html()
        ret_str += f"</{self.tag}>"

        return ret_str
