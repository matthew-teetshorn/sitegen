import unittest
import os

from extractlinks import extract_markdown_images, extract_markdown_links


class TestExtractLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Custom setUpClass method to print the current file name.
        """
        print(f"\nRunning tests from: {os.path.basename(__file__)}")

    def test_link(self):
        text = "Here is a link [boot.dev](https://boot.dev)"
        expected = ("boot.dev", "https://boot.dev")
        result = extract_markdown_links(text)
        if result is not None:
            item1, item2 = result[0][0], result[0][1]
            self.assertEqual((item1, item2), expected)
        self.assertIsNotNone(result)

    def test_img(self):
        text = "Here is an image ![alt text](lorem.picsum/200/200)"
        expected = [("alt text", "lorem.picsum/200/200")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_both_for_image(self):
        text = "Here is an image ![alt text](lorem.picsum/200/200) and link [to boot dev](https://boot.dev)"
        expected = [("alt text", "lorem.picsum/200/200")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_both_for_link(self):
        text = "Here is an image ![alt text](lorem.picsum/200/200) and link [to boot dev](https://boot.dev)"
        expected = ("to boot dev", "https://boot.dev")
        result = extract_markdown_links(text)
        if result is not None:
            item1, item2 = result[0][0], result[0][1]
            self.assertEqual((item1, item2), expected)
        self.assertIsNotNone(result)

    def test_weird_link(self):
        text = "Here is a link tag [a[to boot dev](https://boot.dev) in front of a link"
        expected = ("to boot dev", "https://boot.dev")
        result = extract_markdown_links(text)
        if result is not None:
            item1, item2 = result[0][0], result[0][1]
            self.assertEqual((item1, item2), expected)
        self.assertIsNotNone(result)

    def test_weird_img_none(self):
        text = (
            "Here is an image tag ![a[to boot dev](https://boot.dev) in front of a link"
        )
        # Should not find the image tag with extra '[' inside
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_weird_img(self):
        text = "Here is an image tag ![a![alt text](lorem.picsum/200/200) in front of an image tag"
        expected = [("alt text", "lorem.picsum/200/200")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_link_parens(self):
        text = "Here is a link tag [to boot dev](https://boot.(paren)dev) in front of a link"
        expected = ("to boot dev", "https://boot.(paren)dev")
        result = extract_markdown_links(text)
        if result is not None:
            item1, item2 = result[0][0], result[0][1]
            self.assertEqual((item1, item2), expected)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
