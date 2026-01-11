import os
import streamlit as st
from src.langraph_agenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        # --- 1: Set page layout and title with defensive fallbacks ---
        # Fetch the title once and ensure it's not None
        raw_title = self.config.get_page_title()
        page_title = raw_title if raw_title else "Chat-Web-Brief AI"
        
        # st.set_page_config must be the first streamlit command called
        st.set_page_config(page_title="🤖 " + page_title, layout="wide")
        
        # Use the 'page_title' variable to avoid NoneType concatenation
        st.title("🧠 " + page_title)
        st.caption("A multi-agent framework powered by Groq and Gemini.")
        st.markdown("---") 
        
        # --- 2: Structure the sidebar with headings and dividers ---
        with st.sidebar:
            st.markdown("## ⚙️ Configuration Settings")
            st.markdown("---")

            # Get options from config with safety fallbacks for lists
            llm_options = self.config.get_llm_options() or ["Groq", "Gemini"]
            usecase_options = self.config.get_usecase_options() or ["Basic Chatbot", "Chatbot With Web", "News"]

            # LLM Provider Selection
            st.markdown("### 🤖 LLM Selection")
            self.user_controls["selected_llm"] = st.selectbox("Select LLM Provider", llm_options)
            st.markdown("---")

            # --- Dynamic Model & API Key Handling ---
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options() or ["llama3-8b-8192"]
                self.user_controls["selected_groq_model"] = st.selectbox("⚡️ Select Groq Model", model_options)
                
                with st.container(border=True):
                    # Using .get() for session_state to avoid KeyErrors
                    existing_key = st.session_state.get("GROQ_API_KEY", "")
                    self.user_controls["GROQ_API_KEY"] = st.text_input("🔑 Groq API Key", type="password", value=existing_key)
                    st.session_state["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"]

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API Key to proceed.")
            
            elif self.user_controls["selected_llm"] == "Gemini":
                model_options = self.config.get_gemini_model_options() or ["gemini-1.5-flash"]
                self.user_controls["selected_gemini_model"] = st.selectbox("✨ Select Gemini Model", model_options)
                
                with st.container(border=True):
                    existing_key = st.session_state.get("GEMINI_API_KEY", "")
                    self.user_controls["GEMINI_API_KEY"] = st.text_input("🔑 Gemini API Key", type="password", value=existing_key)
                    st.session_state["GEMINI_API_KEY"] = self.user_controls["GEMINI_API_KEY"]

                if not self.user_controls["GEMINI_API_KEY"]:
                    st.warning("⚠️ Please enter your Gemini API Key to proceed.")

            st.markdown("---")

            # Usecase selection
            st.markdown("### 🎯 Usecase Selection")
            self.user_controls["selected_usecase"] = st.selectbox("Select Application Usecase", usecase_options)
            st.markdown("---")

            # Tavily Api Key Handling
            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "News"]:
                label = "🌐 Web Search" if self.user_controls["selected_usecase"] == "Chatbot With Web" else "📰 News Generator"
                st.markdown(f"#### {label}")
                
                with st.container(border=True):
                    existing_tavily = st.session_state.get("TAVILY_API_KEY", "")
                    self.user_controls["TAVILY_API_KEY"] = st.text_input("🔍 Tavily API Key", type="password", value=existing_tavily)
                    st.session_state["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]

                if self.user_controls["TAVILY_API_KEY"]:
                    os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]
                else:
                    st.warning("⚠️ Please enter your Tavily API Key to proceed.")

            st.markdown("---")
            st.info("Built with LangGraph & Streamlit.")
        
        # --- 3. Validation Gate ---
        current_llm = self.user_controls.get("selected_llm")
        current_usecase = self.user_controls.get("selected_usecase")
        
        has_key = False
        has_key_T = True # Default to True unless a search usecase is selected

        if current_llm == "Groq":
            has_key = bool(st.session_state.get("GROQ_API_KEY"))
        elif current_llm == "Gemini":
            has_key = bool(st.session_state.get("GEMINI_API_KEY"))
        
        if current_usecase in ["Chatbot With Web", "News"]:
            has_key_T = bool(st.session_state.get("TAVILY_API_KEY"))
        
        self.user_controls["has_key"] = has_key
        self.user_controls["has_key_T"] = has_key_T

        return self.user_controls