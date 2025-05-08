import pyttsx3
import threading

class TTSManager:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        self.is_speaking = False
        self.lock = threading.Lock()

    def speak(self, text: str) -> None:
        """
        Speak the given text using text-to-speech.
        
        Args:
            text: Text to speak
        """
        with self.lock:
            if not self.is_speaking:
                self.is_speaking = True
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                finally:
                    self.is_speaking = False

    def stop(self) -> None:
        """Stop any ongoing speech"""
        with self.lock:
            if self.is_speaking:
                self.engine.stop()

# Global TTS manager instance
tts_manager = TTSManager()

def tts_play(text: str) -> None:
    """
    Play text using text-to-speech.
    
    Args:
        text: Text to speak
    """
    tts_manager.speak(text)

def tts_stop() -> None:
    """Stop any ongoing speech"""
    tts_manager.stop() 