import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# constants
OBSIDIAN_PATH = os.getenv("OBSIDIAN", "")


# init FastMCP server
mcp = FastMCP("obsidian-mcp")


def get_markdown_files(path_str: str) -> list[str] | str:
    try:
        path = Path(path_str)
    except Exception:
        return f"Invalid path: {path_str}"

    out_file_names = []
    for dir_path, _, file_names in os.walk(path):
        # ignore assets folder
        if "assets" in dir_path:
            continue

        for file_name in file_names:
            if file_name.endswith(".md"):
                out_file_names.append(os.path.join(dir_path, file_name))

    return out_file_names


@mcp.tool()
def list_file_names() -> list[str] | str:
    """List the names of the markdown files in the Obsidian vault"""
    return get_markdown_files(OBSIDIAN_PATH)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
