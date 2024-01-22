# Dependencies:
#pip install pyaudio
#pip install python-dotenv (if not already installed)

# Code modified from Deepgram Examples
# Still not finished (Wont run on my Desktop)

from dotenv import load_dotenv

import deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

def main():
    try:
        # Make a free account at deepgram.com to get an API key 
        # Create a Deepgram client using the API key from environment variables
        # (ie export DEEPGRAM_API_KEY="YOUR_API_KEY")
        deepgram = DeepgramClient()

        dg_connection = deepgram.listen.live.v("1")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            print(f"transcription: {sentence}")
            
        def on_error(self, error, **kwargs):
            print(f"\n\n{error}\n\n")

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Error, on_error)

        options = LiveOptions(
            smart_format=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
        )
        dg_connection.start(options)

        # Open a microphone stream
        microphone = Microphone(dg_connection.send)

        # start microphone
        microphone.start()

        # wait until finished
        input("Press Enter to stop recording...\n\n")

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        dg_connection.finish()

        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    main()
