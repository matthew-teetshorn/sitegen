from typing import List
import unittest
import os

from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node
from splitnodes import split_nodes_delimiter


class TestSplitNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_none(self):
        node = TextNode("This text has no delimiter", TextType.TEXT)
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(old_nodes[0], new_nodes[0])

    def test_open(self):
        node = TextNode("This **text has no closing delimiter", TextType.TEXT)
        nodes = [node]
        self.assertRaises(Exception, split_nodes_delimiter, nodes, "**", TextType.BOLD)

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_code(self):
        node = TextNode("This is `code block` text", TextType.TEXT)
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_multi_node(self):
        node1 = TextNode("This is **bold** text", TextType.TEXT)
        node2 = TextNode("**This** is bold text at beginning", TextType.TEXT)
        node3 = TextNode("This is bold text at **end**", TextType.TEXT)
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("This", TextType.BOLD))
        self.assertEqual(
            new_nodes[4], TextNode(" is bold text at beginning", TextType.TEXT)
        )
        self.assertEqual(new_nodes[5], TextNode("This is bold text at ", TextType.TEXT))
        self.assertEqual(new_nodes[6], TextNode("end", TextType.BOLD))

    def test_multi_bold(self):
        node = TextNode("**This** is multiple **bold** text **pieces**", TextType.TEXT)
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode(" is multiple ", TextType.TEXT))
        self.assertEqual(new_nodes[2], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[3], TextNode(" text ", TextType.TEXT))
        self.assertEqual(new_nodes[4], TextNode("pieces", TextType.BOLD))


if __name__ == "__main__":
    unittest.main()
