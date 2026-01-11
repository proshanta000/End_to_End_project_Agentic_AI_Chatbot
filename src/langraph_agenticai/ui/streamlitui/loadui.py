import os
import streamlit as st
from src.langraph_agenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        raw_title = self.config.get_page_title()
        page_title = raw_title if raw_title else "Chat-Web-Brief AI"
        
        st.set_page_config(page_title="🤖 " + page_title, layout="wide")
        st.title("🧠 " + page_title)
        st.caption("A multi-agent framework powered by Groq and Gemini.")
        st.markdown("---") 

        # --- Sidebar ---
        with st.sidebar:
            st.markdown("## ⚙️ Configuration Settings")
            st.markdown("---")

            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            default_limit = self.config.get_word_limit()

            self.user_controls["selected_llm"] = st.selectbox("Select LLM Provider", llm_options)
            
            if self.user_controls["selected_llm"] == "Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("⚡️ Groq Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.text_input("🔑 Groq Key", type="password", value=st.session_state.get("GROQ_API_KEY", ""))
                st.session_state["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"]
            
            elif self.user_controls["selected_llm"] == "Gemini":
                model_options = self.config.get_gemini_model_options()
                self.user_controls["selected_gemini_model"] = st.selectbox("✨ Gemini Model", model_options)
                self.user_controls["GEMINI_API_KEY"] = st.text_input("🔑 Gemini Key", type="password", value=st.session_state.get("GEMINI_API_KEY", ""))
                st.session_state["GEMINI_API_KEY"] = self.user_controls["GEMINI_API_KEY"]

            st.markdown("---")

            # Usecase selection
            selected_usecase = st.selectbox("Select Application Usecase", usecase_options)
            self.user_controls["selected_usecase"] = selected_usecase

            # DYNAMIC LIMITATION UI (Updated to specify "Maximum")
            if selected_usecase == 'News':
                st.markdown("#### 📝 News Limits")
                self.user_controls["word_limit"] = st.number_input(
                    "Maximum Word Limit", 
                    min_value=10, # Lowered to allow very short reports
                    max_value=1000, 
                    value=default_limit,
                    help="The response will NOT exceed this length, but can be much shorter."
                )
            else:
                st.markdown("#### 💬 Chat Length")
                limit_range = [50, 100, 200, 300, 400, 500, 600, 700, 800]
                self.user_controls["word_limit"] = st.select_slider(
                    "Maximum Detail Level", 
                    options=limit_range, 
                    value=400,
                    help="Limits the maximum length. Short answers are allowed."
                )

            if selected_usecase in ["Chatbot With Web", "News"]:
                st.markdown("---")
                self.user_controls["TAVILY_API_KEY"] = st.text_input("🔍 Tavily Key", type="password", value=st.session_state.get("TAVILY_API_KEY", ""))
                st.session_state["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]
                if self.user_controls["TAVILY_API_KEY"]:
                    os.environ["TAVILY_API_KEY"] = self.user_controls["TAVILY_API_KEY"]

        # --- Main Page ---
        if selected_usecase == "News":
            st.subheader("📰 Generate News Report")
            self.user_controls["news_topic"] = st.text_input(
                "What topic do you want news about?", 
                placeholder="e.g. AI News",
                key="news_topic_main"
            )

        # Validation logic
        current_llm = self.user_controls.get("selected_llm")
        has_key = bool(st.session_state.get("GROQ_API_KEY") if current_llm == "Groq" else st.session_state.get("GEMINI_API_KEY"))
        has_key_T = bool(st.session_state.get("TAVILY_API_KEY")) if selected_usecase in ["Chatbot With Web", "News"] else True
        
        self.user_controls["has_key"] = has_key
        self.user_controls["has_key_T"] = has_key_T

        return self.user_controls