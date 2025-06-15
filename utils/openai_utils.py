import asyncio
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def transcribe_audio(audio_path: str) -> str:
    print(f">> Transcribing audio from {audio_path} ...")

    loop = asyncio.get_event_loop()

    def sync_transcribe():
        try:
            with open(audio_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=audio_file,
                    model="whisper-1"
                )
            return transcription.text
        except Exception as e:
            print(f"[Transcription Error] {e}")
            return ""

    transcript = await loop.run_in_executor(None, sync_transcribe)
    print(">> Transcript:", transcript[:60])
    return transcript

async def generate_response(prompt: str) -> str:
    print(">> Generating GPT response...")

    loop = asyncio.get_event_loop()

    def sync_generate():
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            print(">> Received GPT response")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Generation Error] {e}")
            return ""

    response = await loop.run_in_executor(None, sync_generate)
    print(">> Response:", response[:60])
    return response


async def summarize_transcript(transcript: str) -> str:
    print(">> Summarizing transcript...")

    loop = asyncio.get_event_loop()

    def sync_summarize():
        prompt = (
            "Summarize this customer call transcript briefly highlighting key points and intent:\n\n"
            + transcript
        )
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You summarize customer call transcripts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.3,
            )
            print(">> Summary generated")
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Summarization Error] {e}")
            return ""

    summary = await loop.run_in_executor(None, sync_summarize)
    print(">> Summary:", summary[:60])
    return summary
