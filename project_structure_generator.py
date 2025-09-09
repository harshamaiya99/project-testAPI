import os
import re
import html

IGNORE_FOLDERS = {".idea", "__pycache__", ".pytest_cache", ".git", "test_results", "test_reports"}
IGNORE_FILES = {"project_structure.txt", ".gitignore", ".env"}  # 👈 add files here
README_FILE = "README.md"

def build_tree(start_path, prefix="", relative_path=""):
    lines = []
    entries = [
        e for e in sorted(os.listdir(start_path))
        if not (
            (os.path.isdir(os.path.join(start_path, e)) and e in IGNORE_FOLDERS) or
            (os.path.isfile(os.path.join(start_path, e)) and e in IGNORE_FILES)
        )
    ]
    entries_count = len(entries)

    for i, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        rel_path = os.path.join(relative_path, entry).replace("\\", "/")

        connector = "└── " if i == entries_count - 1 else "├── "

        if os.path.isdir(path):
            icon = "📁 "
            rel_path += "/"   # ✅ ensure folder links open correctly
        else:
            icon = "📄 "

        safe_text = html.escape(entry)
        clickable_entry = f'<a href="{html.escape(rel_path)}">{icon}{safe_text}</a>'

        lines.append(prefix + connector + clickable_entry)

        if os.path.isdir(path):
            extension = "    " if i == entries_count - 1 else "│   "
            lines.extend(build_tree(path, prefix + extension, rel_path.rstrip("/")))
    return lines


if __name__ == "__main__":
    # ✅ Absolute path to your project
    root_dir = r"C:\Users\maiya\PycharmProjects\project_testAPI"

    # Just the folder name at the top (not full path)
    project_name = os.path.basename(root_dir.rstrip("\\/"))
    tree_lines = [f'<a href="./">📁 {html.escape(project_name)}</a>'] + build_tree(root_dir, relative_path=".")
    tree_text = "<pre>\n" + "\n".join(tree_lines) + "\n</pre>"

    readme_path = os.path.join(root_dir, README_FILE)

    # Read existing README.md or create new
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# Project\n\n"

    # Replace or append "## Project Structure:" section
    if "## Project Structure:" in content:
        content = re.sub(
            r"(## Project Structure:\s*)(?:```[\s\S]*?```|<pre>[\s\S]*?</pre>)?",
            r"\1" + tree_text,
            content,
            flags=re.MULTILINE,
        )
    else:
        content += f"\n\n## Project Structure:\n{tree_text}"

    # Write back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Project structure with folder/file links updated in {readme_path}")
