from pathlib import Path
import json

DEFAULT_PROVIDER = "venice"

# Per-provider defaults. Every value can be overridden in the config file.
#
# `context_size` is the maximum size of one chunk in *characters*, not tokens
# (RecursiveCharacterTextSplitter measures characters unless told otherwise).
# Roughly four characters per token, so keep it comfortably inside the context
# window the model is actually served with.
#
# Venice adds and retires model ids regularly - check
# https://api.venice.ai/api/v1/models before assuming one still exists.
PROVIDER_DEFAULTS = {
    "venice": {
        "api_base": "https://api.venice.ai/api/v1",
        "model": "deepseek-v4-flash",
        "context_size": 128000,
        "api_key_env": "VENICE_API_KEY",
        "api_key_required": True,
    },
    "ollama": {
        "api_base": "http://localhost:11434/v1",
        "model": "gemma4:12b",
        "context_size": 8192,
        "api_key_env": "OLLAMA_API_KEY",
        # Ollama ignores the key, but it runs behind its own auth proxies too.
        "api_key_required": False,
    },
    "openai": {
        "api_base": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "context_size": 128000,
        "api_key_env": "OPENAI_API_KEY",
        "api_key_required": True,
    },
}

SUPPORTED_PROVIDERS = tuple(PROVIDER_DEFAULTS)


class Config:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.default_prompts = {
            "short_summary": "Provide a concise summary of the video.",
            "detailed_summary": "Provide a detailed summary of the video, including key points and specific mentions.",
            "merge_summary": "Merge the following section summaries into a cohesive, well-structured detailed summary. Eliminate redundancy, organize information logically with clear headings, and ensure smooth transitions between sections. Maintain all important details while creating a unified narrative."
        }
        self.config = self.load_config()
        # Fail on an unsupported provider here, before any work is done.
        self.get_model_provider()

    def load_config(self):
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        # No config file: use the Venice defaults, which is what this tool did
        # before providers existed.
        venice = PROVIDER_DEFAULTS[DEFAULT_PROVIDER]
        return {
            "prompts": self.default_prompts,
            "model_provider": DEFAULT_PROVIDER,
            "context_size": venice["context_size"],
            "model": venice["model"],
            "api_base": venice["api_base"],
        }

    def get_model_provider(self):
        """Provider from the config, or Venice when the key is absent.

        Raises ValueError for an unsupported provider, so a typo fails with a
        readable message instead of silently falling back to Venice.
        """
        provider = str(self.config.get("model_provider", DEFAULT_PROVIDER)).strip().lower()
        if provider not in PROVIDER_DEFAULTS:
            raise ValueError(
                f"Unknown model_provider '{provider}'. "
                f"Supported providers: {', '.join(SUPPORTED_PROVIDERS)}"
            )
        return provider

    def _provider_default(self, key):
        """Provider-specific default for a configuration key."""
        return PROVIDER_DEFAULTS[self.get_model_provider()][key]

    def get_prompts(self):
        return self.config.get("prompts", self.default_prompts)

    def get_context_size(self):
        return self.config.get("context_size", self._provider_default("context_size"))

    def get_model_name(self):
        return self.config.get("model", self._provider_default("model"))

    def get_api_base(self):
        return self.config.get("api_base", self._provider_default("api_base"))

    def get_api_key_env(self):
        return self._provider_default("api_key_env")

    def is_api_key_required(self):
        return self._provider_default("api_key_required")
