from pathlib import Path
import json

class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.default_prompts = {
            "short_summary": "Provide a concise summary of the video.",
            "detailed_summary": "Provide a detailed summary of the video, including key points and specific mentions.",
            "merge_summary": "Merge the following section summaries into a cohesive, well-structured detailed summary. Eliminate redundancy, organize information logically with clear headings, and ensure smooth transitions between sections. Maintain all important details while creating a unified narrative."
        }
        self.default_context_size = 128000
        self.default_model_name = "gpt-3.5-turbo"
        self.default_api_base = "https://api.venice.ai/api/v1"
        self.config = self.load_config()

    def load_config(self):
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "prompts": self.default_prompts,
            "context_size": self.default_context_size,
            "model": self.default_model_name,
            "api_base": self.default_api_base
        }

    def get_prompts(self):
        return self.config.get("prompts", self.default_prompts)

    def get_context_size(self):
        return self.config.get("context_size", self.default_context_size)

    def get_model_name(self):
        return self.config.get("model", self.default_model_name)

    def get_api_base(self):
        return self.config.get("api_base", self.default_api_base)
