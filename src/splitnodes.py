from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for current_node in old_nodes:
        if current_node.type != TextType.TEXT:
            new_nodes.append(current_node)
            continue

        substrings = current_node.text.split(delimiter)
        # Even numbers of delimiter always result in odd number of substrings
        if not len(substrings) % 2:
            raise Exception(
                f"Invalid markdown detected, no closing '{delimiter}' found"
            )

        for i in range(len(substrings)):
            current_substring = substrings[i]
            if current_substring == "":
                continue
            # Even substrings are not between delimiters, odds are
            if not i % 2:
                new_nodes.append(TextNode(current_substring, TextType.TEXT))
            else:
                new_nodes.append(TextNode(current_substring, text_type))

    return new_nodes
