import streamlit as st
import requests
import base64
import json
import io
import time
from typing import Optional, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Gemini TTS - Text to Speech",
    page_icon="🎤",
    layout="wide"
)

def get_gemini_tts(text: str, api_key: str, voice: str = "en-US-Journey-D") -> Optional[bytes]:
    """
    Generate speech using Google Gemini API
    
    Args:
        text: Text to convert to speech
        api_key: Google Gemini API key
        voice: Voice model to use
    
    Returns:
        Audio bytes if successful, None if failed
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": f"Generate speech for: {text}"
            }]
        }],
        "generationConfig": {
            "response_mime_type": "audio/wav"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            # Extract audio data from response
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "inline_data" in part:
                            audio_data = part["inline_data"]["data"]
                            return base64.b64decode(audio_data)
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
    st.title("🎤 Gemini Text-to-Speech")
    st.markdown("Convert text to speech using Google's Gemini API")
    
    # Instructions
    with st.expander("📋 How to get your Gemini API Key"):
        st.markdown("""
        1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the generated API key
        5. Paste it in the field below
        
        **Note:** Keep your API key secure and don't share it publicly.
        """)
    
    # API Key input
    api_key = st.text_input(
        "🔑 Enter your Gemini API Key:",
        type="password",
        help="Your API key will not be stored and is only used for this session"
    )
    
    # Text input
    text_input = st.text_area(
        "📝 Enter text to convert to speech:",
        height=100,
        max_chars=1000,
        help="Maximum 1000 characters"
    )
    
    # Voice selection (placeholder for future implementation)
    voice_options = {
        "en-US-Journey-D": "English (US) - Journey D",
        "en-US-Journey-F": "English (US) - Journey F",
        "en-GB-Journey-D": "English (UK) - Journey D"
    }
    
    selected_voice = st.selectbox(
        "🎵 Select Voice:",
        options=list(voice_options.keys()),
        format_func=lambda x: voice_options[x]
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        generate_button = st.button(
            "🎯 Generate Speech",
            type="primary",
            use_container_width=True
        )
    
    # Validation and generation
    if generate_button:
        if not api_key:
            st.error("Please enter your Gemini API key")
        elif not validate_api_key(api_key):
            st.error("Invalid API key format. Please check your key.")
        elif not text_input.strip():
            st.error("Please enter some text to convert to speech")
        elif len(text_input) > 1000:
            st.error("Text is too long. Please limit to 1000 characters.")
        else:
            # Show loading spinner
            with st.spinner("Generating speech... This may take a few seconds."):
                audio_data = get_gemini_tts(text_input.strip(), api_key, selected_voice)
            
            if audio_data:
                st.success("✅ Speech generated successfully!")
                
                # Audio player
                st.audio(audio_data, format="audio/wav")
                
                # Download button
                st.download_button(
                    label="💾 Download Audio",
                    data=audio_data,
                    file_name=f"gemini_tts_{int(time.time())}.wav",
                    mime="audio/wav"
                )
                
                # Show text that was converted
                with st.expander("📄 Converted Text"):
                    st.write(text_input)
            else:
                st.error("Failed to generate speech. Please check your API key and try again.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ by Adnan Akram"
    )

if __name__ == "__main__":
    main()
