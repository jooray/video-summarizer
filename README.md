# Video Summarizer

AI-powered video transcript summarizer. It runs against [Venice AI](https://venice.ai) by default and can also use a local [Ollama](https://ollama.com) model or OpenAI — the client is LangChain's `ChatOpenAI`, so any OpenAI-compatible chat endpoint works. This tool processes video transcripts and generates both concise and detailed summaries.

<!-- jooray-links:start -->
### More from me

**Related projects**

- [venice-frontend](https://github.com/jooray/venice-frontend): alternative Venice.ai front-end for image, video and chat
- [venice-image](https://github.com/jooray/venice-image): generate images with the Venice API from the command line
- [hermes-venice-model-switcher](https://github.com/jooray/hermes-venice-model-switcher): DIEM-aware model switcher for Hermes Agent on Venice
- [venice-e2ee-proxy](https://github.com/jooray/venice-e2ee-proxy): local proxy adding end-to-end encryption to Venice requests
- [hermes-firewall](https://github.com/jooray/hermes-firewall): prompt-injection gate for Hermes Agent

**Full project showcase:** Part of [Venice Tools](https://juraj.bednar.io/showcase/#AI-05) in my project showcase, or [all my projects](https://juraj.bednar.io/showcase/).

I write about building things on [my blog](https://juraj.bednar.io/en/blog-en/). I also wrote a cypherpunk novel, [Tamers of Entropy](https://tamersofentropy.net/), and there is a [trailer](https://tamersofentropy.net/#trailer).
<!-- jooray-links:end -->

To get the transcripts, use [whisper-file](https://gist.github.com/jooray/22559480fecbe38444080c208b715cce) or [yt-whisper](https://gist.github.com/jooray/b7266366dbc2f0c162542cf9927768f9).

## Supported providers

| Provider | Runs on | Cost | API key |
|----------|---------|------|---------|
| **Venice AI** (default) | Venice cloud | paid per token | `VENICE_API_KEY` |
| **Ollama** | your own machine | free | not needed |
| **OpenAI** | OpenAI cloud | paid per token | `OPENAI_API_KEY` |

The provider is chosen with `model_provider` in the config file. A config without that key keeps using Venice, so existing setups need no changes.

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- A Venice AI key, an OpenAI key, or Ollama running locally

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

3. **Pick a provider.**

   #### Venice AI (the default)

   ```bash
   export VENICE_API_KEY="your-api-key-here"
   ```

   Or add it to your shell profile (`.bashrc`, `.zshrc`, etc.):
   ```bash
   echo 'export VENICE_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

   #### Ollama (local, free, private)

   Install Ollama from [ollama.com](https://ollama.com/download), then pull a model:

   ```bash
   ollama pull gemma4:12b      # default in the example config, ~8 GB
   ollama serve                # usually already running
   ```

   `gemma4:e4b` is the lighter option if 12b is too big for the machine.

   No API key is involved. Point the tool at it in the config file:

   ```json
   {
     "model_provider": "ollama",
     "model": "gemma4:12b",
     "context_size": 8192,
     "api_base": "http://localhost:11434/v1"
   }
   ```

   #### OpenAI

   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

   and set `"model_provider": "openai"` in the config file.

4. **Create the configuration file:**

   ```bash
   cp video-summarizer.json-example ~/.video-summarizer.json
   # Edit the config file to select your provider and customize settings
   ```

   With no config file at all, the tool uses the Venice defaults.

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
  --detailed_prompt "Provide a bullet-point summary with timestamps" \
  --merge_prompt "Combine these summaries into a unified report"

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
| `model_provider` | string | `"venice"` | `venice`, `ollama` or `openai` |
| `model` | string | provider-specific | Model name to use for summarization |
| `context_size` | integer | provider-specific | Maximum size of one chunk, in characters |
| `api_base` | string | provider-specific | OpenAI-compatible API base URL |
| `prompts.short_summary` | string | Basic short summary prompt | Prompt for generating concise summaries |
| `prompts.detailed_summary` | string | Basic detailed summary prompt | Prompt for generating comprehensive summaries |
| `prompts.merge_summary` | string | Basic merge prompt | Prompt for merging multiple chunk summaries into a cohesive detailed summary |

`context_size` is measured in **characters**, not tokens — `RecursiveCharacterTextSplitter` counts characters, and roughly four of them make a token. A transcript longer than that is split into chunks, each summarized separately and then merged.

`api_base` accepts any OpenAI-compatible endpoint, so a local proxy or a different host works without code changes.

### Provider Defaults

| Provider | Model | `context_size` | `api_base` |
|----------|-------|----------------|------------|
| **Venice AI** | `deepseek-v4-flash` | 128000 | `https://api.venice.ai/api/v1` |
| **Ollama** | `gemma4:12b` | 8192 | `http://localhost:11434/v1` |
| **OpenAI** | `gpt-4o-mini` | 128000 | `https://api.openai.com/v1` |

These are starting points, not recommendations. Venice retires model ids regularly — the old example default `mistral-31-24b` no longer exists — so if a run fails on the model, list what your account can use with `curl -H "Authorization: Bearer $VENICE_API_KEY" https://api.venice.ai/api/v1/models?type=text` and update `model`.

For Ollama, `context_size` also has to fit the context Ollama actually serves for that model (`OLLAMA_CONTEXT_LENGTH`, or `num_ctx` per model). The stock default is small, so keep chunks modest or raise both together — a chunk that does not fit is silently truncated by the server, not by this tool.

### Example Configurations

#### Venice AI

```json
{
  "model_provider": "venice",
  "model": "deepseek-v4-flash",
  "context_size": 128000,
  "api_base": "https://api.venice.ai/api/v1",
  "prompts": {
    "short_summary": "Provide a concise summary of this video transcript in 2-3 sentences.",
    "detailed_summary": "Provide a comprehensive summary with key points and insights.",
    "merge_summary": "Merge the following summaries into a cohesive detailed summary."
  }
}
```

#### Ollama

```json
{
  "model_provider": "ollama",
  "model": "gemma4:12b",
  "context_size": 8192,
  "api_base": "http://localhost:11434/v1",
  "prompts": {
    "short_summary": "Provide a concise summary of this video transcript in 2-3 sentences.",
    "detailed_summary": "Provide a comprehensive summary with key points and insights.",
    "merge_summary": "Merge the following summaries into a cohesive detailed summary."
  }
}
```

#### OpenAI

```json
{
  "model_provider": "openai",
  "model": "gpt-4o-mini",
  "context_size": 128000,
  "api_base": "https://api.openai.com/v1",
  "prompts": {
    "short_summary": "Provide a concise summary of this video transcript in 2-3 sentences.",
    "detailed_summary": "Provide a comprehensive summary with key points and insights.",
    "merge_summary": "Merge the following summaries into a cohesive detailed summary."
  }
}
```

### Environment Variables

| Variable | Required for | Description |
|----------|--------------|-------------|
| `VENICE_API_KEY` | Venice AI | Your Venice AI API key |
| `OPENAI_API_KEY` | OpenAI | Your OpenAI API key |
| `OLLAMA_API_KEY` | Ollama (optional) | Only needed if something in front of Ollama demands a key |

A missing required key stops the run with an error naming the variable to set. Ollama runs without one.

## Command Line Options

```
usage: video-summarizer [-h] [--config CONFIG] [--short_prompt SHORT_PROMPT]
                        [--detailed_prompt DETAILED_PROMPT]
                        [--merge_prompt MERGE_PROMPT]
                        transcript_path

Video transcript summarizer

positional arguments:
  transcript_path       Path to the transcript file

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to config file
  --short_prompt SHORT_PROMPT
                        Custom short summary prompt
  --detailed_prompt DETAILED_PROMPT
                        Custom detailed summary prompt
  --merge_prompt MERGE_PROMPT
                        Custom merge summary prompt
```

## Support and value4value

If you like this project, I would appreciate if you contributed time, talent or treasure.

Time and talent can be used in testing it out, fixing bugs, spreading the word.

Treasure can be [sent back through here](https://juraj.bednar.io/en/support-me/).


## License

This project is licensed under the [GLWTSPL](https://github.com/me-shaon/GLWTPL/blob/master/NSFW_LICENSE)
