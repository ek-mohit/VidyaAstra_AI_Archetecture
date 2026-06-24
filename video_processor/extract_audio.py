# extract_audio.py

import os
import subprocess


from .config import AUDIO_OUTPUT_DIR
from .utils import create_dir, get_filename_without_ext


def extract_audio(video_path):

    create_dir(AUDIO_OUTPUT_DIR)

    name = get_filename_without_ext(video_path)

    audio_path = os.path.join(
        AUDIO_OUTPUT_DIR,
        f"{name}.wav"
    )

    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        audio_path,
        "-y"
    ]

    subprocess.run(command, check=True)

    return audio_path