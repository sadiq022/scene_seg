# Scene Sage 🎬

**Scene Sage** is a Python tool that splits a `.srt` subtitle file into scenes and analyzes each scene using a Large Language Model (LLM) via [OpenRouter](https://openrouter.ai/). It generates a summary, character list, mood, and cultural references for each scene—saving the result in a structured JSON file.

---

## Features

- **Automatic scene splitting:** Groups subtitles into scenes using time gaps (default: 4 seconds).
- **LLM-powered scene analysis:** Extracts summary, characters, mood, and cultural references using models like Meta Llama 3 or GPT-4o.
- **Easy output:** Results saved as a JSON file for further use or study.

## Installation

First, **clone this repository** to your local machine:

```bash
git clone https://github.com/sadiq022/scene_seg.git
cd scene_seg
```

Then, install all dependencies with: 
```bash
pip install -r requirements.txt
```
---

## Requirements

- Python 3.8 or newer
- [OpenRouter](https://openrouter.ai/) API key (free to create)
- A supported LLM model (Meta Llama 3.3 8B Instruct, GPT-4o, etc.)

## How to Get an OpenRouter API Key

1. **Sign Up or Log In**
   - Visit [https://openrouter.ai/](https://openrouter.ai/).
   - Click **Sign Up** in the top right corner and register using your email or a social login (Google, GitHub, etc).

2. **Create a New API Key**
   - Once logged in, click your profile icon/avatar in the upper-right corner.
   - Select **API Keys** from the dropdown menu.
   - Click the **Create Key** button.
   - (Optional) Give your API key a name (for your reference, e.g., "scene-sage").
   - Click **Create**.  
     The API key (a long string starting with `sk-`) will be shown only once.  
     **Copy this key now and keep it secure!** You will not be able to see it again.

3. **Choose a Model**
   - In the Models section or homepage, search for  
     **Meta: Llama 3.3 8B Instruct (free)**  
     This is a free model provided by OpenRouter and is ideal for getting started.
   - You can also use other models, like GPT-4o, if you have credits in your OpenRouter account.

4. **Save Your API Key Securely**
   - **Recommended:**  
     Create a file named `.env` in your project folder (do NOT share or commit this file).
     ```
     OPENROUTER_API_KEY=YourActualApiKeyHere
     ```
   - **Or:**  
     Set it as an environment variable in your shell/session:
       - **Linux/macOS:**  
         ```bash
         export OPENROUTER_API_KEY=sk-YourActualApiKeyHere
         ```
       - **Windows CMD:**  
         ```cmd
         set OPENROUTER_API_KEY=sk-YourActualApiKeyHere
         ```
       - **Windows PowerShell:**  
         ```powershell
         $env:OPENROUTER_API_KEY="sk-YourActualApiKeyHere"
         ```
   - **Never publish your API key or `.env` file online or in public code repositories.**

5. **Ready to Use**
   - The code in this project will automatically read your API key from the `.env` file or environment variable when you run the script. You do **not** need to edit the Python code to add your key.

### Python packages

- `pysrt`
- `openai`
- `python-dotenv`

## Usage

1. **Place your `.srt` subtitle file** (for example, `plan9.srt`) in your project directory.

2. **Run the script** from the command line:
   ```bash
   python scenesage.py plan9.srt --model meta-llama/llama-3.3-8b-instruct:free --output scenes.json

- The **first argument** is your subtitle file (required, positional).
- `--model` (optional): sets which LLM to use (default: `meta-llama/llama-3.3-8b-instruct:free`).
- `--output` (optional): sets the JSON file for saving the results (default: `scenes.json`).

## Output

The analysis for each scene will be saved in your output file (for example, `scenes.json`) as a list of JSON objects—one for each scene.

## Testing

Automated tests are included to ensure the reliability and correctness of this project.
Unit tests are provided in `test_scenesage.py`.
The tests cover:
- Scene splitting from `.srt` subtitle files using `split_srt_into_scenes`
- The scene analysis logic using `analyze_scene` (with LLM/API responses mocked)

Temporary subtitle files are created for testing, so no extra files are needed.
All tests use Python’s built-in `unittest` framework.

**Run the test script** from the command line:
```bash
python test_scenesage.py
