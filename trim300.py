input_file = "plan9.srt"
output_file = "plan9_new.srt"
max_cues = 300

with open(input_file, encoding='utf-8') as f:
    data = f.read()

cues = data.strip().split('\n\n')  # Each cue is separated by a blank line
subset = cues[:max_cues]

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(subset))
    f.write('\n')  # Ensure file ends with newline