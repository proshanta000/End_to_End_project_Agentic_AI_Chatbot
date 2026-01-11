from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langgraph.prebuilt import ToolNode
from langchain_community.tools import tool
from pydantic import BaseModel, Field

def get_tools():
    """
    Return the list of tools to be used in the chatbot.
    """
    
    # 1. Define input schema for tools
    # Renamed: WikipediaInput
    class WikipediaInput(BaseModel):
        query: str = Field(description="Search Query for wikipedia")

    class ArxivInput(BaseModel):
        query: str = Field(description="Search query for Arxiv")

    # 2. Create tools using the @tool decorator.
    @tool("wikipedia_search", args_schema=WikipediaInput)
    def wikipedia_search(query: str) -> str:
        """Search wikipedia for a given query and return the summary."""
        # Instantiate the wrapper each time the tool is called 
        _wikipedia_api_wrapper_instance = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=300)
        return _wikipedia_api_wrapper_instance.run(query)

    @tool("arxiv_search", args_schema=ArxivInput)
    def arxiv_search(query: str) -> str:
        """Search Arxiv for a given query and return the summary."""
        # Instantiate the wrapper each time the tool is called
        _arxiv_api_wrapper_instance = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=300)
        return _arxiv_api_wrapper_instance.run(query)

    # Tavily instance only created once
    Tavily = TavilySearchResults(max_results=2)

    tools = [wikipedia_search, arxiv_search, Tavily]
    return tools


# Renamed: create_tool_node
def create_tool_node(tools):
    """
    Create and returns a tool node for the graph
    """
    # The ToolNode will automatically handle routing the LLM's requests
    # to the correct tool function in the list.
    return ToolNode(tools=tools)