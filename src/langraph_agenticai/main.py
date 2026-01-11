import streamlit as st
import os
# Importing necessary modules for LLM providers, Graph building, and UI display
from src.langraph_agenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langraph_agenticai.LLMS.groqllm import GroqLLM
from src.langraph_agenticai.LLMS.geminillm import GeminiLLM
from src.langraph_agenticai.graph.graph_buileder import GraphBuilder
from src.langraph_agenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """ 
    Main entry point for the Streamlit application.
    Handles UI rendering, state management, and orchestration of the Agentic Graph.
    """

    # --- 1. UI INITIALIZATION ---
    # Initialize the UI class and render the sidebar/header
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    # --- 2. SESSION STATE MANAGEMENT ---
    # Streamlit reruns the whole script on every interaction. 
    # We use st.session_state to persist data across those reruns.
    if "timeframe" not in st.session_state:
        st.session_state.timeframe = ''
    if "topicInput" not in st.session_state:
        st.session_state.topicInput = ''
    if "ISFetchButtonClicked" not in st.session_state:
        st.session_state.ISFetchButtonClicked = False

    # Variable to hold the final prompt/message sent to the Agentic Graph
    user_message = None 

    # --- 3. USE CASE ROUTING ---
    selected_usecase = user_input.get('selected_usecase')

    # Case A: Basic Chatbot (Requires LLM Key)
    if selected_usecase == 'Basic Chatbot':
        if not user_input.get('has_key'):
            st.info("ℹ️ Please provide an LLM API Key in the sidebar to enable input.")
        else:
            # st.chat_input is a special Streamlit widget for chat interfaces
            user_message = st.chat_input("Enter Your message:")

    # Case B: Web-Enabled Chatbot (Requires LLM Key + Tavily Key)
    elif selected_usecase == 'Chatbot With Web':
        if not user_input.get('has_key') or not user_input.get('has_key_T'):
            st.info("ℹ️ Please provide both LLM and Tavily API Keys in the sidebar.")
        else:
            user_message = st.chat_input("Enter Your message:")

    # Case C: News Summary (Requires LLM Key + Tavily Key + Form Inputs)
    elif selected_usecase == 'News':
        if not user_input.get('has_key') or not user_input.get('has_key_T'):
            st.info("ℹ️ Please provide both LLM and Tavily API Keys in the sidebar.")
        else:
            st.markdown("### 📰 News Research")
            # We use standard text_input instead of chat_input for structured data
            t_input = st.text_input("📝 Enter News Topic:", value=st.session_state.topicInput)
            t_frame = st.selectbox("🗓️ Select Time Frame", ["Daily", "Weekly", "Monthly"])
            
            # Action button for the News use case
            if st.button("🚀 Fetch & Generate Summary", use_container_width=True, type="primary"):
                if t_input:
                    # Update session state so the Graph Builder can access the topic
                    st.session_state.ISFetchButtonClicked = True
                    st.session_state.topicInput = t_input
                    st.session_state.timeframe = t_frame
                    
                    # Formulate the trigger message for the agent
                    user_message = f"Summarize the latest news regarding '{t_input}' for the last {t_frame}."
                else:
                    st.warning("⚠️ Please enter a topic first.")

    # --- 4. AGENTIC GRAPH EXECUTION ---
    # If we have a message (either from chat_input or the News button), run the agent
    if user_message:
        try:
            # 4.1 Initialize the correct LLM Provider
            if user_input["selected_llm"] == "Groq":
                llm_provider = GroqLLM(user_controls_input=user_input)
            elif user_input["selected_llm"] == "Gemini":
                llm_provider = GeminiLLM(user_controls_input=user_input)
            
            # 4.2 Extract the actual model object (LangChain/Groq/Google object)
            model = llm_provider.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized. Check your API Keys.")
                return
            
            # 4.3 Build the Graph
            # We pass the model and the specific topic to the GraphBuilder
            graph_builder = GraphBuilder(model=model, topicInput=st.session_state.topicInput)
            
            # 4.4 Setup the Workflow
            # The setup_graph method usually defines nodes and edges based on the usecase
            graph = graph_builder.setup_graph(selected_usecase)
            
            # 4.5 Execute and Display
            # st.spinner provides a visual loading state while the LLM processes
            with st.spinner("🤖 Agentic system is processing your request..."):
                display_handler = DisplayResultStreamlit(selected_usecase, graph, user_message)
                display_handler.display_result_on_ui()

            # Optional: Reset the fetch button state so it doesn't re-run on next interaction
            st.session_state.ISFetchButtonClicked = False

        except Exception as e:
            # General error handling to prevent the whole app from crashing
            st.error(f"❌ An error occurred during graph execution: {e}")

# Entry point of the script
if __name__ == "__main__":
    load_langgraph_agenticai_app()