import aiohttp
import os

UPLOAD_DIR = "Saved_Audio"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

async def fetch_audio(recording_url: str) -> str:
    """
    Downloads the audio file from Twilio recording_url (with extension),
    saves to UPLOAD_DIR, and returns local path.
    """
    # Twilio's recording_url does NOT include file extension. Usually, add ".wav" or ".mp3"
    if not recording_url.endswith(".wav") and not recording_url.endswith(".mp3"):
        recording_url += ".wav"

    filename = recording_url.split("/")[-1]
    save_path = os.path.join(UPLOAD_DIR, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(recording_url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to download audio: {resp.status}")
            content = await resp.read()

    with open(save_path, "wb") as f:
        f.write(content)

    return save_path

def stream_audio_to_twilio(response_text: str) -> str:
    """
    Returns TwiML VoiceResponse string to say the response_text.
    """
    response = VoiceResponse()
    response.say(response_text, voice='alice', language='en-US')
    return str(response)
