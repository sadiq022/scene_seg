import unittest
from unittest.mock import MagicMock
import tempfile
import os

# Import your actual functions here
from scenesage import split_srt_into_scenes, analyze_scene

class TestSceneSage(unittest.TestCase):

    def setUp(self):
        # Multi-cue SRT content (NO leading spaces on lines)
        self.srt_content = """1
00:00:22,719 --> 00:00:26,759
Greetings, my friend. We are
all interested in the future,

2
00:00:26,860 --> 00:00:31,507
for that is where you and I
are going to spend the
rest of our lives.

3
00:00:31,507 --> 00:00:37,365
And remember my friend, future
events such as these will affect
you in the future.

4
00:00:37,971 --> 00:00:43,830
You are interested in the
unknown, the mysterious, the unexplainable.

5
00:00:43,830 --> 00:00:48,072
That is why you are here.
And now, for the first time,
"""
        # Write to a temporary file for testing
        self.tempfile = tempfile.NamedTemporaryFile(delete=False, suffix='.srt')
        self.tempfile.write(self.srt_content.encode('utf-8'))
        self.tempfile.close()

    def tearDown(self):
        os.unlink(self.tempfile.name)

    def test_split_srt_into_scenes(self):
        scenes = split_srt_into_scenes(self.tempfile.name, pause_threshold=4)
        self.assertEqual(len(scenes), 1)  # All cues merged due to no long pauses

        transcript = scenes[0]['transcript']

        expected_phrases = [
        "Greetings, my friend. We are all interested in the future,",
        "for that is where you and I are going to spend the rest of our lives.",
        "And remember my friend, future events such as these will affect you in the future.",
        "You are interested in the unknown, the mysterious, the unexplainable.",
        "That is why you are here. And now, for the first time,"
        ]

        for phrase in expected_phrases:
            self.assertIn(phrase, transcript)
        self.assertTrue(len(transcript) > 60)

    def test_analyze_scene(self):
        # Mock the LLM client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """
        {
            "summary": "A dramatic introduction to the theme of the future.",
            "characters": ["Narrator"],
            "mood": "Ominous",
            "cultural_references": ["Classic sci-fi opening", "Philosophical pondering"]
        }
        """
        mock_client.chat.completions.create.return_value = mock_response

        transcript = "Greetings, my friend. We are all interested in the future,"
        model = "test-model"
        result = analyze_scene(transcript, mock_client, model)
        self.assertEqual(result['summary'], "A dramatic introduction to the theme of the future.")
        self.assertEqual(result['characters'], ["Narrator"])
        self.assertEqual(result['mood'], "Ominous")
        self.assertIn("Classic sci-fi opening", result['cultural_references'])
        self.assertIn("Philosophical pondering", result['cultural_references'])

if __name__ == '__main__':
    unittest.main()