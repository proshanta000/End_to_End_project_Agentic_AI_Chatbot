import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import os

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def extract_text_content(self, msg):
        """Extracts clean text from Gemini/Groq responses."""
        if msg is None: return ""
        if hasattr(msg, 'content'):
            content = msg.content
            return self._parse_list_content(content) if isinstance(content, list) else str(content).strip()
        if isinstance(msg, list): return self._parse_list_content(msg)
        if isinstance(msg, dict): return msg.get("text", str(msg)).strip()
        return str(msg).strip()

    def _parse_list_content(self, content_list):
        parts = []
        for block in content_list:
            if hasattr(block, 'content'): parts.append(str(block.content))
            elif isinstance(block, dict): parts.append(block.get("text", ""))
            elif isinstance(block, str): parts.append(block)
        return "".join(parts).strip()

    def display_result_on_ui(self):
        # 1. Define configuration with thread_id for memory retrieval
        # Using a fixed ID like "static_user" works for single-user apps.
        config = {"configurable": {"thread_id": "user_session_1"}}
        
        # 2. Prepare the input
        input_state = {"messages": [HumanMessage(content=self.user_message)]}

        # --- CASE 1: BASIC CHATBOT ---
        if self.usecase == "Basic Chatbot":
            with st.chat_message("user"):
                st.write(self.user_message)

            # Use stream with config to maintain memory
            for event in self.graph.stream(input_state, config=config):
                for value in event.values():
                    if "messages" in value:
                        # LangGraph returns a list of messages; we want the latest one
                        last_msg = value["messages"][-1]
                        clean_content = self.extract_text_content(last_msg)
                        if clean_content:
                            with st.chat_message("assistant"):
                                st.write(clean_content)

        # --- CASE 2: CHATBOT WITH WEB ---
        elif self.usecase == "Chatbot With Web":
            # Use invoke with config
            res = self.graph.invoke(input_state, config=config)
            
            for message in res.get('messages', []):
                content = self.extract_text_content(message)
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(content)
                elif isinstance(message, AIMessage):
                    # Filter internal tool steps
                    if "Page:" in content and "Summary:" in content:
                        continue 
                    if content:
                        with st.chat_message("assistant"):
                            st.write(content)

        # --- CASE 3: NEWS ---
        elif self.usecase == "News":
            with st.spinner("Generating News Report..."):
                res = self.graph.invoke(input_state, config=config)
                topic = st.session_state.get("topicInput", "news")
                NEWS_PATH = f"./News/{topic}_summary.md"
                
                if os.path.exists(NEWS_PATH):
                    with open(NEWS_PATH, "r", encoding='utf-8') as f:
                        st.markdown(f.read(), unsafe_allow_html=True)
                else:
                    st.warning("Report not found. Showing last AI message:")
                    if res and "messages" in res:
                        st.write(self.extract_text_content(res["messages"][-1]))