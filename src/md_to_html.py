from typing import List
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from mdtoblocks import block_to_blocktype, markdown_to_blocks, BlockType
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes
import regex
import re_defs

# Parent Node Types:
# div/p/h1-h6/ul/ol/li/blockquote/pre

# Leaf Node Types
# b/i/code/a/img


def text_to_htmlnodes(text: str) -> List[HTMLNode]:
    textnodes = text_to_textnodes(text)
    leafnodes: List[HTMLNode] = []
    # bold italic code img link
    for node in textnodes:
        match node.type:
            case TextType.TEXT:
                leafnodes.append(LeafNode(None, node.text, None))
            case TextType.BOLD:
                leafnodes.append(LeafNode("b", node.text, None))
            case TextType.ITALIC:
                leafnodes.append(LeafNode("i", node.text, None))
            case TextType.CODE:
                leafnodes.append(LeafNode("code", node.text, None))
            case TextType.LINK:
                leafnodes.extend(link_to_node_helper(node))
            case TextType.IMAGE:
                if node.url is not None:
                    leafnodes.append(
                        LeafNode("img", "", {"src": node.url, "alt": node.text})
                    )
                else:
                    raise TypeError("image url value cannot be None")
    return leafnodes


def link_to_node_helper(node: TextNode) -> List[HTMLNode]:
    ret_nodes = []

    if node.url is None:
        raise TypeError("link url value cannot be None")

    # Link text can contain markdown formatting and should be processed
    possible_children = text_to_htmlnodes(node.text)
    if len(possible_children) == 1:  # No md found
        ret_nodes.append(LeafNode("a", node.text, {"href": node.url}))
    else:
        ret_nodes.append(ParentNode("a", possible_children, {"href": node.url}))
    return ret_nodes


def create_paragraph(text: str) -> HTMLNode:
    nodes: List[HTMLNode] = []
    nodes.extend(text_to_htmlnodes(text))
    p_node = ParentNode("p", nodes, None)

    return p_node


def create_heading(text: str) -> HTMLNode:
    new_text = regex.sub(
        re_defs.REGEX_HEADING,
        "",
        text,
    )

    if len(new_text) == len(text):
        raise ValueError("No markdown heading found in create_heading(text)")

    # Get difference and subtract white space character
    heading_length = len(text) - len(new_text) - 1
    nodes: List[HTMLNode] = []
    nodes.extend(text_to_htmlnodes(new_text))
    p_node = ParentNode(f"h{heading_length}", nodes, None)

    return p_node


def create_code(text: str) -> HTMLNode:
    nodes: List[HTMLNode] = []
    new_text = regex.sub(re_defs.REGEX_CODE_BLOCK, r"\1", text, regex.DOTALL)

    if len(new_text) == len(text):
        raise ValueError("No markdown code block found in create_code(text)")

    new_text = new_text.strip("\n")
    # We don't process the code block as markdown, just append it as a LeafNode
    nodes.append(LeafNode(None, new_text, None))
    p_node = ParentNode("code", nodes, None)

    return p_node


def create_quote(text: str) -> HTMLNode:
    nodes: List[HTMLNode] = []
    p_node = ParentNode(None, None, None)

    return p_node


def create_unordered_list(text: str) -> HTMLNode:
    nodes: List[HTMLNode] = []
    p_node = ParentNode(None, None, None)

    return p_node


def create_ordered_list(text: str) -> HTMLNode:
    nodes: List[HTMLNode] = []
    p_node = ParentNode(None, None, None)

    return p_node


def markdown_to_html(markdown: str) -> ParentNode:
    doc_parent = ParentNode("div", None, None)
    doc_parent.children = []

    blocks = markdown_to_blocks(markdown)
    if blocks == []:
        raise Exception("No blocks found in markdown")

    for block in blocks:
        b_type = block_to_blocktype(block)
        match b_type:
            case BlockType.PARAGRAPH:
                doc_parent.children.append(create_paragraph(block))
            case BlockType.HEADING:
                doc_parent.children.append(create_heading(block))
            case BlockType.CODE:
                doc_parent.children.append(create_code(block))
            case BlockType.QUOTE:
                doc_parent.children.append(create_quote(block))
            case BlockType.UNORDERED_LIST:
                doc_parent.children.append(create_unordered_list(block))
            case BlockType.ORDERED_LIST:
                doc_parent.children.append(create_ordered_list(block))

    return doc_parent
