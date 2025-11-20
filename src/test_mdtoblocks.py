import unittest
import os

from mdtoblocks import block_to_blocktype, markdown_to_blocks, BlockType


class TestMdToBlocks(unittest.TestCase):
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
        self.assertEqual(
            blocks,
            [
                "this is a paragraph",
                "Heres one in the middle",
                "with a bunch of lines",
            ],
        )

    def test_p4(self):
        md = """
# this is a heading
### with another heading
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# this is a heading\n### with another heading",
            ],
        )

    def test_h1(self):
        md = "# Heading"
        expected = BlockType.HEADING
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_h2(self):
        md = "###### Heading"
        expected = BlockType.HEADING
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_h3(self):
        # Too many #s
        md = "####### Heading"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_h4(self):
        # Only support blocks with single heading lines
        md = "# Heading\n## Heading 2"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_h5(self):
        # Must have space between
        md = "#Heading"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_c1(self):
        md = "``` This is a code block ```"
        expected = BlockType.CODE
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_c2(self):
        md = """```
int max = 10;
for (int i = 0; i < max; i++) {
doSomething;
}
```"""
        expected = BlockType.CODE
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_c3(self):
        md = """```
int max = 10;
for (int i = 0; i < max; i++) {
doSomething;
}
`"""
        # Improper ending "`" for code block
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_q1(self):
        md = "> Here is a block quote"
        expected = BlockType.QUOTE
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_q2(self):
        md = "> Here is a block quote\n> Another\n> Yet Another\n> Yup, again"
        expected = BlockType.QUOTE
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_q3(self):
        # Missing space at beginning
        md = ">Here is a block quote"
        expected = BlockType.QUOTE
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ul1(self):
        md = "- Here is an unordered list"
        expected = BlockType.UNORDERED_LIST
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ul2(self):
        md = "- Here is a unordered list\n- Another\n- Yet Another\n- Yup, again"
        expected = BlockType.UNORDERED_LIST
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ul3(self):
        # Missing space at beginning
        md = "-Here is a bad list"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ul4(self):
        # One line not quoted
        md = "- Here is a unordered list\n- Another\noops\n- Yup, again"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ol1(self):
        md = "1. Here is an ordered list"
        expected = BlockType.ORDERED_LIST
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ol2(self):
        md = "2. Here is an ordered list"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ol3(self):
        md = "1. Here is an ordered list\n2. Next item\n3. Third item"
        expected = BlockType.ORDERED_LIST
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ol4(self):
        md = "10. Here is an ordered list"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ol5(self):
        md = "1. a\n2. a\n3. a\n4. a\n5. a\n6. a\n7. a\n8. a\n9. a\n10. a"
        expected = BlockType.ORDERED_LIST
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)

    def test_ol6(self):
        # Misnumbered at entry 5
        md = "1. a\n2. a\n3. a\n4. a\n4. a\n6. a\n7. a\n8. a\n9. a\n10. a"
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(md)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
