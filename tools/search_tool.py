from crewai.tools import tool
from duckduckgo_search import DDGS

@tool("DuckDuckGo Web Search")
def web_search_tool(query: str) -> str:
    """Searches the live web using DuckDuckGo and returns top search results."""
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
    return "\n---\n".join(results) if results else "No search results found."
