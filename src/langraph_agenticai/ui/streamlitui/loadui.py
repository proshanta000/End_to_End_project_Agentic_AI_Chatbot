import os
import streamlit as st
from src.langraph_agenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        # --- 1: Set page layout and title with a modern header ---
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        
        # Use a container for the main title to add a splash of color/style
        st.title("🧠 " + self.config.get_page_title())
        st.caption("A multi-agent framework powered by Groq and Gemini.")
        st.markdown("---") # Add a horizontal line for separation
        
        
        # --- 2: Structure the sidebar with headings and dividers ---
        with st.sidebar:
            st.markdown("## ⚙️ Configuration Settings")
            st.markdown("---") # Visual separation

            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()


            # LLM Provider Selection (e.g., Groq, Gemini)
            st.markdown("### 🤖 LLM Selection")
            self.user_controls["selected_llm"] = st.selectbox("Select LLM Provider", llm_options)
            st.markdown("---")


            # --- Dynamic Model & API Key Handling ---
            # Logic for Groq Selection
            if self.user_controls["selected_llm"] == "Groq":
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("⚡️ Select Groq Model", model_options)
                # API Key input placed in a specific container for better grouping
                with st.container(border=True):
                    self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("🔑 Groq API Key", type="password")

                # Validation API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API Key to proceed, Don't have? ref : https://console.groq.com/keys")
            
            # Logic for Gemini Selection
            elif self.user_controls["selected_llm"] == "Gemini":
                # Model selection
                model_options = self.config.get_gemini_model_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("✨ Select Gemini Model", model_options)
                # API Key input placed in a specific container for better grouping
                with st.container(border=True):
                    self.user_controls["GEMINI_API_KEY"] = st.session_state["GEMINI_API_KEY"]=st.text_input("🔑 Gemini API Key", type="password")

                # Validation API Key
                if not self.user_controls["GEMINI_API_KEY"]:
                    st.warning("⚠️ Please enter your Gemini API Key to proceed, Don't have? ref : https://aistudio.google.com/api-keys")

            st.markdown("---") # Visual separation between LLM and Usecase

            # Usecase selection
            st.markdown("### 🎯 Usecase Selection")
            self.user_controls["selected_usecase"] = st.selectbox("Select Application Usecase", usecase_options)
            st.markdown("---")

            # Tavily Api Key
            if self.user_controls["selected_usecase"] == "Chatbot With Web":
                st.markdown("#### 🌐 Web Search Integration")
                with st.container(border=True):
                    self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("🔍 Tavily API Key", type="password")


                if self.user_controls["TAVILY_API_KEY"]:
                    # Only set os.environ if the key is present
                    os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]
                else:
                    # Validation remains
                    st.warning("⚠️ Please enter your Tavily API Key to proceed, Don't have? ref : https://app.tavily.com/home")


            elif self.user_controls["selected_usecase"] == "News":
                # --- UI Improvement 3: Enhanced News Section ---
                st.markdown("#### 📰 News & Summary Generator")
                with st.container(border=True):
                    self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"]=st.text_input("🔍 Tavily API Key", type="password")
                
                if self.user_controls["TAVILY_API_KEY"]:
                    # Only set os.environ if the key is present
                    os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]
                else:
                    # Validation remains
                    st.warning("⚠️ Please enter your Tavily API Key to proceed, Don't have? ref : https://app.tavily.com/home")
                
                    
            
            # --- UI Improvement 4: Final Footer/Branding ---
            st.markdown("---")
            st.info("Built with LangGraph & Streamlit.")
        
        # 4. Validation Gate: Verify if an API Key is present before allowing data input
        current_llm = self.user_controls.get("selected_llm")
        current_usecase = self.user_controls.get("selected_usecase")
        has_key = False
        has_key_T = False

        if current_llm == "Groq":
            has_key = bool(st.session_state.get("GROQ_API_KEY"))

        elif current_llm == "Gemini":
            has_key = bool(st.session_state.get("GEMINI_API_KEY"))
        
        if current_usecase == "Chatbot With Web" or current_usecase == "News":
            has_key_T = bool(st.session_state.get("TAVILY_API_KEY"))
        
        self.user_controls["has_key"] = has_key
        self.user_controls["has_key_T"] = has_key_T


        return self.user_controls