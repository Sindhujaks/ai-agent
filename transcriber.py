import os
from faster_whisper import WhisperModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def transcribe_audio(audio_path):
    """
    Transcribe audio file using OpenAI's Whisper API (OpenAI Python 1.x+).
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    try:
        # Initialize OpenAI client
        model = WhisperModel("tiny", compute_type="int8")

        segments, info = model.transcribe(audio_path)
        full_text = " ".join([segment.text for segment in segments])
        return full_text
            
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}") 