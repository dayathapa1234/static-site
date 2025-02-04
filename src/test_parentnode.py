import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNodeComplex(unittest.TestCase):
    def test_deeply_nested_parent_and_leaf_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("li", "Item 1"),
                        ParentNode(
                            "li",
                            [
                                LeafNode("b", "Bold in list"),
                                LeafNode(None, "Normal in list"),
                            ],
                        ),
                        LeafNode("li", "Item 3"),
                    ],
                ),
                ParentNode(
                    "section",
                    [
                        LeafNode("h1", "Main Heading"),
                        LeafNode("p", "Paragraph with content."),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            (
                '<div>'
                '<ul>'
                '<li>Item 1</li>'
                '<li><b>Bold in list</b>Normal in list</li>'
                '<li>Item 3</li>'
                '</ul>'
                '<section>'
                '<h1>Main Heading</h1>'
                '<p>Paragraph with content.</p>'
                '</section>'
                '</div>'
            ),
        )

    def test_parent_with_htmlnode_child(self):
        class CustomHTMLNode(HTMLNode):
            def to_html(self):
                return "<custom>Custom HTMLNode</custom>"

        node = ParentNode(
            "article",
            [
                CustomHTMLNode(tag=None),
                LeafNode("p", "A paragraph."),
                ParentNode(
                    "div",
                    [LeafNode("span", "Inside div.")],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            (
                '<article>'
                '<custom>Custom HTMLNode</custom>'
                '<p>A paragraph.</p>'
                '<div><span>Inside div.</span></div>'
                '</article>'
            ),
        )

    def test_parent_with_empty_props(self):
        node = ParentNode(
            "section",
            [
                LeafNode("h2", "Subheading"),
                LeafNode("p", "Some text in the section."),
            ],
            props={},
        )
        self.assertEqual(
            node.to_html(),
            '<section><h2>Subheading</h2><p>Some text in the section.</p></section>',
        )

    def test_parent_with_props_and_nested_nodes(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "header",
                    [
                        LeafNode("h1", "Welcome"),
                        LeafNode("h2", "Subheading"),
                    ],
                    {"class": "header-class"},
                ),
                ParentNode(
                    "main",
                    [
                        ParentNode(
                            "article",
                            [
                                LeafNode("p", "First article paragraph."),
                                LeafNode("p", "Second article paragraph."),
                            ],
                            {"id": "article-1"},
                        ),
                        LeafNode("aside", "Sidebar content."),
                    ],
                ),
            ],
            {"id": "main-div", "class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            (
                '<div id="main-div" class="container">'
                '<header class="header-class">'
                '<h1>Welcome</h1>'
                '<h2>Subheading</h2>'
                '</header>'
                '<main>'
                '<article id="article-1">'
                '<p>First article paragraph.</p>'
                '<p>Second article paragraph.</p>'
                '</article>'
                '<aside>Sidebar content.</aside>'
                '</main>'
                '</div>'
            ),
        )

    def test_empty_parent_node_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_parent_node_with_none_tag_raises_error(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "Some text.")])

    def test_parent_with_large_number_of_children(self):
        children = [LeafNode("li", f"Item {i}") for i in range(100)]
        node = ParentNode("ul", children)
        self.assertEqual(
            node.to_html(),
            "<ul>" + "".join([f"<li>Item {i}</li>" for i in range(100)]) + "</ul>",
        )

    def test_nested_parent_nodes_with_empty_props(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "section",
                    [
                        LeafNode("h2", "Section Heading"),
                        ParentNode(
                            "ul",
                            [
                                LeafNode("li", "First list item"),
                                LeafNode("li", "Second list item"),
                            ],
                        ),
                    ],
                    props={},
                )
            ],
            props={},
        )
        self.assertEqual(
            node.to_html(),
            (
                '<body>'
                '<section>'
                '<h2>Section Heading</h2>'
                '<ul>'
                '<li>First list item</li>'
                '<li>Second list item</li>'
                '</ul>'
                '</section>'
                '</body>'
            ),
        )


if __name__ == "__main__":
    unittest.main()
