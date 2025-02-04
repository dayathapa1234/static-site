import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from mapper import text_node_to_html_node

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html(self):
        text_node = TextNode("This is raw text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "This is raw text")

    def test_bold_to_html(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_to_html(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_to_html(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "<code>Code text</code>")

    def test_link_to_html(self):
        text_node = TextNode("Google", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">Google</a>')

    def test_image_to_html(self):
        text_node = TextNode("Image description", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.jpg" alt="Image description"></img>')

    def test_invalid_text_type(self):
        text_node = TextNode("Invalid text", None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_link_without_url(self):
        text_node = TextNode("Missing URL", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

    def test_image_without_url(self):
        text_node = TextNode("Missing URL", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

if __name__ == "__main__":
    unittest.main()
