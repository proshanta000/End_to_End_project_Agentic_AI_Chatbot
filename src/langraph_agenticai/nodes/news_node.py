from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import os
from src.langraph_agenticai.ui.uiconfigfile import Config

class NewsNodes:
    def __init__(self, llm, topicInput):
        self.tavily = TavilyClient()
        self.llm = llm
        self.topic = topicInput
        self.state = {}
        self.cfg = Config()

    def fetch_news(self, state: dict) -> dict:
        """Fetch news based on user frequency or handle greetings."""
        user_input = state['messages'][0].content.lower().strip()
        
        # --- NEW: GREETING CHECK ---
        # If the user says Hi, we set a flag and skip search
        if user_input in ["hi", "hello", "hey", "greetings"]:
            state['is_greeting'] = True
            state['news_data'] = []
            return state
        
        state['is_greeting'] = False
        frequency = user_input
        self.state['frequency'] = frequency
        
        time_range_map = {'daily' : 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 365}

        try:
            response = self.tavily.search(
                query=f'Top news about {self.topic}',
                topic='news',
                time_range=time_range_map.get(frequency, 'w'),
                include_answer='advanced',
                max_results=10,
                days=days_map.get(frequency, 7),
            )
            state['news_data'] = response.get('results', [])
        except Exception:
            state['news_data'] = []

        self.state['news_data'] = state['news_data']
        return state
    
    def summarize_news(self, state: dict) -> dict:
        """Summarize news as a MAX ceiling, allowing short responses."""
        # --- NEW: GREETING RESPONSE ---
        if state.get('is_greeting'):
            state['summary'] = "Hello! I'm ready to generate your news report. Please type a frequency like 'daily' or 'weekly' to begin."
            return state

        news_items = self.state.get('news_data', [])
        limit = self.cfg.get_word_limit() 

        # --- UPDATED PROMPT: "MAXIMUM" LOGIC ---
        system = f"""You are an expert News reporter.
        Summarize the news into a well-structured markdown report.
        
        CRITICAL LENGTH RULE: Your total response MUST NOT exceed {limit} words.
        This is a MAXIMUM limit. You are encouraged to be as brief and concise as possible. 
        If there is only one article or a simple greeting is needed, use very few words. 
        DO NOT add extra text or 'fluff' to try and reach the word limit.
        
        Format each item as:
        ### [Date] [Headline]
        [Summary Paragraph]
        **Source:** [Read more](Url)
        """
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system),
            ("user", "Articles found:\n{articles}")
        ])

        if not news_items:
            state['summary'] = f"No news found for '{self.topic}' in the requested timeframe."
            return state

        articles_str = "\n\n".join([
            f"Title: {item.get('title')}\nContent: {item.get('content')}\nURL: {item.get('url')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = response.content
        return state
    
    def saving_result(self, state: dict) -> dict:
        """Save results and update the UI message."""
        frequency = self.state.get('frequency', 'general')
        summary = state.get('summary', 'No summary generated.')
        limit = self.cfg.get_word_limit()
        
        # Don't save to file if it was just a greeting
        if state.get('is_greeting'):
            state['messages'] = [AIMessage(content=summary)]
            return state

        base_dir = os.getcwd()
        news_dir = os.path.join(base_dir, "News")
        os.makedirs(news_dir, exist_ok=True)
        filename = os.path.join(news_dir, f"{frequency}_summary.md")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(summary)
            state['messages'] = [AIMessage(content=f"✅ Report (Max: {limit} words):\n\n{summary}")]
        except Exception as e:
            state['messages'] = [AIMessage(content=f"❌ Error: {str(e)}")]

        return state