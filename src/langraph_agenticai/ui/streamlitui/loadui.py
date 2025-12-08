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
        st.title("🧠 LangGraph Agentic AI Interface")
        st.caption("A multi-agent framework powered by Groq and Gemini.")
        st.markdown("---") # Add a horizontal line for separation
        
        # Initialize session state variables if they don't exist
        if "timeframe" not in st.session_state:
            st.session_state.timeframe = ''
        if "topicInput" not in st.session_state:
            st.session_state.topicInput = ''
        if "ISFetchButtonClicked" not in st.session_state:
            st.session_state.ISFetchButtonClicked = False
        
        # --- 2: Structure the sidebar with headings and dividers ---
        with st.sidebar:
            st.markdown("## ⚙️ Configuration Settings")
            st.markdown("---") # Visual separation

            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()


            # LLM Selecttion 
            st.markdown("### 🤖 LLM Selection")
            self.user_controls["selected_llm"] = st.selectbox("Select LLM Provider", llm_options)
            st.markdown("---")


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
                
                # Removed redundant subheader here, using markdown above
                topic_input = st.text_input("📝 Enter News Topic:")

                # Moved time_frame selector to a separate container or just ensure good spacing
                time_frame = st.selectbox(
                    "🗓️ Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0
                )
                
                if topic_input:
                    # Use a success/primary button style for better visibility
                    if st.button("🚀 Fetch & Generate Summary", use_container_width = True, type="primary"): 
                        st.session_state.ISFetchButtonClicked =True
                        st.session_state.timeframe = time_frame
                        st.session_state.topicInput = topic_input
                else:
                    # Validation remains
                    st.warning("⚠️ Topic is empty, Please enter the Topic")
            
            # --- UI Improvement 4: Final Footer/Branding ---
            st.markdown("---")
            st.info("Built with LangGraph & Streamlit.")


        return self.user_controls