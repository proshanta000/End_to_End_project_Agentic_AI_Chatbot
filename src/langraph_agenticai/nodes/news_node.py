from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from src.langraph_agenticai.ui.streamlitui.loadui import LoadStreamlitUI


class NewsNodes:
    """
    Node responsible for fetching and summarizing user entered topic news using Tavily and an LLM.
    """
    def __init__(self, llm, topicInput):
        """
        Initialize the NewsNode with LLM and Tavily Client.
        
        Args:
            llm: The Language Model instance to use for summarization.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        self.topic = topicInput

        # Dictionary to store state/steps for potential debugging or history tracking
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch  news based on the specified frequency requested by the user.

        Args: 
            state (dict): The state dictionary containing the current conversation 'messages'.
        
        Returns:
            dict: Updated state with 'news_data' key containing the list of fetched news articles.
        """
        # Extract the user's requested frequency (e.g., "daily", "weekly")
        frequency = state['messages'][0].content.lower()
        self.state['frequency'] = frequency
        
        # Mappings to convert user frequency phrases to Tavily API parameters
        time_range_map = {'daily' : 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 365}

        # Perform the search using Tavily API
        # We query for top AI technology news in India and globally
        response = self.tavily.search(
            query=f'Top news about {self.topic}',
            topic='news',
            time_range=time_range_map.get(frequency, 'w'), # Default to weekly if match failed
            include_answer='advanced', # basic or advanced
            max_results=10,
            days=days_map.get(frequency, 7),
        )

        # Store results in the state
        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    
    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using the LLM into a readable markdown format.

        Args:
            state (dict): The state dictionary containing 'news_data'.

        Returns:
            dict: Updated state with 'summary' key containing the summarized markdown text.
        """
        news_items = self.state['news_data']

        # System prompt to guide the LLM's summarization style
        system = """You are an expert  News reporter.
        Summarize the provided  news articles into a well-structured markdown report.
        
        For each suitable news item:
        1. **Headline**: Create a clear, bold title.
        2. **Date**: Include the date in **YYYY-MM-DD** format (IST timezone if possible).
        3. **Summary**: Write a detailed yet concise paragraph (3-4 sentences) summarizing the key points. Do NOT just write a single line. Explain *why* it matters.
        4. **Source**: Provide the source URL as a separate line at the end of the item.

        **Format Guide**:
        ### [Date] [Headline]
        [Detailed Summary Paragraph]
        **Source:** [Read more](Url)
        
        Order the news by date (latest first).
        If multiple articles cover the same topic, combine them into one coherent summary.
        """
        
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                ("user", "Here are the articles found:\n{articles}")
            ]
        )

        # Format the news items into a single string for the prompt
        articles_str = "\n\n".join([
            f"Title: {item.get('title', 'Unknown Title')}\nContent: {item.get('content', '')} \nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        # Invoke the LLM to generate the summary
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        
        # Store the result in state (fixing previous variable name 'summery' -> 'summary')
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    

    def saving_result(self, state):
        """
        Save the summarized news to a markdown file.

        Args:
            state (dict): Current state containing 'frequency' and 'summary'.
        
        Returns:
            dict: Updated state with the 'filename' of the saved report.
        """
        frequency = self.state['frequency']
        summary = self.state['summary']
        filename = f"./News/{frequency}_summary.md"

        # Write to file with UTF-8 encoding to handle special characters correctly
        import os
        os.makedirs("./News", exist_ok=True) # Ensure directory exists
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {frequency.capitalize()}  News Summary\n\n")
            f.write(summary)
        
        self.state['filename'] = filename
        return self.state
