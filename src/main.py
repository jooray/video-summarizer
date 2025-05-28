import argparse
import os
import sys
from .config import Config
from .summarizer import Summarizer

def main():
    parser = argparse.ArgumentParser(description="Video transcript summarizer")
    parser.add_argument("transcript_path", help="Path to the transcript file")
    parser.add_argument("--config", help="Path to config file",
                       default=os.path.expanduser("~/.video-summarizer.json"))
    parser.add_argument("--short_prompt", help="Custom short summary prompt")
    parser.add_argument("--detailed_prompt", help="Custom detailed summary prompt")

    args = parser.parse_args()

    if not os.path.exists(args.transcript_path):
        print(f"Error: Transcript file '{args.transcript_path}' not found")
        sys.exit(1)

    with open(args.transcript_path, 'r') as f:
        transcript = f.read()

    config = Config(args.config)

    # Override prompts if provided via command line
    prompts = config.get_prompts()
    if args.short_prompt:
        prompts['short_summary'] = args.short_prompt
    if args.detailed_prompt:
        prompts['detailed_summary'] = args.detailed_prompt

    api_key = os.getenv('VENICE_API_KEY')
    if not api_key:
        print("Error: VENICE_API_KEY environment variable not set")
        sys.exit(1)

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
