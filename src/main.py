import os
from initilizer import copy_static, generate_pages_recursive

def main():
    static_src = "static"
    public_dest = "public"
    content_src = "src/content"  # ✅ Update path to `src/content`
    template_src = "src/template.html"  # ✅ Ensure template is correctly referenced

    print(f"Current Working Directory: {os.getcwd()}")
    print("🧹 Cleaning public directory...")
    copy_static(static_src, public_dest)

    print("🚀 Generating site recursively...")
    generate_pages_recursive(content_src, template_src, public_dest)

    print("🎉 Static site generated successfully!")

if __name__ == "__main__":
    main()
