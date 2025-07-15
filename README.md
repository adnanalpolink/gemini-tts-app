# Gemini Text-to-Speech App

A Streamlit web application that converts text to speech using Google's Gemini API.

## Features

- 🎤 Convert text to speech using Google Gemini API
- 🔐 Secure API key input
- 🎵 Voice selection options
- 📱 Responsive web interface
- 💾 Download generated audio files
- ⚡ Real-time audio playback

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your Gemini API key:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in and create an API key
   - Copy the generated key

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter your Gemini API key in the secure input field
2. Type or paste the text you want to convert to speech
3. Select your preferred voice
4. Click "Generate Speech"
5. Play the audio or download the file

## Requirements

- Python 3.7+
- Streamlit
- Requests
- Valid Google Gemini API key

## Security

- API keys are handled securely and not stored
- Input validation prevents malicious requests
- Error handling for network and API issues
