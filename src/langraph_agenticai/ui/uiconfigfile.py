import os
from configparser import ConfigParser

class Config:
    """
    Robust Configuration helper for Hugging Face (Linux) and Local (Windows).
    """
    def __init__(self, config_file=None):
        self.config = ConfigParser()
        
        if config_file is None:
            # 1. Dynamically find the path relative to this script
            # Works on both Windows and Linux/Hugging Face
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(current_dir, "uiconfigfile.ini")
        
        # 2. Check if file exists before reading
        if not os.path.exists(config_file):
            print(f"CRITICAL: Config file not found at {config_file}")
            # We don't crash here; the getter methods will handle the missing data
        else:
            self.config.read(config_file)

    def _get_list(self, key, default):
        """Helper to safely get a list from the config."""
        try:
            value = self.config["DEFAULT"].get(key)
            if value:
                return value.split(", ")
        except (KeyError, AttributeError):
            pass
        return default

    def get_llm_options(self):
        return self._get_list("LLM_OPTIONS", ["Groq", "Gemini"])
    
    def get_usecase_options(self):
        return self._get_list("USECASE_OPTIONS", ["Basic Chatbot", "Chatbot With Web", "News"])
    
    def get_groq_model_options(self):
        return self._get_list("GROQ_MODEL_OPTIONS", ["llama3-8b-8192", "mixtral-8x7b-32768"])
    
    def get_gemini_model_options(self):
        return self._get_list("GEMINI_MODEL_OPTIONS", ["gemini-1.5-flash", "gemini-1.5-pro"])
    
    def get_page_title(self):
        try:
            return self.config["DEFAULT"].get("PAGE_TITLE", "Chat-Web-Brief AI")
        except KeyError:
            return "Chat-Web-Brief AI"