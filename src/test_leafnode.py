import unittest
import os

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_eq(self):
        node1 = LeafNode("p", "some text")
        node2 = LeafNode("p", "some text")
        self.assertEqual(node1, node2)

    def test_eq_default(self):
        node1 = LeafNode("p", "some text")
        node2 = LeafNode("p", "some text", None, None)
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = LeafNode("p", "some text")
        node2 = LeafNode("p", "some other text")
        self.assertNotEqual(node1, node2)

    def test_neq_tag(self):
        node1 = LeafNode("a")
        node2 = LeafNode("p")
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        node1 = LeafNode("a", props={"href": "https://boot.dev"})
        node2 = LeafNode("a", props={"href": "https://python.org"})
        self.assertNotEqual(node1, node2)

    def test_has_children(self):
        node1 = LeafNode("a", children=[LeafNode("p"), LeafNode("H1")])
        self.assertIsNone(node1.children)

    def test_leaf_to_html_p(self):
        node1 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node1 = LeafNode("a", "Click Here", None, {"href": "https://link.dev"})
        self.assertEqual(node1.to_html(), '<a href="https://link.dev">Click Here</a>')


if __name__ == "__main__":
    unittest.main()
