from fastapi import FastAPI, Header, HTTPException
from model.detector import detect_voice
from utils.audio import save_audio
import os

app = FastAPI()

API_KEY = "sk_test_123456"

SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]


@app.post("/api/voice-detection")
def voice_detection(data: dict, x_api_key: str = Header(None)):

    try:
        # ✅ API KEY CHECK
        if x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")

        # ✅ LANGUAGE CHECK
        if data.get("language") not in SUPPORTED_LANGUAGES:
            raise HTTPException(status_code=400, detail="Unsupported language")

        # ✅ AUDIO CHECK
        if not data.get("audioBase64"):
            raise HTTPException(status_code=400, detail="Audio data missing")

        # ✅ SAVE AUDIO
        audio_path = save_audio(data.get("audioBase64"))

        # ✅ DETECT VOICE
        classification, score, explanation = detect_voice(audio_path)

        # ✅ DELETE TEMP FILE (VERY IMPORTANT)
        if os.path.exists(audio_path):
            os.remove(audio_path)

        # ✅ RESPONSE FORMAT (Matches Hackathon)
        return {
            "status": "success",
            "language": data["language"],
            "classification": classification,
            "confidenceScore": round(score, 2),
            "explanation": explanation
        }

    # ✅ Let FastAPI handle real HTTP errors
    except HTTPException:
        raise

    # ✅ Catch unexpected crashes
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Invalid or corrupted audio file"
        )

