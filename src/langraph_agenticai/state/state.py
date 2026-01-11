from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    Represents the shared memory (state) of the LangGraph workflow.
    Each key holds specific data that nodes can read from or write to.
    """

    # 'messages' stores the conversation history. 
    # The 'Annotated' with 'add_messages' ensures that when a node returns a message,
    # it is APPENDED to the existing list rather than overwriting it.
    messages: Annotated[list, add_messages]

    # 'news_data' stores the raw list of articles found by the Tavily search tool.
    # This acts as a temporary storage before the news is summarized.
    news_data: list

    # 'summary' holds the final markdown-formatted string produced by the NewsNode.
    # This is what gets saved to the .md file and displayed to the user.
    summary: str

    # 'filename' stores the path to the saved report (e.g., 'News/daily_summary.md').
    # Useful if you want to provide a download link in the UI later.
    filename: str