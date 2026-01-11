import streamlit as st
import os
from src.langraph_agenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langraph_agenticai.LLMS.groqllm import GroqLLM
from src.langraph_agenticai.LLMS.geminillm import GeminiLLM
from src.langraph_agenticai.graph.graph_builder import GraphBuilder
from src.langraph_agenticai.ui.streamlitui.display_result import DisplayResultStreamlit

def load_langgraph_agenticai_app():
    """ 
    Main entry point for the Streamlit application with Memory Persistence.
    """
    # --- 1. UI INITIALIZATION ---
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input.")
        return

    # --- 2. SESSION STATE MANAGEMENT ---
    if "topicInput" not in st.session_state:
        st.session_state.topicInput = ''
    
    selected_usecase = user_input.get('selected_usecase')
    user_message = None 

    # --- 3. USE CASE ROUTING ---
    if selected_usecase == 'Basic Chatbot':
        if not user_input.get('has_key'):
            st.info("ℹ️ Please provide an LLM API Key in the sidebar.")
        else:
            user_message = st.chat_input("Enter your message:")

    elif selected_usecase == 'Chatbot With Web':
        if not user_input.get('has_key') or not user_input.get('has_key_T'):
            st.info("ℹ️ Please provide both LLM and Tavily API Keys.")
        else:
            user_message = st.chat_input("Enter your message:")

    elif selected_usecase == 'News':
        if not user_input.get('has_key') or not user_input.get('has_key_T'):
            st.info("ℹ️ Please provide both LLM and Tavily API Keys.")
        else:
            topic_from_ui = user_input.get("news_topic", "").strip()
            st.markdown(f"### 🗓️ News Schedule")
            t_frame = st.selectbox("Select Research Frequency", ["Daily", "Weekly", "Monthly"])
            
            if st.button("🚀 Fetch & Generate Summary", use_container_width=True, type="primary"):
                if topic_from_ui:
                    st.session_state.topicInput = topic_from_ui
                    user_message = t_frame 
                else:
                    st.warning("⚠️ Please enter a topic first.")

    # --- 4. AGENTIC GRAPH EXECUTION ---
    if user_message:
        try:
            # 4.1 Initialize LLM Provider
            if user_input["selected_llm"] == "Groq":
                llm_provider = GroqLLM(user_controls_input=user_input)
            else:
                llm_provider = GeminiLLM(user_controls_input=user_input)
            
            model = llm_provider.get_llm_model()

            # 4.2 CACHE THE GRAPH OBJECT
            # This is critical! If we recreate the graph, memory is wiped.
            # We use a unique key per usecase.
            graph_session_key = f"graph_{selected_usecase}"
            
            if graph_session_key not in st.session_state:
                graph_builder = GraphBuilder(model=model, topicInput=st.session_state.topicInput)
                st.session_state[graph_session_key] = graph_builder.setup_graph(selected_usecase)
            
            # 4.3 Setup Display Handler with the Cached Graph
            with st.spinner(f"🤖 Processing..."):
                display_handler = DisplayResultStreamlit(
                    selected_usecase, 
                    st.session_state[graph_session_key], 
                    user_message
                )
                display_handler.display_result_on_ui()

        except Exception as e:
            st.error(f"❌ Application Error: {e}")

if __name__ == "__main__":
    load_langgraph_agenticai_app()