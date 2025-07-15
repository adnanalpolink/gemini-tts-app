import streamlit as st
import requests
import base64
import json
import io
import time
from typing import Optional, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Gemini 2.5 TTS - Text to Speech",
    page_icon="🎤",
    layout="wide"
)

# Available models based on Gemini 2.5 TTS documentation
MODELS = {
    "gemini-2.5-flash-preview-tts": "Gemini 2.5 Flash Preview TTS",
    "gemini-2.5-pro-preview-tts": "Gemini 2.5 Pro Preview TTS"
}

# Voice options from the official documentation
VOICES = {
    "Zephyr": "Zephyr - Bright",
    "Puck": "Puck - Upbeat", 
    "Charon": "Charon - Informative",
    "Kore": "Kore - Firm",
    "Fenrir": "Fenrir - Excitable",
    "Leda": "Leda - Youthful",
    "Orus": "Orus - Firm",
    "Aoede": "Aoede - Breezy",
    "Callirrhoe": "Callirrhoe - Easy-going",
    "Autonoe": "Autonoe - Bright",
    "Enceladus": "Enceladus - Breathy",
    "Iapetus": "Iapetus - Clear",
    "Umbriel": "Umbriel - Easy-going",
    "Algieba": "Algieba - Smooth",
    "Despina": "Despina - Smooth",
    "Erinome": "Erinome - Clear",
    "Algenib": "Algenib - Gravelly",
    "Rasalgethi": "Rasalgethi - Informative",
    "Laomedeia": "Laomedeia - Upbeat",
    "Achernar": "Achernar - Soft",
    "Alnilam": "Alnilam - Firm",
    "Schedar": "Schedar - Even",
    "Gacrux": "Gacrux - Mature",
    "Pulcherrima": "Pulcherrima - Forward",
    "Achird": "Achird - Friendly",
    "Zubenelgenubi": "Zubenelgenubi - Casual",
    "Vindemiatrix": "Vindemiatrix - Gentle",
    "Sadachbia": "Sadachbia - Lively",
    "Sadaltager": "Sadaltager - Knowledgeable",
    "Sulafat": "Sulafat - Warm"
}

# Supported languages
LANGUAGES = {
    "ar-EG": "Arabic (Egyptian)",
    "en-US": "English (US)",
    "de-DE": "German (Germany)",
    "es-US": "Spanish (US)",
    "fr-FR": "French (France)",
    "hi-IN": "Hindi (India)",
    "id-ID": "Indonesian (Indonesia)",
    "it-IT": "Italian (Italy)",
    "ja-JP": "Japanese (Japan)",
    "ko-KR": "Korean (Korea)",
    "pt-BR": "Portuguese (Brazil)",
    "ru-RU": "Russian (Russia)",
    "nl-NL": "Dutch (Netherlands)",
    "pl-PL": "Polish (Poland)",
    "th-TH": "Thai (Thailand)",
    "tr-TR": "Turkish (Turkey)",
    "vi-VN": "Vietnamese (Vietnam)",
    "ro-RO": "Romanian (Romania)",
    "uk-UA": "Ukrainian (Ukraine)",
    "bn-BD": "Bengali (Bangladesh)",
    "en-IN": "English (India)",
    "mr-IN": "Marathi (India)",
    "ta-IN": "Tamil (India)",
    "te-IN": "Telugu (India)"
}

def get_gemini_tts_single(text: str, api_key: str, model: str, voice: str) -> Optional[bytes]:
    """Generate single-speaker speech using Gemini 2.5 TTS API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {
                    "prebuiltVoiceConfig": {
                        "voiceName": voice
                    }
                }
            }
        }
    }
    
    return make_api_request(url, headers, payload)

def get_gemini_tts_multi(text: str, api_key: str, model: str, speakers: list) -> Optional[bytes]:
    """Generate multi-speaker speech using Gemini 2.5 TTS API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    
    speaker_configs = []
    for speaker in speakers:
        speaker_configs.append({
            "speaker": speaker["name"],
            "voiceConfig": {
                "prebuiltVoiceConfig": {
                    "voiceName": speaker["voice"]
                }
            }
        })
    
    payload = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "multiSpeakerVoiceConfig": {
                    "speakerVoiceConfigs": speaker_configs
                }
            }
        }
    }
    
    return make_api_request(url, headers, payload)

