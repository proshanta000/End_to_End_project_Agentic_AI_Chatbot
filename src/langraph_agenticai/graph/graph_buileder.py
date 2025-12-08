from langgraph.graph import StateGraph, START, END
from src.langraph_agenticai.state.state import State
from src.langraph_agenticai.nodes.basic_chatbot_node import BasicChatbotNode
from langgraph.prebuilt import tools_condition, ToolNode

from src.langraph_agenticai.tools.search_tool import get_tools, create_tool_node
from src.langraph_agenticai.nodes.chatbot_with_tools_nood import ChatbotWithToolNode
from src.langraph_agenticai.nodes.news_node import NewsNodes


class GraphBuilder:
    """
    Class to build and manage the LangGraph state graph.
    """
    def __init__(self, model, topicInput=None):
        """
        Initialize the GraphBuilder with a specific LLM model.
        
        Args:
            model: The LLM model instance to be used by the graph nodes.
            topicInput: The topic for news search (optional).
        """
        self.llm = model
        self.topicInput = topicInput
        self.graph_builder=StateGraph(State)


    def basic_chatbot_build_graph(self):
        """
         Builds a basic chatbot graph using Langgraph.
         This method initializes a chatbot node using the 'BasicChatbotNode' class
         and in interagets it into the graph. The chatbot node is set as both the 
         entry and exit point of the graph.
        """
        self.basic_chatbot_build_node = BasicChatbotNode(self.llm)
        # --- node ---
        # Add the chatbot node to the graph
        self.graph_builder.add_node("chatbot",self.basic_chatbot_build_node.process )

        # --- edge ---
        # Define the flow: Start -> Chatbot -> End
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def chatbot_with_tools_building_graph(self):
        """
        BUilds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. it defines tools, initializes the chatbot with tool
        capabilities, and sets up conditional and direct edges between nodes.
        The chatbot node is set the entry point.
        """

        # Define the tool and tool node
        tools = get_tools()
        tools_node = create_tool_node(tools)

        # Define the llm 
        llm = self.llm

        # Define the chatbot node
        obj_chatbot_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_node.create_chatbot(tools)

        # --- node ---
        # Add the chatbot node to the graph
        self.graph_builder.add_node("chatbot",chatbot_node )
        self.graph_builder.add_node("tools", tools_node)

        # --- edge ---
        # Define the flow: Start -> Chatbot -><- tools -> End
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
            {"tools": "tools", END: END}
        )
        self.graph_builder.add_edge("tools", "chatbot")

    def news_builder_graph(self):

        # Define the llm 
        llm = self.llm
        topic = self.topicInput

        # Define the AI news chatbot node
        news_node=NewsNodes(llm, topic)

        # --- node ---
        # Add the chatbot node to the graph
        self.graph_builder.add_node("fetch_news", news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", news_node.summarize_news)
        self.graph_builder.add_node("save_result", news_node.saving_result)

        # --- edge ---
        # Define the flow: Start -> fetch_news -> summarize_news -> save_result -> End
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)



    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """

        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools_building_graph()
        
        elif usecase == "News":
            self.news_builder_graph()
        
        return self.graph_builder.compile()

        