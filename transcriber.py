import os
import requests


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
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"file": open(audio_path, "rb")}
    data = {"model": model}

    if language:
        data["language"] = language
    if prompt:
        data["prompt"] = prompt
    if response_format:
        data["response_format"] = response_format
    if temperature:
        data["temperature"] = temperature
    if timestamp_granularities:
        data["timestamp_granularities[]"] = timestamp_granularities

    try:
        response = requests.post(url, files=files, headers=headers, data=data)
        response.raise_for_status()  # This will raise an HTTPError for bad responses

        try:
            data = response.json()
            transcription = data.get("text", "No transcription found")
            return transcription
        except ValueError as e:
            print("Error decoding JSON:", e)
            print("Response content:", response.text[:500])
            return "Error: Non-JSON response received."
    except FileNotFoundError:
        return "Error: Audio file not found at " + audio_path
    except requests.exceptions.HTTPError as e:
        return "HTTP Error: " + str(e) + " | Response content: " + response.text[:500]
    except requests.exceptions.RequestException as e:
        return "Request failed: " + str(e)


def main():
    api_key = os.getenv(
        "API_KEY"
    )  # It's better to use environment variables for API keys
    audio_path = input(
        "Enter the path to your audio file (max 25MB): "
    )  # Dynamically obtain the audio file path
    model = "whisper-1"  # Use the available model "whisper-1"
    language = "en"  # Set the language if known, e.g., "en" for English
    prompt = None  # Optionally provide a prompt to guide the transcription
    response_format = "json"  # Choose the desired response format
    temperature = 0  # Set the temperature for random sampling
    timestamp_granularities = None  # Optionally specify timestamp granularities

    transcription = transcribe_audio(
        api_key,
        audio_path,
        model,
        language,
        prompt,
        response_format,
        temperature,
        timestamp_granularities,
    )
    print("Transcription or error message:")
    print(transcription)


if __name__ == "__main__":
    main()
