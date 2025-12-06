from langgraph.graph import StateGraph, START, END
from src.langraph_agenticai.state.state import State
from src.langraph_agenticai.nodes.basic_chatbot_node import BasicChatbotNode


class GraphBuilder:
    """
    Class to build and manage the LangGraph state graph.
    """
    def __init__(self, model):
        """
        Initialize the GraphBuilder with a specific LLM model.
        
        Args:
            model: The LLM model instance to be used by the graph nodes.
        """
        self.llm = model
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

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """

        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        return self.graph_builder.compile()

        