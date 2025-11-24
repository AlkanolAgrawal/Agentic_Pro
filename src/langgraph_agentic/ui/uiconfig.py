import os
from configparser import ConfigParser

class UIConfig:
    def __init__(self, config_file=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = config_file or os.path.join(base_dir, "uiconfig.ini")
        self.config = ConfigParser()
        self.config.read(self.config_file)
    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(",")
    def get_usecase_options(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(",")
    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(",")
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")