import unittest
import os

from md_to_html import (
    markdown_to_html,
    create_heading,
    create_code,
    create_quote,
    create_ordered_list,
    create_unordered_list,
)


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

    def test_p5(self):
        text = "![img](i_url) with ![img2](i_url2)"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = '<div><p><img src="i_url" alt="img"/> with <img src="i_url2" alt="img2"/></p></div>'
        self.assertEqual(result, expected)

    def test_p6(self):
        text = "![img](i_url)![img2](i_url2)"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = '<div><p><img src="i_url" alt="img"/><img src="i_url2" alt="img2"/></p></div>'
        self.assertEqual(result, expected)

    def test_p7(self):
        text = "text in front [link1](url1)[link2](url2) text in back"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = '<div><p>text in front <a href="url1">link1</a><a href="url2">link2</a> text in back</p></div>'
        self.assertEqual(result, expected)

    def test_p8(self):
        text = """
Here is a paragraph of text.
That spans across
multiple lines.
"""
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><p>Here is a paragraph of text.<br />That spans across<br />multiple lines.</p></div>"
        self.assertEqual(result, expected)

    def test_h1(self):
        text = "# Here is a heading"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><h1>Here is a heading</h1></div>"
        self.assertEqual(result, expected)

    def test_h2(self):
        text = "###### Here is a heading"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><h6>Here is a heading</h6></div>"
        self.assertEqual(result, expected)

    def test_h3(self):
        text = "####### Here is a paragraph with a bad heading"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><p>####### Here is a paragraph with a bad heading</p></div>"
        self.assertEqual(result, expected)

    def test_h4(self):
        text = "####### Here is a paragraph with a bad heading"
        self.assertRaises(ValueError, create_heading, text)

    def test_h5(self):
        text = "### Here is some **bold** _italic_ and `code` text in a heading"
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><h3>Here is some <b>bold</b> <i>italic</i> and <code>code</code> text in a heading</h3></div>"
        self.assertEqual(result, expected)

    def test_c1(self):
        text = """```
for (int i = 0; i < 10; i++) {
    doSomething();
}```"""
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><pre><code>for (int i = 0; i < 10; i++) {<br />    doSomething();<br />}</code></pre></div>"
        self.assertEqual(result, expected)

    def test_c2(self):
        text = "`` this isn't properly formatted ``"
        self.assertRaises(ValueError, create_code, text)

    def test_q1(self):
        text = """
> Here is a block
> quote with some
> stuff in it.
"""
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><blockquote><p>Here is a block<br />quote with some<br />stuff in it.</p></blockquote></div>"
        self.assertEqual(result, expected)

    def test_q2(self):
        text = """
> Here is a **bold**
> quote with _italic_
> and `code` in it.
"""
        node = markdown_to_html(text)
        result = node.to_html()
        expected = "<div><blockquote><p>Here is a <b>bold</b><br />quote with <i>italic</i><br />and <code>code</code> in it.</p></blockquote></div>"
        self.assertEqual(result, expected)

    def test_q3(self):
        text = """
>Here is a **bold**
>quote with _italic_
>and `code` in it.
"""
        self.assertRaises(ValueError, create_quote, text)


if __name__ == "__main__":
    unittest.main()
