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
