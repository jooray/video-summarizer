# Video Summarizer

AI-powered video transcript summarizer using Venice AI API (you can alternatively use different API that is OpenAI compatible). This tool processes video transcripts and generates both concise and detailed summaries.

To get the transcripts, use [whisper-file](https://gist.github.com/jooray/22559480fecbe38444080c208b715cce) or [yt-whisper](https://gist.github.com/jooray/b7266366dbc2f0c162542cf9927768f9).

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- Venice AI API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jooray/video-summarizer
   cd video-summarizer
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Set up your Venice AI API key:**
   ```bash
   export VENICE_API_KEY="your-api-key-here"
   ```
   
   Or add it to your shell profile (`.bashrc`, `.zshrc`, etc.):
   ```bash
   echo 'export VENICE_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Create configuration file (optional):**
   ```bash
   cp video-summarizer.json-example ~/.video-summarizer.json
   # Edit the config file to customize prompts and settings
   ```

## Usage

### Basic Usage

```bash
# Using poetry script
poetry run video-summarizer path/to/transcript.txt

# Or using python directly
poetry run python src/main.py path/to/transcript.txt
```

### Advanced Usage

```bash
# Use custom config file
poetry run video-summarizer transcript.txt --config /path/to/custom-config.json

# Override prompts via command line
poetry run video-summarizer transcript.txt \
  --short_prompt "Summarize this video in one sentence" \
  --detailed_prompt "Provide a bullet-point summary with timestamps"

# Combine custom config and prompt overrides
poetry run video-summarizer transcript.txt \
  --config ./my-config.json \
  --short_prompt "Custom short summary prompt"
```

## Configuration

The tool uses a JSON configuration file to customize behavior. By default, it looks for `~/.video-summarizer.json`.

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `prompts.short_summary` | string | Basic short summary prompt | Prompt for generating concise summaries |
| `prompts.detailed_summary` | string | Basic detailed summary prompt | Prompt for generating comprehensive summaries |
| `context_size` | integer | 128000 | Maximum tokens per chunk for processing |
| `model` | string | "mistral-31-24b" | Model name to use for summarization |

### Example Configuration

```json
{
  "prompts": {
    "short_summary": "Provide a concise summary of this video transcript in 2-3 sentences, highlighting the main topic and key takeaways.",
    "detailed_summary": "Analyze this video transcript and provide a comprehensive summary that includes: 1) Main topics discussed, 2) Key points and insights, 3) Important quotes or specific mentions, 4) Any actionable items or conclusions. Structure your response with clear headings and bullet points where appropriate."
  },
  "context_size": 128000,
  "model": "mistral-31-24b"
}
```

## Command Line Options

```
Usage: video-summarizer [OPTIONS] TRANSCRIPT_PATH

  Summarize video transcripts using Venice API (or another OpenAI compatible API).

Arguments:
  TRANSCRIPT_PATH  Path to the video transcript file  [required]

Options:
  --short_prompt TEXT      Custom prompt for short summary
  --detailed_prompt TEXT   Custom prompt for detailed summary
  --config PATH            Path to custom configuration file
  --help                   Show this message and exit.
```

## Support and value4value

If you like this project, I would appreciate if you contributed time, talent or treasure.

Time and talent can be used in testing it out, fixing bugs, spreading the word.

Treasure can be [sent back through here](https://juraj.bednar.io/en/support-me/).


## License

This project is licensed under the [GLWTSPL](https://github.com/me-shaon/GLWTPL/blob/master/NSFW_LICENSE)
