import os
from os import PathLike
from time import time
import asyncio
from typing import Union
from dotenv import load_dotenv
import pygame
from pygame import mixer
import wikipediaapi  # Import the Wikipedia API module
from record import speech_to_text

# Load API keys
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize APIs
mixer.init()

class MockElevenlabs:
    @staticmethod
    def generate(*args, **kwargs):
        return "Mock generated response"

    @staticmethod
    def save(*args, **kwargs):
        pass

elevenlabs = MockElevenlabs()

conversation = {"Conversation": []}
RECORDING_PATH = "audio/recording.wav"

async def transcribe_audio(file_name: Union[Union[str, bytes, PathLike[str], PathLike[bytes]], int]):
    """Mock transcribe audio."""
    return [{"word": "mock"}]

def get_wikipedia_info(query: str):
    """Retrieve information from Wikipedia based on the given query."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)
    page_py = wiki_wiki.page(query)
    if page_py.exists():
        return page_py.summary[:300]  # Adjust the length of the summary as needed
    else:
        return "No information found on Wikipedia."

def log(log_text: str):
    """Print and write to status.txt"""
    print(log_text)
    with open("status.txt", "w") as f:
        f.write(log_text)

if __name__ == "__main__":
    while True:
        # Record audio
        log("Listening...")
        speech_to_text()
        log("Done listening")

        # Transcribe audio
        current_time = time()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        words = loop.run_until_complete(transcribe_audio(RECORDING_PATH))
        string_words = " ".join(
            word_dict.get("word") for word_dict in words if "word" in word_dict
        )
        with open("conv.txt", "a") as f:
            f.write(f"{string_words}\n")
        transcription_time = time() - current_time
        log(f"Finished transcribing in {transcription_time:.2f} seconds.")

        # Get information from Wikipedia
        current_time = time()
        wikipedia_info = get_wikipedia_info(string_words)
        wikipedia_time = time() - current_time
        log(f"Finished getting Wikipedia info in {wikipedia_time:.2f} seconds.")

        # Generate a mock response (you can replace this with the actual response)
        response = "Mock generated response"

        # Convert response to audio
        current_time = time()
        audio = elevenlabs.generate(
            text=response, voice="Adam", model="eleven_monolingual_v1"
        )
        elevenlabs.save(audio, "audio/response.wav")
        audio_time = time() - current_time
        log(f"Finished generating audio in {audio_time:.2f} seconds.")

        # Play response
        log("Speaking...")
        sound = mixer.Sound("audio/response.wav")
        with open("conv.txt", "a") as f:
            f.write(f"{response}\n")
        sound.play()
        pygame.time.wait(int(sound.get_length() * 1000))
        print(f"\n --- USER: {string_words}\n --- WIKIPEDIA: {wikipedia_info}\n --- JARVIS: {response}\n")
