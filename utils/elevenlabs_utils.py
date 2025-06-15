import aiohttp
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = "seXpNd4yuPlnhV8r4bsu"  # ELI VOICE ID

async def generate_speech(text: str) -> str:
    """
    Generate speech from text using ElevenLabs API.
    Saves the audio to a local file and returns the file path.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    json_data = {
        "text": text,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.75
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data, headers=headers) as resp:
            if resp.status != 200:
                content = await resp.text()
                raise Exception(f"ElevenLabs TTS API error {resp.status}: {content}")
            audio_bytes = await resp.read()

    # Ensure Saved_Audio directory exists
    save_dir = "Saved_Audio"
    os.makedirs(save_dir, exist_ok=True)

    # Save audio to file
    save_path = os.path.join(save_dir, "response.mp3")
    with open(save_path, "wb") as f:
        f.write(audio_bytes)

    return save_path
