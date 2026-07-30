# 🩺 Voicebot Doctor — AI Medical Vision Assistant

A voice-driven medical assistant that listens to a patient's spoken symptoms, looks at an uploaded medical image, and returns a structured AI-generated diagnosis — spoken back out loud. Built with Gradio, Google Gemini (vision), Whisper (speech-to-text), and gTTS (text-to-speech).

## How it works

1. **Speak your symptoms** into the microphone and **upload a medical image** (e.g. a skin condition photo).
2. Your voice is transcribed to text using **Faster-Whisper**.
3. The image + transcribed query are sent to **Gemini** (`gemini-3-flash-preview`) with a structured output schema.
4. Gemini returns a structured diagnosis: detected issue, description, severity, recommendations, whether to consult a doctor, a confidence score, and a spoken-friendly response.
5. The spoken response is converted back to audio with **gTTS** and played back automatically.

All of this is wrapped in a simple **Gradio** UI.

## Features

- 🎙️ **Voice input** — record symptoms directly from the browser microphone
- 🖼️ **Image analysis** — upload a photo for visual diagnosis (e.g. skin conditions)
- 🧠 **Structured AI diagnosis** — Gemini returns a typed, structured response (not free text) via a Pydantic schema
- 🔊 **Spoken response** — the AI's response is read back out loud
- 🖥️ **Simple web UI** — built with Gradio, no separate frontend needed

## Tech Stack

| Purpose | Technology |
|---|---|
| UI | Gradio |
| Speech-to-Text | Faster-Whisper |
| Vision + Diagnosis LLM | Google Gemini (`gemini-3-flash-preview`) via `google-genai` |
| Text-to-Speech | gTTS |
| Structured output validation | Pydantic |
| Env management | python-dotenv |

## Project Structure

```
.
├── app.py               # Gradio UI + main pipeline (audio + image -> diagnosis)
├── llm.py                # Gemini vision model call (ask_vision_model)
├── models.py             # Medical_Response schema (Pydantic)
├── speech_to_text.py     # Whisper-based transcription (transcribe_audio)
├── text_to_speech.py     # gTTS-based speech synthesis (speak_text)
├── audio_recorder.py     # Standalone mic recording utility (sounddevice)
├── req.txt               # Python dependencies
└── artifacts/            # Sample images (e.g. acne.jpeg) for testing
```

## Getting Started

### Prerequisites

- Python 3.10+
- A Google Gemini API key

### Installation

```bash
git clone https://github.com/Aishveerdev/Voicebot-doctor.git
cd Voicebot-doctor
pip install -r req.txt
```

> Note: `req.txt` lists `dotenv` — make sure `python-dotenv` is installed (`pip install python-dotenv`) since that's the actual package providing `dotenv.load_dotenv`.

### Environment Variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_gemini_api_key
```

### Running the app

```bash
python app.py
```

This launches a Gradio web interface where you can upload an image and record your symptoms.

## Response Schema

The AI's diagnosis is returned in a structured format (`Medical_Response`):

```python
{
  "detected_issue": str,
  "description": str,
  "severity": str,
  "recommendations": list[str],
  "should_consult_doctor": bool,
  "confidence": float,
  "spoken_response": str
}
```

## Sample Data

The `artifacts/` folder includes a sample image (`acne.jpeg`) you can use to try the app out quickly.

## Disclaimer

This project is for educational/demo purposes only and is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare provider for medical concerns.

## License

*(Add your license here, e.g. MIT.)*
