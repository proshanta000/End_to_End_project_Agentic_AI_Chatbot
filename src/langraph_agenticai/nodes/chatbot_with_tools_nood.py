from src.langraph_agenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanceed with tool integration.
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state:State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        user_input = state["messages"][-1] if  state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "suer", "content": user_input}])

        # Simulate tool-specific logic
        tools_response = f"Tool integration for: '{user_input}"



        return {"messages": [llm_response, tools_response]}
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot node function bound to tools.
        The returned function is designed to be used as a node in LangGraph.
        """

        # 1. Bind the tools to the LLM 
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State) -> dict:
            """
            LangGraph Node: Takes the current state (message history) and 
            invokes the LLM bound with tools, returning the new AIMessage.
            
            Args:
                state: The current graph state containing the 'messages' history.
                
            Returns:
                A dictionary to update the state, containing the new AIMessage.
            """
            
            # The LangGraph state will contain a list of BaseMessage objects.
            messages = state["messages"]
            
            # 2. Invoke the LLM with the full message history
            llm_response = llm_with_tools.invoke(messages)
            
            # 3. Return the update dictionary to append the new AIMessage
            return {"messages": [llm_response]}
        
        return chatbot_node