import unittest
import os

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_eq(self):
        node1 = HTMLNode("p", "some text")
        node2 = HTMLNode("p", "some text")
        self.assertEqual(node1, node2)

    def test_eq_default(self):
        node1 = HTMLNode("p", "some text")
        node2 = HTMLNode("p", "some text", None, None)
        self.assertEqual(node1, node2)

    def test_neq_text(self):
        node1 = HTMLNode("p", "some text")
        node2 = HTMLNode("p", "some other text")
        self.assertNotEqual(node1, node2)

    def test_neq_tag(self):
        node1 = HTMLNode("a")
        node2 = HTMLNode("p")
        self.assertNotEqual(node1, node2)

    def test_neq_url(self):
        node1 = HTMLNode("a", props={"href": "https://boot.dev"})
        node2 = HTMLNode("a", props={"href": "https://python.org"})
        self.assertNotEqual(node1, node2)

    def test_neq_children(self):
        node1 = HTMLNode("a", children=[HTMLNode("p"), HTMLNode("H1")])
        node2 = HTMLNode("a", children=[HTMLNode("p")])
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        print(
            HTMLNode(
                "a",
                value="Boot.Dev",
                props={"href": "https://boot.dev", "rel": "external"},
            )
        )
        print(
            HTMLNode(
                "a",
                children=[
                    HTMLNode(
                        "img",
                        props={
                            "border": "0",
                            "alt": "W3Schools",
                            "src": "logo_w3s.gif",
                            "width": "100",
                            "height": "100",
                        },
                    ),
                    HTMLNode(
                        "img",
                        props={
                            "border": "10",
                            "alt": "Some other image",
                            "src": "otherimage.gif",
                            "width": "100",
                            "height": "100",
                        },
                    ),
                ],
            )
        )


if __name__ == "__main__":
    unittest.main()
