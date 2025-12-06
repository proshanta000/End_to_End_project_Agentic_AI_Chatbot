import os
import streamlit as st
from src.langraph_agenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        st.header("🤖 " + self.config.get_page_title())

        with st.sidebar:
            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()


            # LLM Selecttion 
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                # Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"]=st.text_input("API Key", type="password")

                # Validation API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("⚠️ Please enter your GROQ API Key to proceed, Don't have? ref : https://console.groq.com/keys")
            
            elif self.user_controls["selected_llm"] == "Gemini":
                # Model selection
                model_options = self.config.get_gemini_model_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("Select Model", model_options)
                self.user_controls["GEMINI_API_KEY"] = st.session_state["GEMINI_API_KEY"]=st.text_input("API Key", type="password")

                # Validation API Key
                if not self.user_controls["GEMINI_API_KEY"]:
                    st.warning("⚠️ Please enter your Gemini API Key to proceed, Don't have? ref : https://aistudio.google.com/api-keys")

            # Usecase selection
            self.user_controls["selected_usecase"] = st.selectbox("Select Usecase", usecase_options)
        
        return self.user_controls