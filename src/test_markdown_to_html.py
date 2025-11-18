import unittest
import os

from md_to_html import markdown_to_html


class TestMarkdownToHTML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_p1(self):
        text = "Here is a basic paragraph block"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><p>Here is a basic paragraph block</p></div>"
        self.assertEqual(result, expected)

    def test_p2(self):
        text = "Here is a `code` block with **bold** and _italic_ text"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><p>Here is a <code>code</code> block with <b>bold</b> and <i>italic</i> text</p></div>"
        self.assertEqual(result, expected)

    def test_p3(self):
        text = "Here is a `code` block with **bold** and _italic_ text and ![image](i_url) and [link](l_url)"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = '<div><p>Here is a <code>code</code> block with <b>bold</b> and <i>italic</i> text and <img src="i_url" alt="image"/> and <a href="l_url">link</a></p></div>'
        self.assertEqual(result, expected)

    def test_p4(self):
        text = "[here is a **bold** and _italic_ link text with `code in it`](http://www.google.com)"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = '<div><p><a href="http://www.google.com">here is a <b>bold</b> and <i>italic</i> link text with <code>code in it</code></a></p></div>'
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
