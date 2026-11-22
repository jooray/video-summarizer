import argparse
import os
import sys
from .config import Config
from .summarizer import Summarizer

# ChatOpenAI refuses an empty key. Ollama never checks it, so any non-empty
# placeholder will do when no OLLAMA_API_KEY is set.
NO_KEY_PLACEHOLDER = "ollama"


def get_api_key(config: Config) -> str:
    """Return the API key for the configured provider, or exit with a hint."""
    env_var = config.get_api_key_env()
    api_key = os.getenv(env_var)

    if api_key:
        return api_key
    if config.is_api_key_required():
        print(f"Error: {env_var} environment variable not set "
              f"(required for model_provider '{config.get_model_provider()}')")
        print(f"       export {env_var}=\"your-api-key-here\"")
        sys.exit(1)
    return NO_KEY_PLACEHOLDER


def main():
    parser = argparse.ArgumentParser(description="Video transcript summarizer")
    parser.add_argument("transcript_path", help="Path to the transcript file")
    parser.add_argument("--config", help="Path to config file",
                       default=os.path.expanduser("~/.video-summarizer.json"))
    parser.add_argument("--short_prompt", help="Custom short summary prompt")
    parser.add_argument("--detailed_prompt", help="Custom detailed summary prompt")
    parser.add_argument("--merge_prompt", help="Custom merge summary prompt")

    args = parser.parse_args()

    if not os.path.exists(args.transcript_path):
        print(f"Error: Transcript file '{args.transcript_path}' not found")
        sys.exit(1)

    with open(args.transcript_path, 'r') as f:
        transcript = f.read()

    try:
        config = Config(args.config)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Override prompts if provided via command line
    prompts = config.get_prompts()
    if args.short_prompt:
        prompts['short_summary'] = args.short_prompt
    if args.detailed_prompt:
        prompts['detailed_summary'] = args.detailed_prompt
    if args.merge_prompt:
        prompts['merge_summary'] = args.merge_prompt

    api_key = get_api_key(config)

    summarizer = Summarizer(
        transcript=transcript,
        prompts=prompts,
        context_size=config.get_context_size(),
        model=config.get_model_name(),
        api_key=api_key,
        api_base=config.get_api_base()
    )

    short_summary, detailed_summary = summarizer.summarize()
    print("Short Summary:")
    print(short_summary)
    print("\nDetailed Summary:")
    print(detailed_summary)

if __name__ == "__main__":
    main()
