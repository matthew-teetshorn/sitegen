from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        # LeafNode is not allowed to have children
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def props_to_html(self):
        ret_str = ""
        if self.props is None or len(self.props) == 0:
            return ret_str

        for prop in self.props:
            ret_str += f' {prop}="{self.props[prop]}"'

        return ret_str

    def __eq__(self, other):
        equal = True
        if type(self) is not type(other):
            return False
        for attrname, attrvalue in vars(self).items():
            if getattr(self, attrname) != getattr(other, attrname):
                equal = False
        return equal

    def __repr__(self, indent: int = 0):
        indent_str = " " * indent
        ret_str = ""
        ret_str += "\n" + indent_str + f"HTMLNode: tag: {self.tag}, value: {self.value}"

        if self.children is None:
            ret_str += ", children: None"
        if self.props is None:
            ret_str += ", props: None"

        if self.children is not None:
            ret_str += "\n"
            for child in self.children:
                ret_str += indent_str + "   Child:"
                ret_str += child.__repr__(indent + 4)

        if self.props is not None:
            ret_str += "\n"
            ret_str += indent_str + "   Props:"
            ret_str += self.props_to_html()
            # for prop in self.props:
            #     ret_str += f" {prop}"

            ret_str += "\n"

        return ret_str + "\n"
