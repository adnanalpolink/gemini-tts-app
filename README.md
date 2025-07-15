# Gemini 2.5 TTS - Text to Speech App

A comprehensive Streamlit web application that converts text to speech using Google's latest Gemini 2.5 TTS models with native text-to-speech capabilities.

## Features

- 🎤 **Latest Gemini 2.5 TTS Models**: Flash and Pro variants with native TTS
- 🎵 **30 Unique Voices**: From bright and clear to breathy and mature
- 🎭 **Single & Multi-Speaker**: Support for up to 2 speakers in conversations
- 🌍 **24 Languages**: Automatic language detection for global use
- 🎨 **Style Control**: Natural language prompts to control tone, pace, and emotion
- 🔐 **Secure**: API keys handled securely without storage
- 📱 **Responsive**: Clean, intuitive web interface
- 💾 **Download**: Save generated audio as WAV files

## Supported Models

- **Gemini 2.5 Flash Preview TTS**: Fast, efficient speech generation
- **Gemini 2.5 Pro Preview TTS**: Higher quality, more nuanced speech

## Voice Options (30 Total)

### Bright & Clear
- Zephyr, Autonoe, Iapetus, Erinome

### Firm & Strong  
- Kore, Orus, Alnilam

### Upbeat & Lively
- Puck, Laomedeia, Sadachbia

### Easy-going & Smooth
- Callirrhoe, Umbriel, Algieba, Despina

### Informative
- Charon, Rasalgethi, Sadaltager

### Unique Characteristics
- Fenrir (Excitable), Enceladus (Breathy), Gacrux (Mature)
- Achernar (Soft), Algenib (Gravelly), Pulcherrima (Forward)
- And 12 more unique voices...

## Supported Languages (24 Total)

- **English**: US, India
- **European**: German, French, Italian, Dutch, Polish, Romanian, Ukrainian
- **Asian**: Japanese, Korean, Thai, Vietnamese, Indonesian
- **Indian**: Hindi, Marathi, Tamil, Telugu, Bengali
- **Others**: Arabic (Egyptian), Spanish (US), Portuguese (Brazil), Russian, Turkish

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Get Gemini API key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in and create an API key
   - Ensure you have access to Gemini 2.5 TTS models (Preview)

3. **Run the application:**
```bash
streamlit run app.py
```

## Usage Examples

### Single Speaker
```
Say cheerfully: Have a wonderful day!
```

```
Say in a spooky whisper: Something wicked this way comes
```

### Multi-Speaker
```
Speaker1: How's it going today?
Speaker2: Not too bad, how about you?
```

```
Make Speaker1 sound tired and bored, and Speaker2 sound excited:

Speaker1: So... what's on the agenda today?
Speaker2: You're never going to guess!
```

## API Configuration

The app uses the official Gemini 2.5 TTS API structure:

### Single Speaker
```python
{
    "contents": [{"parts": [{"text": text}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": {
                "prebuiltVoiceConfig": {"voiceName": voice}
            }
        }
    }
}
```

### Multi-Speaker
```python
{
    "contents": [{"parts": [{"text": text}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "multiSpeakerVoiceConfig": {
                "speakerVoiceConfigs": [
                    {
                        "speaker": "Speaker1",
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {"voiceName": "Kore"}
                        }
                    }
                ]
            }
        }
    }
}
```

## Limitations

- **Input**: Text-only (no other modalities)
- **Output**: Audio-only (WAV format)
- **Context**: 32k token limit (~8000 characters)
- **Speakers**: Maximum 2 speakers for multi-speaker mode
- **Access**: Requires Gemini 2.5 TTS Preview access

## Advanced Features

- **Style Control**: Use natural language to guide emotion, pace, and tone
- **Language Detection**: Automatic detection of 24 supported languages
- **Voice Matching**: Choose voices that complement your desired style
- **Error Handling**: Comprehensive error messages and validation
- **Real-time Feedback**: Loading indicators and progress updates

## Requirements

- Python 3.7+
- Streamlit
- Requests
- Valid Google Gemini API key with 2.5 TTS access

## Security & Privacy

- API keys are masked and not stored
- Input validation prevents malicious requests
- Secure HTTPS communication with Google APIs
- No audio data retention after session ends
