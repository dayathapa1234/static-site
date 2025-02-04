from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from mapper import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matchs = re.findall(pattern, text)
    return matchs

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text) 
    return matches

def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            before, _, after = text.partition(f"![{alt}]({url})")
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for anchor, url in links:
            before, _, after = text.partition(f"[{anchor}]({url})")
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = after
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    
    nodes = split_nodes_link(nodes)
    
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes

def markdown_to_blocks(markdown):

    blocks = [block.strip() for block in markdown.split("\n\n")]

    return [block for block in blocks if block]

def block_to_block_type(block):

    lines = block.split("\n")

    if re.match(r"^#{1,6} ", lines[0]):
        return "heading"

    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"

    if all(line.startswith(">") for line in lines):
        return "quote"

    if all(re.match(r"^(\*|-)\s", line) for line in lines):
        return "unordered_list"

    if all(re.match(r"^\d+\.\s", line) for line in lines):
        numbers = [int(line.split(".")[0]) for line in lines]
        if numbers == list(range(1, len(numbers) + 1)):
            return "ordered_list"

    return "paragraph"


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            node = handle_heading(block)
        elif block_type == "paragraph":
            node = handle_paragraph(block)
        elif block_type == "code":
            node = handle_code_block(block)
        elif block_type == "quote":
            node = handle_quote_block(block)
        elif block_type == "unordered_list":
            node = handle_unordered_list(block)
        elif block_type == "ordered_list":
            node = handle_ordered_list(block)
        else:
            raise ValueError(f"Unknown block type: {block_type}")

        block_nodes.append(node)

    return ParentNode("div", block_nodes)    

def handle_heading(block):

    match = re.match(r"^(#{1,6}) (.+)", block)
    if not match:
        raise ValueError(f"Invalid heading format: {block}")
    
    level = len(match.group(1))  
    text_content = match.group(2)
    
    children = text_to_children(text_content)
    return ParentNode(f"h{level}", children)

def handle_paragraph(block):

    children = text_to_children(block)
    return ParentNode("p", children)

def handle_code_block(block):
    text_content = block.strip("`").strip()
    return ParentNode("pre", [ParentNode("code", [LeafNode(None, text_content)])])

def handle_quote_block(block):
    quote_text = "\n".join(line.lstrip("> ") for line in block.split("\n"))
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)

def handle_unordered_list(block):
    list_items = []
    for line in block.split("\n"):
        match = re.match(r"^(\*|-)\s*(.*)", line)
        if not match:
            continue

        text = match.group(2)
        print(f"DEBUG: List item text (processed): {text}")

        children = text_to_children(text)
        list_items.append(ParentNode("li", children))

    return ParentNode("ul", list_items)


def handle_ordered_list(block):
    list_items = [ParentNode("li", text_to_children(line.split(". ", 1)[1])) for line in block.split("\n")]
    return ParentNode("ol", list_items)

def handle_table(block):
    rows = block.split("\n")
    header_cells = [ParentNode("th", text_to_children(cell.strip())) for cell in rows[0].split("|") if cell]
    header_row = ParentNode("tr", header_cells)

    body_rows = []
    for row in rows[2:]: 
        body_cells = [ParentNode("td", text_to_children(cell.strip())) for cell in row.split("|") if cell]
        body_rows.append(ParentNode("tr", body_cells))

    return ParentNode("table", [ParentNode("thead", [header_row]), ParentNode("tbody", body_rows)])

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):  
            return line[2:].strip() 
    raise ValueError("No H1 heading found in markdown")