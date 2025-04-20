from mcp.server.fastmcp import FastMCP

# init FastMCP server
mcp = FastMCP("obsidian-mcp")


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
