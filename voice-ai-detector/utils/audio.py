import base64
import uuid
import os
from pydub import AudioSegment

from pydub import AudioSegment
AudioSegment.converter = "ffmpeg"

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)


def process_audio(audio_base64: str):

    file_id = str(uuid.uuid4())

    mp3_path = f"{TEMP_DIR}/{file_id}.mp3"
    wav_path = f"{TEMP_DIR}/{file_id}.wav"

    # decode
    audio_bytes = base64.b64decode(audio_base64)

    with open(mp3_path, "wb") as f:
        f.write(audio_bytes)

    # convert
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

    return mp3_path, wav_path


def cleanup_files(*paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
