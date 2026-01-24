# Video Summarizer

AI-powered video transcript summarizer supporting multiple AI providers (Venice AI, Ollama, OpenAI). This tool processes video transcripts and generates both concise and detailed summaries.

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

## Supported AI Providers

| Provider | Privacy | Cost | Setup Difficulty | API Key Required |
|----------|---------|------|------------------|------------------|
| **Ollama** | Local/Private | Free | Easy | No |
| **Venice AI** | Cloud | Paid | Easy | Yes |
| **OpenAI** | Cloud | Paid | Easy | Yes |

## Installation

### Prerequisites

- Python 3.11 or higher
- Poetry (for dependency management)
- An API key for your chosen provider (Venice AI or OpenAI), or Ollama installed locally

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

3. **Choose and configure your AI provider:**

   #### Option 1: Ollama (Local, Private, Free)
   
   **Install Ollama:**
   ```bash
   # On macOS or Linux
   curl -fsSL https://ollama.com/install.sh | sh
   
   # On Windows, download from https://ollama.com/download
   ```
   
   **Pull a model:**
   ```bash
   # For general use (4GB RAM required)
   ollama pull llama2
   
   # For better quality (8GB RAM required)
   ollama pull llama3.1
   
   # For highest quality (48GB RAM required)
   ollama pull llama3.3:70b
   ```
   
   **No API key needed for Ollama!**

   #### Option 2: Venice AI (Cloud, Paid)
   
   ```bash
   export VENICE_API_KEY="your-api-key-here"
   ```
   
   Or add it to your shell profile (`.bashrc`, `.zshrc`, etc.):
   ```bash
   echo 'export VENICE_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

   #### Option 3: OpenAI (Cloud, Paid)
   
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   Or add it to your shell profile:
   ```bash
   echo 'export OPENAI_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Create configuration file:**
   ```bash
   cp video-summarizer.json-example ~/.video-summarizer.json
   # Edit the config file to select your provider and customize settings
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
| `model_provider` | string | "venice" | AI provider to use: "venice", "ollama", or "openai" |
| `model` | string | Provider-specific | Model name to use for summarization |
| `context_size` | integer | Provider-specific | Maximum tokens per chunk for processing |
| `api_base` | string | Provider-specific | API base URL (auto-configured per provider) |
| `prompts.short_summary` | string | Default prompt | Prompt for generating concise summaries |
| `prompts.detailed_summary` | string | Default prompt | Prompt for generating comprehensive summaries |
| `prompts.merge_summary` | string | Default prompt | Prompt for merging multiple chunk summaries |

### Provider-Specific Defaults

| Provider | Default Model | Default Context Size | Default API Base |
|----------|---------------|---------------------|------------------|
| **Venice AI** | llama-3.3-70b | 128,000 | https://api.venice.ai/api/v1 |
| **Ollama** | llama2 | 4,096 | http://localhost:11434/v1 |
| **OpenAI** | gpt-4 | 128,000 | https://api.openai.com/v1 |

### Example Configurations

#### Venice AI Configuration
```json
{
  "model_provider": "venice",
  "model": "llama-3.3-70b",
  "context_size": 128000,
  "api_base": "https://api.venice.ai/api/v1",
  "prompts": {
    "short_summary": "Provide a concise summary of this video transcript in 2-3 sentences.",
    "detailed_summary": "Provide a comprehensive summary with key points and insights.",
    "merge_summary": "Merge the following summaries into a cohesive detailed summary."
  }
}
```

#### Ollama Configuration
```json
{
  "model_provider": "ollama",
  "model": "llama2",
  "context_size": 4096,
  "api_base": "http://localhost:11434/v1",
  "prompts": {
    "short_summary": "Provide a concise summary of this video transcript in 2-3 sentences.",
    "detailed_summary": "Provide a comprehensive summary with key points and insights.",
    "merge_summary": "Merge the following summaries into a cohesive detailed summary."
  }
}
```

**Ollama Model Context Sizes:**
- `llama2`: 4,096 tokens
- `llama3.1`: 128,000 tokens  
- `llama3.3:70b`: 128,000 tokens
- `mistral`: 8,192 tokens
- `mixtral`: 32,768 tokens

**Note:** Adjust `context_size` based on the model you're using with Ollama.

#### OpenAI Configuration
```json
{
  "model_provider": "openai",
  "model": "gpt-4",
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

| Variable | Required For | Description |
|----------|-------------|-------------|
| `VENICE_API_KEY` | Venice AI | Your Venice AI API key |
| `OPENAI_API_KEY` | OpenAI | Your OpenAI API key |
| `OLLAMA_API_KEY` | Ollama (optional) | Optional API key for Ollama (usually not needed) |

## Command Line Options

```
Usage: video-summarizer [OPTIONS] TRANSCRIPT_PATH

  Summarize video transcripts using your configured AI provider (Venice AI, Ollama, or OpenAI).

Arguments:
  TRANSCRIPT_PATH  Path to the video transcript file  [required]

Options:
  --short_prompt TEXT      Custom prompt for short summary
  --detailed_prompt TEXT   Custom prompt for detailed summary
  --merge_prompt TEXT      Custom prompt for merging chunk summaries
  --config PATH            Path to custom configuration file (default: ~/.video-summarizer.json)
  --help                   Show this message and exit.
```

## Support and value4value

If you like this project, I would appreciate if you contributed time, talent or treasure.

Time and talent can be used in testing it out, fixing bugs, spreading the word.

Treasure can be [sent back through here](https://juraj.bednar.io/en/support-me/).


## License

This project is licensed under the [GLWTSPL](https://github.com/me-shaon/GLWTPL/blob/master/NSFW_LICENSE)
