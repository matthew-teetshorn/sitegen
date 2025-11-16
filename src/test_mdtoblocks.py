import unittest
import os

from mdtoblocks import markdown_to_blocks


class TestSplitImgsLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_p1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        print("\n:::::::::::::::::::RESULT INCOMING::::::::::::::::::")
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_p2(self):
        md = """
this is a paragraph







with a bunch of lines
"""
        blocks = markdown_to_blocks(md)
        print("\n:::::::::::::::::::RESULT INCOMING::::::::::::::::::")
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "this is a paragraph",
                "with a bunch of lines",
            ],
        )

    def test_p3(self):
        md = """
this is a paragraph



Heres one in the middle



with a bunch of lines
"""
        blocks = markdown_to_blocks(md)
        print("\n:::::::::::::::::::RESULT INCOMING::::::::::::::::::")
        print(blocks)
        self.assertEqual(
            blocks,
            [
                "this is a paragraph",
                "Heres one in the middle",
                "with a bunch of lines",
            ],
        )


if __name__ == "__main__":
    unittest.main()
