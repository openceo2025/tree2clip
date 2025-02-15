import os
import argparse
import fnmatch
import pyperclip

def generate_tree(root, prefix=""):
    """Generate a directory tree structure as a list of strings."""
    lines = []
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return [prefix + "[Access Denied]"]
    count = len(entries)
    for i, entry in enumerate(entries):
        path = os.path.join(root, entry)
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + entry)
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree(path, prefix + extension))
    return lines

def collect_file_contents(root, exclude_patterns=None, skip_all=False):
    """
    Collect the contents of each file in the directory recursively.
    
    If skip_all is True, all file contents are excluded.
    Files matching any of the patterns in exclude_patterns are not read.
    
    By default, the following files are excluded:
    - Files matching *.bin
    - Image files: *.png, *.jpg, *.jpeg, *.gif, *.bmp
    - Python bytecode files: *.pyc
    """
    default_excludes = ["*.bin", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.pyc"]
    if exclude_patterns:
        exclude_patterns = list(set(exclude_patterns) | set(default_excludes))
    else:
        exclude_patterns = default_excludes

    file_texts = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Exclude __pycache__ directories from recursion
        if '__pycache__' in dirnames:
            dirnames.remove('__pycache__')
        filenames.sort()
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(dirpath, filename), root)
            if skip_all:
                continue
            if any(fnmatch.fnmatch(filename, pattern) for pattern in exclude_patterns):
                continue
            file_full_path = os.path.join(dirpath, filename)
            try:
                with open(file_full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                header = f"\n=== {relative_path} ===\n"
                file_texts.append(header + content)
            except Exception as e:
                header = f"\n=== {relative_path} (failed to read) ===\n"
                file_texts.append(header + str(e))
    return file_texts

def main():
    parser = argparse.ArgumentParser(
        description="Tool to generate a directory tree and copy file contents to the clipboard."
    )
    parser.add_argument(
        "directory", nargs="?", default=".",
        help="Base directory for generating the tree (default: current directory)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-content", action="store_true",
        help="Exclude file contents and copy only the tree structure"
    )
    group.add_argument(
        "--exclude", action="append", metavar="PATTERN",
        help="Exclude files matching the given glob pattern (can be specified multiple times), e.g., --exclude \"*.txt\""
    )
    args = parser.parse_args()
    
    target_dir = os.path.abspath(args.directory)
    if not os.path.isdir(target_dir):
        print(f"Specified directory does not exist: {target_dir}")
        return
    
    # Generate the directory tree
    tree_lines = generate_tree(target_dir)
    tree_text = "\n".join([os.path.basename(target_dir)] + tree_lines)
    
    # Collect file contents
    if args.no_content:
        files_text = "\n[File contents excluded]\n"
    else:
        files_text_list = collect_file_contents(
            target_dir,
            exclude_patterns=args.exclude,
            skip_all=False
        )
        if files_text_list:
            files_text = "\n".join(files_text_list)
        else:
            files_text = "\n[No file contents found]\n"
    
    # Combine the tree and file contents into one output
    output_text = "Directory Tree:\n" + tree_text + "\n\nFile Contents:\n" + files_text
    
    # Copy the output to the clipboard
    try:
        pyperclip.copy(output_text)
        print("Directory tree and file contents copied to clipboard.")
    except Exception as e:
        print("Failed to copy to clipboard:", e)
    
    # Also print the directory tree to stdout
    print("\n" + tree_text)

if __name__ == '__main__':
    main()
