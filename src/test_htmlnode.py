import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        """Test converting props dictionary to an HTML attribute string."""
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_empty_props(self):
        """Test when props are empty."""
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        """Test the __repr__ method."""
        node = HTMLNode(tag="a", value="Click me", props={"href": "https://example.com"})
        expected_repr = (
            "HTMLNode(tag=a, value=Click me, children=[], props={'href': 'https://example.com'})"
        )
        self.assertEqual(repr(node), expected_repr)

    def test_children(self):
        """Test adding children to the node."""
        child = HTMLNode(tag="span", value="child text")
        parent = HTMLNode(tag="div", children=[child])
        self.assertEqual(parent.children[0], child)
        self.assertEqual(len(parent.children), 1)

    def test_no_tag(self):
        """Test an HTMLNode without a tag (should render raw text)."""
        node = HTMLNode(value="Raw text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Raw text")

    def test_no_value_with_children(self):
        """Test a node with children but no value."""
        child = HTMLNode(tag="span", value="child text")
        parent = HTMLNode(tag="div", children=[child])
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 1)

    def test_no_children_with_value(self):
        """Test a node with a value but no children."""
        node = HTMLNode(tag="p", value="Paragraph text")
        self.assertEqual(node.value, "Paragraph text")
        self.assertEqual(len(node.children), 0)

    def test_props_to_html_edge_case(self):
        """Test props with special characters."""
        node = HTMLNode(props={"data-info": "Some info", "class": "my-class"})
        self.assertEqual(node.props_to_html(), ' data-info="Some info" class="my-class"')

    def test_empty_node(self):
        """Test an HTMLNode with all fields empty."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_nested_nodes(self):
        """Test deeply nested children nodes."""
        child1 = HTMLNode(tag="span", value="child1 text")
        child2 = HTMLNode(tag="span", value="child2 text")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.children[0], child1)
        self.assertEqual(parent.children[1], child2) 
        self.assertEqual(len(parent.children), 2)

    def test_props_with_none(self):
        """Test props where some attributes have a None value."""
        node = HTMLNode(tag="div", props={"id": "main", "data-info": None})
        self.assertEqual(node.props_to_html(), ' id="main"')

    def test_multiple_children(self):
        """Test multiple children with different tags and values."""
        child1 = HTMLNode(tag="h1", value="Title")
        child2 = HTMLNode(tag="p", value="Description")
        parent = HTMLNode(tag="section", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].tag, "h1")
        self.assertEqual(parent.children[1].tag, "p")

    def test_mixed_children_and_value(self):
        """Test a node with both value and children (value takes precedence)."""
        child = HTMLNode(tag="span", value="child text")
        parent = HTMLNode(tag="div", value="Parent text", children=[child])
        self.assertEqual(parent.value, "Parent text")
        self.assertEqual(len(parent.children), 1)

    def test_repr_with_children(self):
        """Test __repr__ method for a node with children."""
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        expected_repr = (
            "HTMLNode(tag=div, value=None, children=[HTMLNode(tag=span, value=Child 1, children=[], props={}), "
            "HTMLNode(tag=span, value=Child 2, children=[], props={})], props={})"
        )
        self.assertEqual(repr(parent), expected_repr)

if __name__ == "__main__":
    unittest.main()