def make_api_request(url: str, headers: dict, payload: dict) -> Optional[bytes]:
    """Make API request and handle response"""
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "inlineData" in part:
                            audio_data = part["inlineData"]["data"]
                            return base64.b64decode(audio_data)
            return None
        elif response.status_code == 400:
            error_data = response.json()
            if "error" in error_data:
                st.error(f"API Error: {error_data['error'].get('message', 'Bad request')}")
            else:
                st.error("Bad request - please check your input")
            return None
        elif response.status_code == 401:
            st.error("Invalid API key. Please check your Gemini API key.")
            return None
        elif response.status_code == 403:
            st.error("API access forbidden. Please check your API key permissions.")
            return None
        elif response.status_code == 429:
            st.error("Rate limit exceeded. Please wait a moment and try again.")
            return None
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    return api_key and len(api_key) > 20 and api_key.startswith("AIza")

def main():
    st.title("🎤 Gemini 2.5 TTS - Text to Speech")
    st.markdown("Convert text to speech using Google's latest Gemini 2.5 TTS models with 30 unique voices")
    
    # Instructions
    with st.expander("📋 How to get your Gemini API Key"):
        st.markdown("""
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the generated API key
        5. Paste it in the field below
        
        **Note:** You need access to Gemini 2.5 TTS models (currently in Preview).
        """)
    
    # API Key input
    api_key = st.text_input(
        "🔑 Enter your Gemini API Key:",
        type="password",
        help="Your API key will not be stored and is only used for this session"
    )
    
    # Model selection
    selected_model = st.selectbox(
        "🤖 Select Gemini Model:",
        options=list(MODELS.keys()),
        format_func=lambda x: MODELS[x],
        help="Choose the Gemini 2.5 TTS model"
    )
    
    # Mode selection
    mode = st.radio(
        "🎭 Select Mode:",
        ["Single Speaker", "Multi Speaker (up to 2)"],
        help="Choose between single or multi-speaker audio generation"
    )
    
    if mode == "Single Speaker":
        # Single speaker interface
        st.subheader("Single Speaker Configuration")
        
        # Voice selection
        selected_voice = st.selectbox(
            "🎵 Select Voice:",
            options=list(VOICES.keys()),
            format_func=lambda x: VOICES[x],
            help="Choose from 30 unique voice options"
        )
        
        # Text input with style guidance
        st.markdown("**💡 Style Tips:** You can control style with natural language:")
        st.code('Say cheerfully: Have a wonderful day!')
        st.code('Say in a spooky whisper: Something wicked this way comes')
        
        text_input = st.text_area(
            "📝 Enter text to convert to speech:",
            height=150,
            max_chars=8000,
            help="Maximum ~8000 characters (32k token limit)"
        )
        
    else:
        # Multi-speaker interface
        st.subheader("Multi Speaker Configuration (Up to 2 speakers)")
        
        # Speaker 1
        col1, col2 = st.columns(2)
        with col1:
            speaker1_name = st.text_input("Speaker 1 Name:", value="Speaker1")
            speaker1_voice = st.selectbox(
                "Speaker 1 Voice:",
                options=list(VOICES.keys()),
                format_func=lambda x: VOICES[x],
                key="speaker1_voice"
            )
        
        with col2:
            speaker2_name = st.text_input("Speaker 2 Name:", value="Speaker2")
            speaker2_voice = st.selectbox(
                "Speaker 2 Voice:",
                options=list(VOICES.keys()),
                format_func=lambda x: VOICES[x],
                key="speaker2_voice",
                index=1
            )
        
        # Multi-speaker text input with examples
        st.markdown("**💡 Multi-Speaker Format Examples:**")
        st.code(f'''{speaker1_name}: How's it going today?
{speaker2_name}: Not too bad, how about you?''')
        
        st.code(f'''Make {speaker1_name} sound tired and bored, and {speaker2_name} sound excited:

{speaker1_name}: So... what's on the agenda today?
{speaker2_name}: You're never going to guess!''')
        
        text_input = st.text_area(
            "📝 Enter conversation text:",
            height=200,
            max_chars=8000,
            help="Use speaker names as defined above. Maximum ~8000 characters"
        )
    
    # Character count
    char_count = len(text_input) if text_input else 0
    st.caption(f"Characters: {char_count}/8000")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        generate_button = st.button(
            "🎯 Generate Speech",
            type="primary",
            use_container_width=True,
            disabled=not (api_key and text_input.strip())
        )
    
    # Validation and generation
    if generate_button:
        if not api_key:
            st.error("Please enter your Gemini API key")
        elif not validate_api_key(api_key):
            st.error("Invalid API key format. Please check your key.")
        elif not text_input.strip():
            st.error("Please enter some text to convert to speech")
        elif len(text_input) > 8000:
            st.error("Text is too long. Please limit to ~8000 characters.")
        else:
            # Show loading spinner
            with st.spinner("Generating speech... This may take up to a minute."):
                if mode == "Single Speaker":
                    audio_data = get_gemini_tts_single(text_input.strip(), api_key, selected_model, selected_voice)
                    config_info = f"**Voice:** {VOICES[selected_voice]}"
                else:
                    speakers = [
                        {"name": speaker1_name, "voice": speaker1_voice},
                        {"name": speaker2_name, "voice": speaker2_voice}
                    ]
                    audio_data = get_gemini_tts_multi(text_input.strip(), api_key, selected_model, speakers)
                    config_info = f"**{speaker1_name}:** {VOICES[speaker1_voice]} | **{speaker2_name}:** {VOICES[speaker2_voice]}"
            
            if audio_data:
                st.success("✅ Speech generated successfully!")
                
                # Display generation info
                st.info(f"**Model:** {MODELS[selected_model]} | {config_info}")
                
                # Audio player
                st.audio(audio_data, format="audio/wav")
                
                # Download button
                mode_suffix = "single" if mode == "Single Speaker" else "multi"
                filename = f"gemini_tts_{mode_suffix}_{int(time.time())}.wav"
                st.download_button(
                    label="💾 Download Audio",
                    data=audio_data,
                    file_name=filename,
                    mime="audio/wav"
                )
                
                # Show text that was converted
                with st.expander("📄 Generated Text"):
                    st.write(text_input)
            else:
                st.error("Failed to generate speech. Please check your settings and try again.")
    
    # Voice samples info
    with st.expander("🎵 Voice Characteristics"):
        col1, col2, col3 = st.columns(3)
        
        voice_groups = [
            ("Bright & Clear", ["Zephyr", "Autonoe", "Iapetus", "Erinome"]),
            ("Firm & Strong", ["Kore", "Orus", "Alnilam"]),
            ("Upbeat & Lively", ["Puck", "Laomedeia", "Sadachbia"]),
            ("Easy-going & Smooth", ["Callirrhoe", "Umbriel", "Algieba", "Despina"]),
            ("Informative & Clear", ["Charon", "Rasalgethi"]),
            ("Unique Styles", ["Fenrir - Excitable", "Enceladus - Breathy", "Gacrux - Mature"])
        ]
        
        for i, (category, voices) in enumerate(voice_groups[:3]):
            with [col1, col2, col3][i]:
                st.markdown(f"**{category}**")
                for voice in voices:
                    if voice in VOICES:
                        st.write(f"• {voice}")
    
    # Statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Available Models", len(MODELS))
    with col2:
        st.metric("Voice Options", len(VOICES))
    with col3:
        st.metric("Supported Languages", len(LANGUAGES))
    with col4:
        st.metric("Max Speakers", "2")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ by Adnan Akram"
    )

if __name__ == "__main__":
    main()
