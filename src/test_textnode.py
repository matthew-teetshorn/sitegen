import unittest
import os

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text nod", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, url="www.site.com")
        self.assertNotEqual(node, node2)

    def test_neq_other_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, "this is not a node")

    def test_text_to_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_node(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic_to_node(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code_to_node(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link_to_node_noURL(self):
        node = TextNode("This is a link node", TextType.LINK)
        self.assertRaises(ValueError, text_node_to_html_node, node)

    def test_link_to_node(self):
        node = TextNode("This is a link node", TextType.LINK, "http://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertIsNotNone(html_node.props)
        if html_node.props is not None:  # Stop pyright from yelling
            self.assertEqual(html_node.props["href"], "http://boot.dev")

    def test_img_to_node(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://imagesrc.com")
        html_node = text_node_to_html_node(node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertIsNotNone(html_node.props)
        if html_node.props is not None:  # Stop pyright from yelling
            self.assertEqual(html_node.props["src"], "http://imagesrc.com")
            self.assertEqual(html_node.props["alt"], "This is an image node")


if __name__ == "__main__":
    unittest.main()
