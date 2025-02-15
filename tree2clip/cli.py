import os
import argparse
import fnmatch
import pyperclip

def generate_tree(root, prefix=""):
    """ディレクトリツリーを生成する関数"""
    lines = []
    try:
        entries = sorted(os.listdir(root))
    except PermissionError:
        return [prefix + "[アクセス拒否]"]
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
    ディレクトリ内の各ファイルの内容を収集する関数。
    ・skip_all=Trueの場合は全ファイルの内容を除外する。
    ・exclude_patternsにマッチするファイルは内容を収集しません。
    
    デフォルトで以下のファイルは除外対象となります:
    - *.bin
    - 画像ファイル: *.png, *.jpg, *.jpeg, *.gif, *.bmp
    - バイトコードファイル: *.pyc
    """
    # 除外する拡張子のデフォルトリスト
    default_excludes = ["*.bin", "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.pyc"]
    if exclude_patterns:
        # ユーザー指定とデフォルトを合算（重複は除外）
        exclude_patterns = list(set(exclude_patterns) | set(default_excludes))
    else:
        exclude_patterns = default_excludes

    file_texts = []
    for dirpath, dirnames, filenames in os.walk(root):
        # __pycache__ ディレクトリは再帰対象から除外
        if '__pycache__' in dirnames:
            dirnames.remove('__pycache__')
        filenames.sort()
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(dirpath, filename), root)
            # 全てのファイル内容をスキップする場合
            if skip_all:
                continue
            # 除外パターンにマッチする場合、内容を収集しない
            if any(fnmatch.fnmatch(filename, pattern) for pattern in exclude_patterns):
                continue
            file_full_path = os.path.join(dirpath, filename)
            try:
                with open(file_full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                header = f"\n=== {relative_path} ===\n"
                file_texts.append(header + content)
            except Exception as e:
                header = f"\n=== {relative_path} (読み込み失敗) ===\n"
                file_texts.append(header + str(e))
    return file_texts

def main():
    parser = argparse.ArgumentParser(
        description="ディレクトリのツリー表示とファイル内容をクリップボードにコピーするツール"
    )
    parser.add_argument(
        "directory", nargs="?", default=".",
        help="ツリー表示の起点となるディレクトリ (デフォルトは現在のディレクトリ)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-content", action="store_true",
        help="ファイルの内容を全て除外してツリー表示のみをコピーする"
    )
    group.add_argument(
        "--exclude", action="append", metavar="PATTERN",
        help="指定したパターンにマッチするファイルは内容を除外する (複数指定可)。例: --exclude \"*.txt\""
    )
    args = parser.parse_args()
    
    target_dir = os.path.abspath(args.directory)
    if not os.path.isdir(target_dir):
        print(f"指定されたディレクトリが存在しません: {target_dir}")
        return
    
    # ツリー表示の生成
    tree_lines = generate_tree(target_dir)
    tree_text = "\n".join([os.path.basename(target_dir)] + tree_lines)
    
    # ファイル内容の収集
    if args.no_content:
        files_text = "\n[ファイル内容は除外されています]\n"
    else:
        files_text_list = collect_file_contents(
            target_dir,
            exclude_patterns=args.exclude,
            skip_all=False
        )
        if files_text_list:
            files_text = "\n".join(files_text_list)
        else:
            files_text = "\n[ファイル内容はありません]\n"
    
    # 最終的な出力文字列の生成
    output_text = "Directory Tree:\n" + tree_text + "\n\nFile Contents:\n" + files_text
    
    # クリップボードにコピー
    try:
        pyperclip.copy(output_text)
        print("ツリー表示とファイル内容がクリップボードにコピーされました。")
    except Exception as e:
        print("クリップボードへのコピーに失敗しました:", e)
    
    # ツリー表示を標準出力にも表示
    print("\n" + tree_text)

if __name__ == '__main__':
    main()
