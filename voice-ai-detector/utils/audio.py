import base64
import uuid


def save_audio(base64_string):

    if not base64_string:
        raise ValueError("Empty audio data")

    file_path = f"temp_{uuid.uuid4()}.mp3"

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base64_string))

    return file_path
