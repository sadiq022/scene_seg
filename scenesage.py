import sys
import os
import time
import re
import json
import pysrt
import argparse
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Split SRT into scenes and analyze with LLM."
    )
    parser.add_argument(
        "filename",
        help="Subtitle file (.srt) (positional argument)"
    )
    parser.add_argument(
        "--model",
        default="meta-llama/llama-3.3-8b-instruct:free",
        help="Model name for OpenRouter/OpenAI API"
    )
    parser.add_argument(
        "--output",
        default="scenes.json",
        help="Filename for output JSON file"
    )
    return parser.parse_args()

def split_srt_into_scenes(filename, pause_threshold=4):
    subs = pysrt.open(filename, encoding='utf-8')
    scenes = []
    current_scene = {
        'start': None,
        'end': None,
        'transcript': []
    }

    for i, sub in enumerate(subs):
        start = sub.start
        end = sub.end
        text = sub.text.replace('\n', ' ').strip()
        

        if current_scene['start'] is None:
            current_scene['start'] = str(start)

        if current_scene['end'] is not None:
            # Calculate the pause (in seconds) between this and previous subtitle
            pause = (start.ordinal - prev_end.ordinal) / 1000.0
        else:
            pause = 0

        # If there is a pause >= threshold, end current scene and start new
        if pause >= pause_threshold:
            scenes.append({
                'start': current_scene['start'],
                'end': current_scene['end'],
                'transcript': ' '.join(current_scene['transcript'])
            })
            current_scene = {
                'start': str(start),
                'end': None,
                'transcript': []
            }

        current_scene['transcript'].append(text)
        current_scene['end'] = str(end)
        prev_end = end

    # Add the last scene
    if current_scene['transcript']:
        scenes.append({
            'start': current_scene['start'],
            'end': current_scene['end'],
            'transcript': ' '.join(current_scene['transcript'])
        })

    return scenes

def analyze_scene(transcript, client, model):
    prompt = (
        "Given the transcript below, extract the following in valid JSON:\n"
        "- summary: one-sentence summary\n"
        "- characters: list of characters mentioned\n"
        "- mood: overall mood or emotion\n"
        "- cultural_references: up to 3 references (e.g., famous works, genres, pop culture, tropes, or historical context)\n\n"
        f"Transcript:\n{transcript}\n"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content.strip()

    # Extract JSON from code block, even with a prefix or explanation before it
    match = re.search(r'```(?:json)?\s*([\s\S]+?)\s*```', content)
    if match:
        json_str = match.group(1)
    else:
        # If not in code block, try to find first { ... } as fallback
        match_brace = re.search(r'({[\s\S]+})', content)
        if match_brace:
            json_str = match_brace.group(1)
        else:
            json_str = content  # last resort

    try:
        data = json.loads(json_str)
    except Exception as e:
        print("Failed to parse response as JSON:", content)
        print("Error details:", e)
        data = {
            "summary": "",
            "characters": [],
            "mood": "",
            "cultural_references": []
        }

    return {
        "summary": data.get("summary", ""),
        "characters": data.get("characters", []),
        "mood": data.get("mood", ""),
        "cultural_references": data.get("cultural_references", [])
    }

if __name__ == "__main__":

    args = parse_args()
    filename = args.filename
    model = args.model
    output_file = args.output

    my_api_key = os.getenv("OPENROUTER_API_KEY")
    if not my_api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable not set")

    # --- 1. Split into scenes ---
    print("Splitting into scenes...")
    scenes = split_srt_into_scenes(filename)
    print(f"Found {len(scenes)} scenes.")

    # --- 2. Set up OpenAI/OpenRouter client ---
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=my_api_key,  # <--- PUT YOUR API KEY HERE
    )

    # --- 3. Analyze each scene ---
    analyzed_scenes = []
    for i, scene in enumerate(scenes):
        print(f"\nAnalyzing Scene {i+1}/{len(scenes)} ({scene['start']} - {scene['end']})...")
        analysis = analyze_scene(scene['transcript'], client, args.model)
        analyzed_scene = {
            "start": scene["start"],
            "end": scene["end"],
            "transcript": scene["transcript"],
            "summary": analysis.get("summary", ""),
            "characters": analysis.get("characters", []),
            "mood": analysis.get("mood", ""),
            "cultural_refs": analysis.get("cultural_references", [])
        }
        analyzed_scenes.append(analyzed_scene)
        time.sleep(1.5)  # Avoid hitting rate limits

    # Write all results to a JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analyzed_scenes, f, ensure_ascii=False, indent=2)
        print(f"Output saved to {output_file} file")
