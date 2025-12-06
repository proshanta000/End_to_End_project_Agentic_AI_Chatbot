import streamlit as st
from src.langraph_agenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langraph_agenticai.LLMS.groqllm import GroqLLM
from src.langraph_agenticai.LLMS.geminillm import GeminiLLM
from src.langraph_agenticai.graph.graph_buileder import GraphBuilder
from src.langraph_agenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """ 
    Loads and runs the Langgraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configurrs the LLM model,
    sets up the graph based on the seledted use case, and displays the output while 
    implementting exception handling for robustness.
    """

    # Load UI
    ui=LoadStreamlitUI()
    user_input =ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter Your message:")

    if user_message:
        try:
            # Configure LLM
            if user_input["selected_llm"] == "Groq":
                llm_model = GroqLLM(user_controls_input = user_input)
            elif user_input["selected_llm"] == "Gemini":
                llm_model = GeminiLLM(user_controls_input = user_input)
            obj_llm_config = llm_model
            model =obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return
            
            #Initialize and set up the graph based on use case
            usecase = user_input.get('selected_usecase')
            if not usecase:
                st.error("Error: No use case selected")
                return
            
            # Graph Builder
            graph_builder = GraphBuilder(model=model)

            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()

            except Exception as e:
                st.error(f"Error: Graph set up failed -{e}")
                return

        except Exception as e:
            st.error(f"Error: Graph set up failed -{e}")
            return
