from src.langraph_agenticai.state.state import State
from langchain_core.messages import SystemMessage, AIMessage # Added AIMessage
from src.langraph_agenticai.ui.uiconfigfile import Config

class BasicChatbotNode:
    """
    Basic Chatbot logic implementation with a flexible word ceiling.
    """

    def __init__(self, model):
        self.llm = model
        self.cfg = Config()

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response.
        """
        # 1. Get the dynamic limit from config.ini
        limit = self.cfg.get_word_limit()

        # 2. Refined System Message
        # We ensure the instructions are clear so the LLM doesn't "freeze" 
        # trying to calculate exact word counts.
        constraint = SystemMessage(
            content=(
                f"You are a helpful assistant. "
                f"RULE: Your response must be under {limit} words. "
                f"Be direct and concise. Do not explain the word limit."
            )
        )

        # 3. Combine with history
        # We pull 'messages' specifically from the state
        current_messages = state.get("messages", [])
        messages_with_constraint = [constraint] + current_messages

        try:
            # 4. Invoke the LLM
            response = self.llm.invoke(messages_with_constraint)
            
            # --- THE FIX ---
            # If the response is empty or null, we provide a fallback 
            # so the graph always returns something to the UI.
            if not response.content or str(response.content).strip() == "":
                response = AIMessage(content="I'm sorry, I couldn't generate a response within that limit. Could you try a broader question?")

            # We MUST return the key 'messages' as a list [response]
            return {"messages": [response]}

        except Exception as e:
            # If the API fails, return the error so the UI shows it
            error_msg = AIMessage(content=f"Error: {str(e)}")
            return {"messages": [error_msg]}