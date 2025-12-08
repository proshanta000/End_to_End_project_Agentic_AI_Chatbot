import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    """
    Class to handle the display of results on the Streamlit UI based on the use case.
    """
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        """
        Routes the display logic to the appropriate UI component based on the selected usecase.
        """
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # Case 1: Basic Chatbot - Streams the response
        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages': ("user", user_message)}):
                print(event.values())
                for value in event.values():
                    print(value['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)


        # Case 2: Chatbot With Web - Search and Answer
        elif usecase=="Chatbot With Web":
            # Prepare state and invoke the graph
            initial_state = {"messages": [user_message]}
            res = graph.invoke(initial_state)
            
            # Display the conversation history
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user"):
                        st.write(message.content)
                elif type(message) == AIMessage and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
        

        # Case 3: News - Fetches and displays a markdown report
        elif usecase=="News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news.... ⏳"):
                # Invoke the graph to fetch and generate the news report
                # Wrap input in HumanMessage as the node expects to access .content from a message object
                result = graph.invoke({"messages": [HumanMessage(content=frequency)]})
                try:
                    # Read the markdown file (Note: Filename now uses 'summary', not 'summery')
                    NEWS_PATH = f"./News/{frequency}_summary.md"
                    
                    # Use UTF-8 encoding to ensure all characters (like emojis or special symbols) display correctly
                    with open(NEWS_PATH, "r", encoding='cp1252') as file:
                        markdown_content = file.read()

                        # Display the markdown content in streamlit
                        st.markdown(markdown_content, unsafe_allow_html= True)

                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {NEWS_PATH}")
                
                except Exception as e:
                    st.error(f"An error occured: {str(e)}")
                        