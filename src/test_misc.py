import unittest
from textnode import TextNode, TextType
from misc import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_splits(self):
        node = TextNode("Some *italic* and **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "*", TextType.ITALIC)
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)


    def test_no_delimiters(self):
        node = TextNode("Plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])
    
    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_adjacent_delimiters(self):
        node = TextNode("**bold****bold again**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("bold again", TextType.BOLD),
        ]
        self.assertEqual(result, expected)


    def test_extract_markdown_images(self):
        text = "![image1](https://example.com/1.jpg) ![image2](https://example.com/2.png)"
        assert extract_markdown_images(text) == [
            ("image1", "https://example.com/1.jpg"),
            ("image2", "https://example.com/2.png"),
        ]

        text = "This is a ![test image](https://example.com/test.jpg)"
        assert extract_markdown_images(text) == [("test image", "https://example.com/test.jpg")]

        text = "No images here."
        assert extract_markdown_images(text) == []


    def test_extract_markdown_links(self):
        text = "[link1](https://example.com) [link2](https://example.org)"
        assert extract_markdown_links(text) == [
            ("link1", "https://example.com"),
            ("link2", "https://example.org"),
        ]

        text = "This is a [test link](https://example.com/test)"
        assert extract_markdown_links(text) == [("test link", "https://example.com/test")]

        text = "No links here."
        assert extract_markdown_links(text) == []

    def test_mixed_content(self):
        text = "![image](https://example.com/image.jpg) [link](https://example.com)"
        assert extract_markdown_images(text) == [("image", "https://example.com/image.jpg")]
        assert extract_markdown_links(text) == [("link", "https://example.com")]

    def test_basic_image_split(self):
        node = TextNode("Text with ![image1](url1)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url1"),
        ]
        assert result == expected

    def test_multiple_images(self):
        node = TextNode("Text with ![image1](url1) and ![image2](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "url2"),
        ]
        assert result == expected

    def test_no_images(self):
        node = TextNode("This is plain text with no images.", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [node]
        assert result == expected


    def test_adjacent_images(self):
        node = TextNode("Text![image1](url1)![image2](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text", TextType.TEXT),
            TextNode("image1", TextType.IMAGE, "url1"),
            TextNode("image2", TextType.IMAGE, "url2"),
        ]
        assert result == expected

    def test_image_without_surrounding_text(self):
        node = TextNode("![image](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "url"),
        ]
        assert result == expected

    def test_image_without_surrounding_text(self):
        node = TextNode("![image](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "url"),
        ]
        assert result == expected

    def test_malformed_image_markdown(self):
        node = TextNode("This is text with ![image](url but no closing parenthesis", TextType.TEXT)
        try:
            split_nodes_image([node])
        except ValueError as e:
            assert str(e) == "Missing closing delimiter ')' in text: This is text with ![image](url but no closing parenthesis"

    def test_basic_link_split(self):
        node = TextNode("Text with [link](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        assert result == expected

    def test_multiple_links(self):
        node = TextNode("Text with [link1](url1) and [link2](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        assert result == expected

    def test_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [node]
        assert result == expected

    def test_adjacent_links(self):
        node = TextNode("Text[link1](url1)[link2](url2)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("Text", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        assert result == expected

    def test_link_without_surrounding_text(self):
        node = TextNode("[link](url)", TextType.TEXT)
        result = split_nodes_link([node])
        expected = [
            TextNode("link", TextType.LINK, "url"),
        ]
        assert result == expected

    def test_malformed_link_markdown(self):
        node = TextNode("This is text with [link](url but no closing parenthesis", TextType.TEXT)
        try:
            split_nodes_link([node])
        except ValueError as e:
            assert str(e) == "Missing closing delimiter ')' in text: This is text with [link](url but no closing parenthesis"

    def test_mixed_links_and_images(self):
        node = TextNode("Text with [link](url) and ![image](url2)", TextType.TEXT)
        links_result = split_nodes_link([node])
        final_result = split_nodes_image(links_result)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
        ]
        assert final_result == expected

    def test_nested_markdown(self):
        node = TextNode("Text with [link](url) and some text ![image](url2)", TextType.TEXT)
        links_result = split_nodes_link([node])
        final_result = split_nodes_image(links_result)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(" and some text ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url2"),
        ]
        assert final_result == expected

    def test_no_content_after_markdown(self):
        node = TextNode("Text ends with ![image](url)", TextType.TEXT)
        result = split_nodes_image([node])
        expected = [
            TextNode("Text ends with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
        ]
        assert result == expected

    def test_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result_images = split_nodes_image([node])
        result_links = split_nodes_link([node])
        assert result_images == [node]
        assert result_links == [node]

    def test_multiple_consecutive_links_images(self):
        node = TextNode("[link1](url1)[link2](url2)![image1](url3)![image2](url4)", TextType.TEXT)
        links_result = split_nodes_link([node])
        final_result = split_nodes_image(links_result)
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode("image1", TextType.IMAGE, "url3"),
            TextNode("image2", TextType.IMAGE, "url4"),
        ]
        assert final_result == expected

    def test_simple_text(self):
        text = "This is simple text."
        result = text_to_textnodes(text)
        expected = [TextNode("This is simple text.", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_and_code(self):
        text = "This *italic* word and a `code block`."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_images(self):
        text = "This is an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is an image ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_links(self):
        text = "Here is a [link](https://boot.dev) and another [example](https://example.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("example", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_combined(self):
        text = "This is **bold** and *italic* with a `code block`, ![image](url), and [link](url)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    
    def test_basic_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_multiple_empty_lines(self):
        text = """# Heading 1


This is a paragraph.


* List item 1
* List item 2


Another paragraph.
"""
        expected = [
            "# Heading 1",
            "This is a paragraph.",
            "* List item 1\n* List item 2",
            "Another paragraph."
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_trailing_and_leading_whitespace(self):
        text = """  
# Heading 1  

This is a paragraph with leading and trailing spaces.  

* List item 1
* List item 2   

Another paragraph.   
"""
        expected = [
            "# Heading 1",
            "This is a paragraph with leading and trailing spaces.",
            "* List item 1\n* List item 2",
            "Another paragraph."
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_single_block(self):
        text = "This is just a single block of text."
        expected = ["This is just a single block of text."]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_only_newlines(self):
        text = "\n\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_only_whitespace(self):
        text = "     \n  \n  \n  "
        expected = []
        self.assertEqual(markdown_to_blocks(text), expected)


    def test_mixed_content(self):
        text = """# Title

Hello, this is a paragraph.

> A quote block

1. Ordered list item 1
2. Ordered list item 2

Some more text.

```
print("Code block")
```

End of document.
"""
        expected = [
            "# Title",
            "Hello, this is a paragraph.",
            "> A quote block",
            "1. Ordered list item 1\n2. Ordered list item 2",
            "Some more text.",
            "```\nprint(\"Code block\")\n```",
            "End of document."
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("## Subheading"), "heading")
        self.assertEqual(block_to_block_type("###### Smallest heading"), "heading")

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('Hello')\n```"), "code")
        self.assertEqual(block_to_block_type("```\ndef add(x, y):\n    return x + y\n```"), "code")

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2\n> Line 3"), "quote")

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("- Task 1\n- Task 2\n- Task 3"), "unordered_list")

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), "ordered_list")
        self.assertEqual(block_to_block_type("1. Task 1\n2. Task 2\n3. Task 3"), "ordered_list")

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), "paragraph")
        self.assertEqual(block_to_block_type("Here is another paragraph with **bold text** inside."), "paragraph")

    def test_mixed_content(self):
        self.assertEqual(block_to_block_type("Here is a paragraph.\n- But also a list item."), "paragraph")

    def test_invalid_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n3. Incorrect numbering"), "paragraph")

    def test_heading(self):
        md = "# Heading"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><h1>Heading</h1></div>")

    def test_paragraph(self):
        md = "This is a paragraph."
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><p>This is a paragraph.</p></div>")

    def test_code_block1(self):
        md = "```\nprint('Hello')\n```"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html().strip(), "<div><pre><code>print('Hello')</code></pre></div>")


    def test_quote_block(self):
        md = "> This is a quote."
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><blockquote>This is a quote.</blockquote></div>")

    def test_unordered_list(self):
        md = "* Item 1\n* Item 2"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>")

    def test_ordered_list(self):
        md = "1. First item\n2. Second item"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><ol><li>First item</li><li>Second item</li></ol></div>")

    def test_valid_title(self):
        self.assertEqual(extract_title("# Welcome to My Blog"), "Welcome to My Blog")

    def test_valid_title_with_whitespace(self):
        self.assertEqual(extract_title("#    Hello World  "), "Hello World")

    def test_no_title_raises_error(self):
        with self.assertRaises(ValueError):
            extract_title("This is just a paragraph\nAnother line")

    def test_title_among_other_text(self):
        markdown = "Some text\n# My Title\nMore text"
        self.assertEqual(extract_title(markdown), "My Title")
if __name__ == "__main__":
    unittest.main()
