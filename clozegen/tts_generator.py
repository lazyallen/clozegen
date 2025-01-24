import asyncio
import hashlib
import os

from edge_tts import Communicate

from .config import Config

# TTS Constants from Config
TTS_DIR = Config.TTS_OUTPUT_DIR
TTS_VOICE = Config.TTS_VOICE_ID
MAX_RETRIES = Config.TTS_MAX_RETRIES
RETRY_DELAY = Config.TTS_RETRY_DELAY

# Create TTS directory if it doesn't exist
os.makedirs(TTS_DIR, exist_ok=True)


def generate_audio_filename(text: str) -> str:
    """Generate a unique filename for the audio file based on the text content."""
    hash_object = hashlib.md5(text.encode())
    return f"{hash_object.hexdigest()}.mp3"


async def generate_tts(text: str, filename: str, retries: int = MAX_RETRIES) -> bool:
    """Generate TTS audio file for the given text.

    Args:
        text: Text to convert to speech
        filename: Output audio file path
        retries: Number of retries on failure

    Returns:
        bool: True if generation successful, False otherwise
    """
    for attempt in range(retries):
        try:
            communicate = Communicate(text, TTS_VOICE)
            await communicate.save(filename)
            return True
        except Exception as e:
            if attempt == retries - 1:
                print(f"Failed to generate TTS after {retries} attempts: {str(e)}")
                return False
            await asyncio.sleep(RETRY_DELAY)
            continue
