from typing import List
import unittest
import os

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from extractlinks import split_nodes_image, split_nodes_link


class TestSplitImgsLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_link(self):
        node = TextNode(
            "Here is a link [link text](https://test.com) with some end text",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "https://test.com"),
            TextNode(" with some end text", TextType.TEXT),
        ]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, expected)

    def test_link_mult(self):
        node = TextNode(
            "Here is a link [l1](url1) with another [l2](url2)",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("l1", TextType.LINK, "url1"),
            TextNode(" with another ", TextType.TEXT),
            TextNode("l2", TextType.LINK, "url2"),
        ]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, expected)

    def test_link_with_image(self):
        node = TextNode(
            "Here is a link [l1](url1) with an image ![l2](url2)",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("l1", TextType.LINK, "url1"),
            TextNode(" with an image ![l2](url2)", TextType.TEXT),
        ]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, expected)

    def test_weird_link(self):
        node = TextNode(
            "Here is a weird link ![kin[l1](url1)",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is a weird link ![kin", TextType.TEXT),
            TextNode("l1", TextType.LINK, "url1"),
        ]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, expected)

    def test_weird_link2(self):
        node = TextNode(
            "Here is a weird link [kin[l1](url1)",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is a weird link [kin", TextType.TEXT),
            TextNode("l1", TextType.LINK, "url1"),
        ]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, expected)

    def test_img(self):
        node = TextNode(
            "Here is an image ![image text](https://imageurl.com) with some end text",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("image text", TextType.IMAGE, "https://imageurl.com"),
            TextNode(" with some end text", TextType.TEXT),
        ]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, expected)

    def test_img_mult(self):
        node = TextNode(
            "Here is an image ![t1](url1) and another ![t2](url2)", TextType.TEXT
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("t1", TextType.IMAGE, "url1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("t2", TextType.IMAGE, "url2"),
        ]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, expected)

    def test_img_mult_both_ends(self):
        node = TextNode(
            "![t3](url3) Here is an image ![t1](url1) and another ![t2](url2)",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("t3", TextType.IMAGE, "url3"),
            TextNode(" Here is an image ", TextType.TEXT),
            TextNode("t1", TextType.IMAGE, "url1"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("t2", TextType.IMAGE, "url2"),
        ]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, expected)

    def test_img_with_link(self):
        node = TextNode(
            "Here is an image ![t1](url1) and a link [anchor text](url2)",
            TextType.TEXT,
        )
        old_nodes: List[TextNode | HTMLNode] = []
        old_nodes = [node]
        expected = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("t1", TextType.IMAGE, "url1"),
            TextNode(" and a link [anchor text](url2)", TextType.TEXT),
        ]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
