import os
from openai import OpenAI


def transcribe_audio(
    api_key,
    audio_path,
    model="whisper-1",
    language=None,
    prompt=None,
    response_format="json",
    temperature=0,
    timestamp_granularities=None,
):
    """
    Transcribe audio using the OpenAI Audio API, including specifying a model and additional parameters.
    """
    client = OpenAI(api_key=api_key)

    try:
        with open(audio_path, "rb") as audio_file:
            options = {
                "model": model,
                "response_format": response_format,
                "temperature": temperature,
            }

            if language:
                options["language"] = language
            if prompt:
                options["prompt"] = prompt
            if timestamp_granularities:
                options["timestamp_granularities[]"] = timestamp_granularities

            response = client.audio.transcriptions.create(file=audio_file, **options)
            transcription = response.text  # Accessing the text attribute directly
            return transcription

    except FileNotFoundError:
        return f"Error: Audio file not found at {audio_path}"
    except Exception as e:
        return f"Error: {e}"


def save_transcription_to_file(transcription):
    with open("Transcription.txt", "w") as file:
        file.write(transcription)


def main():
    api_key = os.getenv("API_KEY")  # Use environment variables for API keys
    if not api_key:
        error_message = (
            "Error: API key not found. Please set the API_KEY environment variable."
        )
        print(error_message)
        save_transcription_to_file(error_message)
        return

    audio_path = input(
        "Enter the path to your audio file (max 25MB): "
    )  # Obtain the audio file path from user input

    transcription = transcribe_audio(
        api_key=api_key,
        audio_path=audio_path,
        model="whisper-1",  # Use the available model "whisper-1"
        language="en",  # Set the language if known, e.g., "en" for English
        prompt=None,  # Optionally provide a prompt to guide the transcription
        response_format="json",  # Choose the desired response format
        temperature=0,  # Set the temperature for random sampling
        timestamp_granularities=None,  # Optionally specify timestamp granularities
    )

    print("Transcription or error message:")
    print(transcription)
    save_transcription_to_file(transcription)


if __name__ == "__main__":
    main()
