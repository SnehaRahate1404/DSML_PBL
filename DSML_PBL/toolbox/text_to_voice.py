import edge_tts
import asyncio
import os
import pygame
import tempfile

async def text_to_speech(text, voice='en-US-AriaNeural'):
    try:
        # Create a Communicate instance with the text and voice
        communicate = edge_tts.Communicate(text, voice)
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            file_path = temp_audio.name
            await communicate.save(file_path)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(1)
        
        # Stop playback
        pygame.mixer.music.stop()
        
        # Ensure the file is not in use before deleting
        pygame.mixer.quit()
        
        # Delete the temporary file
        os.remove(file_path)
        
    except edge_tts.exceptions.NoAudioReceived as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

voice_list=["en-IN-PrabhatNeural","ar-EG-SalmaNeural","en-US-AriaNeural"]

