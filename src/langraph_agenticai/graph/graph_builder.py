from langgraph.graph import StateGraph, START, END
from src.langraph_agenticai.state.state import State
from src.langraph_agenticai.nodes.basic_chatbot_node import BasicChatbotNode
from langgraph.prebuilt import tools_condition, ToolNode

# ADD THIS IMPORT
from langgraph.checkpoint.memory import MemorySaver 

from src.langraph_agenticai.tools.search_tool import get_tools, create_tool_node
from src.langraph_agenticai.nodes.chatbot_with_tools_node import ChatbotWithToolNode
from src.langraph_agenticai.nodes.news_node import NewsNodes


class GraphBuilder:
    def __init__(self, model, topicInput=None):
        self.llm = model
        self.topicInput = topicInput
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        self.basic_chatbot_node = BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_building_graph(self):
        tools = get_tools()
        tools_node = create_tool_node(tools)
        obj_chatbot_node = ChatbotWithToolNode(self.llm)
        chatbot_node = obj_chatbot_node.create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tools_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
            {"tools": "tools", END: END}
        )
        self.graph_builder.add_edge("tools", "chatbot")

    def news_builder_graph(self):
        news_node = NewsNodes(self.llm, self.topicInput)
        self.graph_builder.add_node("fetch_news", news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", news_node.summarize_news)
        self.graph_builder.add_node("save_result", news_node.saving_result)

        self.graph_builder.add_edge(START, "fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

    def setup_graph(self, usecase: str):
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools_building_graph()
        elif usecase == "News":
            self.news_builder_graph()
        
        # --- CRITICAL CHANGE START ---
        # 1. Initialize an in-memory checkpointer
        memory = MemorySaver()
        
        # 2. Compile the graph with the checkpointer enabled
        return self.graph_builder.compile(checkpointer=memory)
        # --- CRITICAL CHANGE END ---