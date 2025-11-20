import unittest
import os

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_1(self):
        text = "# Simple Header"
        expected = "Simple Header"
        result = extract_title(text)
        self.assertEqual(result, expected)

    def test_2(self):
        text = "## Simple Header"
        self.assertRaises(Exception, extract_title, text)

    def test_3(self):
        text = "### Blah little header\n\n# Simple Header\n\nSome other stuff"
        expected = "Simple Header"
        result = extract_title(text)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
