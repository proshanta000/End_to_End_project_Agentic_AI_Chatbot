from src.langraph_agenticai.state.state import State
from langchain_core.messages import SystemMessage
from src.langraph_agenticai.ui.uiconfigfile import Config

class ChatbotWithToolNode:
    def __init__(self, model):
        self.llm = model
        self.cfg = Config() # Initialize config to get the limit

    def create_chatbot(self, tools):
        # Bind tools to the model
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State) -> dict:
            messages = state["messages"]
            
            # 1. Get the dynamic limit from config.ini
            limit = self.cfg.get_word_limit()
            
            # 2. Updated System Constraint: Ceiling logic instead of Fixed logic
            # We explicitly tell the AI that short answers (like 'Hi') are perfect.
            constraint = SystemMessage(
                content=(
                    f"You are a helpful and concise assistant. "
                    f"MAXIMUM LIMIT: Your response must not exceed {limit} words. "
                    f"You are encouraged to be as brief as possible. If a one-word "
                    f"answer is appropriate (like a greeting), use only one word. "
                    f"Do not add unnecessary text to reach the word limit."
                )
            )
            
            # 3. Add the constraint to the messages being sent to the LLM
            llm_input = [constraint] + messages
            
            # 4. Invoke the LLM
            # Using the bound model that can call Tavily/other tools
            response = llm_with_tools.invoke(llm_input)
            
            # 5. Return the response to the graph state
            return {"messages": [response]}
        
        return chatbot_node