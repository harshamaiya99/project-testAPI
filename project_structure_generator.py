import os
import re

IGNORE_FOLDERS = {".idea", "__pycache__", ".pytest_cache", ".git", "test_results", "test_reports"}
README_FILE = "README.md"

def build_tree(start_path, prefix="", root_path=None):
    if root_path is None:
        root_path = start_path

    lines = []
    entries = [e for e in sorted(os.listdir(start_path)) if e not in IGNORE_FOLDERS]
    entries_count = len(entries)

    for i, entry in enumerate(entries):
        path = os.path.join(start_path, entry)
        rel_path = os.path.relpath(path, root_path).replace("\\", "/")

        # icons
        icon = "📁" if os.path.isdir(path) else "📄"

        # make clickable <a> link with no underline
        link = f'<a href="./{rel_path}" style="text-decoration:none">{entry}</a>'

        connector = "└── " if i == entries_count - 1 else "├── "
        lines.append(prefix + connector + f"{icon} {link}")

        if os.path.isdir(path):
            extension = "    " if i == entries_count - 1 else "│   "
            lines.extend(build_tree(path, prefix + extension, root_path))

    return lines


if __name__ == "__main__":
    # ✅ Absolute path to your project
    root_dir = r"C:\Users\maiya\PycharmProjects\project_testAPI"

    # Just the folder name at the top (not full path)
    project_name = os.path.basename(root_dir.rstrip("\\/"))
    project_link = f'<a href="." style="text-decoration:none">{project_name}</a>'
    tree_lines = [f"📁 {project_link}"] + build_tree(root_dir)
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
            r"(## Project Structure:\s*)(?:<pre>[\s\S]*?</pre>)?",
            r"\1" + tree_text,
            content,
            flags=re.MULTILINE,
        )
    else:
        content += f"\n\n## Project Structure:\n{tree_text}"

    # Write back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Project structure appended/updated in {readme_path}")
