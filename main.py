from fastapi import FastAPI, Request, BackgroundTasks
app = FastAPI()
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
from utils.twilio_utils import fetch_audio, stream_audio_to_twilio
from utils.elevenlabs_utils import generate_speech
from utils.openai_utils import transcribe_audio, generate_response, summarize_transcript
from utils.db import save_lead_data
import uvicorn

import os

from fastapi import Query

@app.get("/process-audio/")
async def process_audio(filename: str = Query(..., description="Name of audio file in Saved_Audio")):
    audio_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(audio_path):
        return {"error": "File not found"}

    transcript = await transcribe_audio(audio_path)
    response_text = await generate_response(transcript)
    summary = await summarize_transcript(transcript)

    return {
        "transcript": transcript,
        "response": response_text,
        "summary": summary
    }



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "Saved_Audio"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/voice")
async def handle_call(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    call_sid = form.get("CallSid")
    recording_url = form.get("RecordingUrl")
    from_number = form.get("From")

    background_tasks.add_task(process_call, call_sid, recording_url, from_number)

    response = VoiceResponse()
    response.say("Thanks for calling. Please hold while we process your request.")
    return PlainTextResponse(str(response))

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

app.mount("/saved_audio", StaticFiles(directory=UPLOAD_DIR), name="saved_audio")


from fastapi import UploadFile, File

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    contents = await file.read()
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "path": save_path}



@app.get("/api/hello")
async def say_hello():
    return {"message": "Hello from backend!"}

@app.get("/")
def read_root():
    return {"message": "AI Caller Backend is running!"}


async def process_call(call_sid: str, recording_url: str, from_number: str):
    audio_path = await fetch_audio(recording_url)
    transcript = await transcribe_audio(audio_path)
    response_text = await generate_response(transcript)
    audio_response_path = await generate_speech(response_text)
    await stream_audio_to_twilio(call_sid, audio_response_path)
    summary = await summarize_transcript(transcript)
    await save_lead_data(call_sid, from_number, transcript, response_text, summary, recording_url)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
