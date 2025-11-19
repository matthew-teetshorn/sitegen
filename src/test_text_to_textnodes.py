import unittest
import os

from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_link0(self):
        string = (
            "This is **text** with an _italic_ word and a `code block`"
            " and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
            " and a [link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(string)
        self.assertEqual(result, expected)

    def test_link1(self):
        string = "There is no markdown in here"
        expected = [
            TextNode("There is no markdown in here", TextType.TEXT),
        ]
        result = text_to_textnodes(string)
        self.assertEqual(result, expected)

    def test_link2(self):
        string = "_IT_ has **B** ![l](u) `code line`"
        expected = [
            TextNode("IT", TextType.ITALIC),
            TextNode(" has ", TextType.TEXT),
            TextNode("B", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("l", TextType.IMAGE, "u"),
            TextNode(" ", TextType.TEXT),
            TextNode("code line", TextType.CODE),
        ]
        result = text_to_textnodes(string)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
