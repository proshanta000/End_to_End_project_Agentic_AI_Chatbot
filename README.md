---
title: ChatLens AI
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
license: mit
---

# ChatLens AI: Chat, Search & Summarize

**Chat, search, and summarize news with agentic AI.**

This application is an all-in-one information assistant built using **LangGraph** and **Google Gemini**. It features three distinct "agentic" modes to help you stay informed and productive.

## 🚀 Features

* **Basic Chat**: Direct conversational AI for brainstorming and quick answers.
* **Chat with Web**: Agentic search integration to find real-time data and verify facts.
* **News Summarization**: Automated scraping and summarization of the latest news on any topic.

## 🛠️ Technology Stack

* **Framework**: [LangGraph](https://www.langchain.com/langgraph) (for stateful agent orchestration)
* **LLM**: [Google Gemini 1.5](https://deepmind.google/technologies/gemini/)
* **UI**: [Streamlit](https://streamlit.io/)
* **Search**: Tavily / DuckDuckGo API

## 📖 How to Use

1.  **Select a Mode**: Use the sidebar to choose between Basic Chat, Web Search, or News.
2.  **Enter your Query**: Type your message or the news topic you want to explore.
3.  **Get Results**: The agent will process your request, browse the web if needed, and provide a concise summary under 400 words.

## 🔑 Environment Variables

To run this space, you need to add the following secrets in your Space Settings:
* `GOOGLE_API_KEY`: Your Gemini API Key.
* `TAVILY_API_KEY`: (Optional) If using Tavily for web search.

---
Built with ❤️ using LangGraph and Streamlit.
