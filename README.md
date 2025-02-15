# tree2clip

**tree2clip** is a Python tool that recursively generates a directory tree and concatenates the contents of files, then copies the result to the clipboard. It is especially useful for providing an entire directory's information to large language models (LLMs).

## Features

- Recursively generates a directory tree from a specified folder
- Collects and concatenates the text contents of files
- Automatically excludes unnecessary files such as binary files, image files, and Python bytecode (e.g., `*.pyc` and files in `__pycache__`)
- Runs from the command line and copies the output to the clipboard

## Installation

To install from PyPI:

```bash
pip install tree2clip
```

For development purposes, install in editable mode:

```bash
pip install -e .
```

## Usage

### Basic Usage

Copy the directory tree and file contents from the current directory:

```bash
tree2clip
```

Specify a different directory:

```bash
tree2clip /path/to/directory
```

### Options

- **Copy tree only (exclude file contents):**

  ```bash
  tree2clip /path/to/directory --no-content
  ```

- **Exclude files matching a specific pattern:**

  For example, to exclude files ending with `.txt`:

  ```bash
  tree2clip /path/to/directory --exclude "*.txt"
  ```

## Notes

- By default, the following files are excluded from content collection:
  - Files matching `*.bin`
  - Image files: `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.bmp`
  - Python bytecode files: `*.pyc` and files within the `__pycache__` directory

- The output is automatically copied to your clipboard, so simply paste where needed.

## License

This project is released under the [MIT License](LICENSE).
