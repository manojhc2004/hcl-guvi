from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from utils.audio import process_audio, cleanup_files
from model.detector import detect_voice

app = FastAPI()

API_KEY = "sk_guvi_hcl_2026"

ALLOWED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]


class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/api/voice-detection")
def voice_detection(request: VoiceRequest, x_api_key: str = Header(None)):

    # ✅ API KEY
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # ✅ format check
    if request.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Only MP3 allowed")

    # ✅ language check
    if request.language not in ALLOWED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Unsupported language")

    mp3_path, wav_path = process_audio(request.audioBase64)

    try:
        classification, confidence, explanation = detect_voice(wav_path)

        return {
            "status": "success",
            "language": request.language,
            "classification": classification,
            "confidenceScore": confidence,
            "explanation": explanation
        }

    finally:
        cleanup_files(mp3_path, wav_path)
