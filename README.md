# Scene Sage 🎬

**Scene Sage** is a Python tool that splits a `.srt` subtitle file into scenes and analyzes each scene using a Large Language Model (LLM) via [OpenRouter](https://openrouter.ai/). It generates a summary, character list, mood, and cultural references for each scene—saving the result in a structured JSON file.

---

## Features

- **Automatic scene splitting:** Groups subtitles into scenes using time gaps (default: 4 seconds).
- **LLM-powered scene analysis:** Extracts summary, characters, mood, and cultural references using models like Meta Llama 3 or GPT-4o.
- **Easy output:** Results saved as a JSON file for further use or study.

---

## Requirements

- Python 3.8 or newer
- [OpenRouter](https://openrouter.ai/) API key (free to create)
- A supported LLM model (Meta Llama 3.3 8B Instruct, GPT-4o, etc.)

### Python packages

- `pysrt`
- `openai`
- `python-dotenv`

Install everything with:
```bash
pip install -r requirements.txt
