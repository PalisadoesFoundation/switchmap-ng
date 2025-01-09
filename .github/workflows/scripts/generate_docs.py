"""Script to generate and manage API documentation for the switchmap project.

This module handles the generation of API documentation using mkgendocs,
including cleaning up previous documentation, managing temporary files,
and preparing the documentation for Docusaurus integration.
"""

import os
import shutil
import subprocess
import glob


def clean_previous_docs():
    """Remove old documentation from the output directory.

    Args:
        None
    Returns:
        None
    """
    output_dir = "docs/auto-docs"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)


def clean_temp_files():
    """Remove intermediary files and directories.

    Args:
        None
    Returns:
        None
    """
    temp_dir = "docs-temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def update_gitignore():
    """Add temporary directory to .gitignore.

    Args:
        None
    Returns:
        None
    """
    gitignore_file = ".gitignore"
    temp_dir = "docs-temp"
    if os.path.exists(gitignore_file):
        with open(gitignore_file, "r") as file:
            lines = file.readlines()
        if temp_dir + "/" not in lines:
            lines.append(temp_dir + "/\n")
        with open(gitignore_file, "w") as file:
            file.writelines(lines)
    else:
        with open(gitignore_file, "w") as file:
            file.write(temp_dir + "/\n")


def generate_docs():
    """Generate documentation and prepare it for Docusaurus.

    Args:
        None
    Returns:
        None
    """
    input_dir = "switchmap"
    temp_dir = "docs-temp"
    output_dir = "docs/auto-docs"

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    subprocess.run(
        [
            "mkgendocs",
            "-i",
            input_dir,
            "-o",
            temp_dir,
        ],
        check=True,
    )

    for markdown_file in glob.glob(f"{temp_dir}/**/*.md", recursive=True):
        shutil.move(markdown_file, output_dir)

    clean_temp_files()


def main():
    """Main script execution.

    Args:
        None
    Returns:
        None
    """
    clean_previous_docs()
    generate_docs()
    update_gitignore()
    print("Documentation generated successfully!")


if __name__ == "__main__":
    main()
