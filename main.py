import os
from pathlib import Path
from thefuzz import fuzz
from mcp.server.fastmcp import FastMCP

# constants
OBSIDIAN_PATH = os.getenv("OBSIDIAN", "")


# init FastMCP server
mcp = FastMCP("obsidian-mcp")


def get_markdown_files(path_str: str) -> list[str]:
    path = Path(path_str)

    if not os.stat(path):
        raise Exception(f"Invalid path: {path_str}")

    out_file_names = []
    for dir_path, _, file_names in os.walk(path):
        # ignore assets folder
        if "assets" in dir_path:
            continue

        for file_name in file_names:
            if file_name.endswith(".md"):
                out_file_names.append(os.path.join(dir_path, file_name))

    return out_file_names


def search_files(
    search_str: str, file_paths: list[str], match_threshold: int = 20
) -> list[str]:
    if len(file_paths) == 0:
        raise Exception("Empty list of files!")

    out_file_paths = []
    for file_path in file_paths:
        file_name = Path(file_path).name
        if fuzz.ratio(search_str, file_name) >= match_threshold:
            out_file_paths.append(file_path)

    # print(f"search string: {search_str}\n\noutput: {file_names}")

    return file_paths


@mcp.tool()
def list_file_paths(search_str: str) -> list[str] | str:
    """
    Fuzzy search through all markdown files in the Obsidian vault for the specified search string.
    Args:
        search_str: the string to search for

    Returns:
        list[str]: a list of file paths that match the search string
    """
    try:
        markdown_files = get_markdown_files(OBSIDIAN_PATH)
        return search_files(search_str, markdown_files)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read a file and output its content.
    Args:
        file_path: the path of the file to read

    Returns:
        str: the content of the file
    """
    try:
        with open(file_path, "r") as file:
            content = file.read()

        return content
    except Exception as e:
        return f"Error: {e}"


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
