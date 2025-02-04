import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_render_leaf_with_tag_and_value(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_render_leaf_with_tag_value_and_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_render_leaf_without_tag(self):
        node = LeafNode(None, "This is raw text.")
        self.assertEqual(node.to_html(), "This is raw text.")

    def test_leafnode_without_value_raises_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_render_leaf_with_empty_props(self):
        node = LeafNode("div", "Empty props test.", {})
        self.assertEqual(node.to_html(), "<div>Empty props test.</div>")

    def test_render_leaf_with_multiple_props(self):
        node = LeafNode("input", "", {"type": "text", "value": "Sample"})
        self.assertEqual(node.to_html(), '<input type="text" value="Sample"></input>')

    def test_render_leaf_with_numeric_props(self):
        node = LeafNode("input", "", {"maxlength": 10})
        self.assertEqual(node.to_html(), '<input maxlength="10"></input>')

    def test_render_leaf_with_empty_string_props(self):
        node = LeafNode("div", "Sample text", {"data-info": ""})
        self.assertEqual(node.to_html(), '<div data-info="">Sample text</div>')

    def test_render_leaf_with_non_string_value(self):
        node = LeafNode("span", 12345)
        self.assertEqual(node.to_html(), "<span>12345</span>")

if __name__ == "__main__":
    unittest.main()