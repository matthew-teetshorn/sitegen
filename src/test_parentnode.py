import unittest
import os

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_eq(self):
        node1 = ParentNode("p", [LeafNode("p", "Some text")])
        node2 = ParentNode("p", [LeafNode("p", "Some text")])
        self.assertEqual(node1, node2)

    def test_eq_default(self):
        node1 = ParentNode("p", [LeafNode("p", "Some text")])
        node2 = ParentNode("p", [LeafNode("p", "Some text")], None)
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = ParentNode("p", [LeafNode("p", "Some text")])
        node2 = ParentNode("p", [LeafNode("p", "Some other text")])
        self.assertNotEqual(node1, node2)

    def test_neq_tag(self):
        node1 = ParentNode("a", None)
        node2 = ParentNode("p", None)
        self.assertNotEqual(node1, node2)

    def test_to_html_empty_children(self):
        node1 = ParentNode("p", None)
        self.assertRaises(ValueError, node1.to_html)

    def test_to_html_empty_tag(self):
        node1 = ParentNode(None, [LeafNode("p", "Some text")])
        self.assertRaises(ValueError, node1.to_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_all_leaves(self):
        node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold Text"),
                LeafNode(None, "Normal Text"),
                LeafNode("i", "italic Text"),
                LeafNode(None, "Normal Text"),
            ],
        )
        self.assertEqual(
            node1.to_html(),
            "<p><b>Bold Text</b>Normal Text<i>italic Text</i>Normal Text</p>",
        )


if __name__ == "__main__":
    unittest.main()
