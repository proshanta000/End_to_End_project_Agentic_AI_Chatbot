import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import os

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def extract_text_content(self, msg):
        """
        Extracts clean text from Gemini's list-based responses or standard objects.
        """
        if msg is None:
            return ""

        # 1. Handle standard LangChain Message objects (AIMessage/HumanMessage)
        if hasattr(msg, 'content'):
            content = msg.content
            if isinstance(content, list):
                return self._parse_list_content(content)
            return str(content).strip()

        # 2. Handle raw lists (Gemini's complex structure)
        if isinstance(msg, list):
            return self._parse_list_content(msg)

        # 3. Handle dictionaries
        if isinstance(msg, dict):
            return msg.get("text", str(msg)).strip()

        return str(msg).strip()

    def _parse_list_content(self, content_list):
        """Helper to extract 'text' from Gemini's part-list."""
        parts = []
        for block in content_list:
            if isinstance(block, dict):
                # Extract 'text' and ignore 'extras' or 'signatures'
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts).strip()

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # --- CASE 1: BASIC CHATBOT ---
        if usecase == "Basic Chatbot":
            with st.chat_message("user"):
                st.write(user_message)

            for event in graph.stream({'messages': [HumanMessage(content=user_message)]}):
                for value in event.values():
                    raw_msg = value.get("messages")
                    clean_content = self.extract_text_content(raw_msg)
                    if clean_content:
                        with st.chat_message("assistant"):
                            st.write(clean_content)

        # --- CASE 2: CHATBOT WITH WEB ---
        elif usecase == "Chatbot With Web":
            initial_state = {"messages": [HumanMessage(content=user_message)]}
            res = graph.invoke(initial_state)
            
            # Iterate through messages and filter out 'internal' search steps
            for message in res.get('messages', []):
                content = self.extract_text_content(message)
                
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(content)
                
                elif isinstance(message, AIMessage):
                    # FILTER: Skip internal search summaries (Page: ... Summary: ...)
                    if "Page:" in content and "Summary:" in content:
                        continue 
                    
                    # Display the actual assistant response
                    if content:
                        with st.chat_message("assistant"):
                            st.write(content)

        # --- CASE 3: NEWS ---
        elif usecase == "News":
            with st.spinner("Generating News Report..."):
                graph.invoke({"messages": [HumanMessage(content=user_message)]})
                
                topic = st.session_state.get("topicInput", "news")
                NEWS_PATH = f"./News/{topic}_summary.md"
                
                if os.path.exists(NEWS_PATH):
                    with open(NEWS_PATH, "r", encoding='utf-8') as f:
                        st.markdown(f.read(), unsafe_allow_html=True)
                else:
                    st.error("Summary file could not be located.")