from src.langraph_agenticai.state.state import State


class BasicChatbotNode:
    """
    Basic Chatbot logic implementation.
    Wraps the LLM interaction within a node structure for the graph.
    """

    def __init__(self, model):
        """
        Initialize the BasicChatbotNode.
        
        Args:
           model: The LLM model to use for generating responses.
        """
        self.llm = model

    def process(self, state:State) -> dict:
        """
        Processes the input state and generates a chatbot response.
        """
        return {"messages": self.llm.invoke(state['messages'])}