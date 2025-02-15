from setuptools import setup, find_packages

setup(
    name="tree2clip",
    version="0.1.0",
    description="ディレクトリのツリー表示とファイル内容をクリップボードにコピーするツール",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pyperclip"
    ],
    entry_points={
        "console_scripts": [
            "tree2clip=tree2clip.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
