from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from io import BytesIO
from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

class TTSRequest(BaseModel):
    text: str
    author: str

author_voices = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM"
}

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

@app.post("/generate")
def generate_audio(req: TTSRequest):
    text = req.text.strip()
    author = req.author

    if not text or author not in author_voices:
        raise HTTPException(status_code=400, detail="Invalid input")

    emotion = emotion_classifier(text)[0]['label']
    voice_id = author_voices[author]

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(f"{ELEVENLABS_API_URL}/{voice_id}/stream", headers=headers, json=data, stream=True)

    if response.status_code != 200:
        print("ERROR from ElevenLabs:")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        raise HTTPException(status_code=500, detail=f"TTS failed: {response.text}")

    return StreamingResponse(
        BytesIO(response.content),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=output.mp3"}
    )


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Serve built frontend from /app/frontend_dist
app.mount("/", StaticFiles(directory="frontend_dist", html=True), name="frontend")

# Optional: serve index.html on /
@app.get("/")
def read_index():
    index_path = os.path.join("frontend_dist", "index.html")
    return FileResponse(index_path)