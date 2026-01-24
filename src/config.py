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
        self.default_model_provider = "venice"
        self.provider_defaults = {
            "venice": {
                "api_base": "https://api.venice.ai/api/v1",
                "model": "llama-3.3-70b",
                "context_size": 128000
            },
            "ollama": {
                "api_base": "http://localhost:11434/v1",
                "model": "llama2",
                "context_size": 4096
            },
            "openai": {
                "api_base": "https://api.openai.com/v1",
                "model": "gpt-4",
                "context_size": 128000
            }
        }
        self.config = self.load_config()

    def load_config(self):
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        # Return defaults for Venice provider
        return {
            "prompts": self.default_prompts,
            "model_provider": self.default_model_provider,
            "context_size": self.provider_defaults["venice"]["context_size"],
            "model": self.provider_defaults["venice"]["model"],
            "api_base": self.provider_defaults["venice"]["api_base"]
        }

    def get_prompts(self):
        return self.config.get("prompts", self.default_prompts)

    def get_model_provider(self):
        return self.config.get("model_provider", self.default_model_provider)

    def get_context_size(self):
        provider = self.get_model_provider()
        default = self.provider_defaults.get(provider, self.provider_defaults["venice"])["context_size"]
        return self.config.get("context_size", default)

    def get_model_name(self):
        provider = self.get_model_provider()
        default = self.provider_defaults.get(provider, self.provider_defaults["venice"])["model"]
        return self.config.get("model", default)

    def get_api_base(self):
        provider = self.get_model_provider()
        default = self.provider_defaults.get(provider, self.provider_defaults["venice"])["api_base"]
        return self.config.get("api_base", default)
