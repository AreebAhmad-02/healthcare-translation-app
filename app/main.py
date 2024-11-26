import streamlit as st
from googletrans import LANGUAGES
import os
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator,LANGUAGES
import os

# Initialize Translator
translator = Translator()

# Function for speech-to-text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        try:
            audio_data = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
        return None

# Function to translate text
def translate_text(text, target_language):
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

# Function to generate audio
def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")
        return None

# Streamlit app
def main():
    st.title("Healthcare Translation Web App")
    st.markdown("#### Real-time multilingual communication for patients and healthcare providers")
    # Get all supported languages as a dictionary
    languages = LANGUAGES
    
    # Convert LANGUAGES dictionary into a list of tuples [(code, name)]
    language_options = [(code, name.title()) for code, name in LANGUAGES.items()]

    # Sidebar for language selection
    st.header("Language Settings")

    # Input Language Selection
    input_lang = st.selectbox(
        "Input Language",
        options=[code for code, name in language_options],
        format_func=lambda code: dict(language_options)[code]
    )
    

    # Output Language Selection
    output_lang = st.selectbox(
        "Output Language",
        options=[code for code, name in language_options],
        format_func=lambda code: dict(language_options)[code]
    )
    # Speech-to-text
    if st.button("Start Recording"):
        text = speech_to_text()
        if text:
            st.success("Original Transcript:")
            st.write(text)
            
            # Translation
            translated_text = translate_text(text, output_lang)
            if translated_text:
                st.success("Translated Transcript:")
                st.write(translated_text)
                
                # Text-to-speech
                audio_file = text_to_speech(translated_text, output_lang)
                if audio_file:
                    if st.button("Speak Translated Text"):
                        st.audio(audio_file, format="audio/mp3")
                        os.remove(audio_file)  # Clean up

    st.markdown('<p style="font-size: 12px; text-align: center;">Powered by Streamlit, Google Speech Recognition, and gTTS</p>', 
        unsafe_allow_html=True)

if __name__ == "__main__":
    main()
