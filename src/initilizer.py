import os
import shutil
from misc import markdown_to_html_node, extract_title

def copy_static(src, dest):
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory '{src}' not found!")

    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest) 

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_static(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)
            print(f"Copied: {src_path} → {dest_path}")


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, "r", encoding="utf-8") as from_file:
        markdown_content = from_file.read()

    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as to_file:
        to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    print(f"DEBUG: Checking directory: {dir_path_content}")
    
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"❌ Directory not found: {dir_path_content}")
    
    for entry in os.listdir(dir_path_content):
        content_entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(content_entry_path):
            os.makedirs(dest_entry_path, exist_ok=True)
            generate_pages_recursive(content_entry_path, template_path, dest_entry_path)

        elif os.path.isfile(content_entry_path) and entry.endswith(".md"):
            dest_html_path = os.path.join(dest_dir_path, entry.replace(".md", ".html"))
            print(f"📄 Generating page from {content_entry_path} → {dest_html_path}")
            generate_page(content_entry_path, template_path, dest_html_path)

