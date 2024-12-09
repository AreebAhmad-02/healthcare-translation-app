import streamlit as st
from googletrans import Translator, LANGUAGES

# from google_trans_new import google_translator
from gtts import gTTS
import os
from streamlit_mic_recorder import speech_to_text
# import assemblyai as aai
from streamlit_mic_recorder import mic_recorder
import google.generativeai as genai
import io



translator = Translator()



def translate_text(text, target_language):
    try:
          
        genai.configure(api_key=st.secrets['GEMINI_API_KEY'])

        # Create a model instance
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Define the text to be translated and the target language
        text_to_translate = text
        target_language = target_language  

        # Prompt the model to translate the text
        prompt = f"You are a language translator who is experienced in medical domain. Translate '{text_to_translate}' to {target_language}. Please be specific and just write the translated language nothing else"

        # Generate the translation
        response = model.generate_content(prompt)


        print(response.text)
        return response.text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return None

# Function to generate audio (Text-to-Speech)


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
    st.markdown(
        "#### Real-time multilingual communication for patients and healthcare providers")

    # Get all supported languages as a dictionary
    language_options = [(code, name.title())
                        for code, name in LANGUAGES.items()]

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

    listening_text = st.empty()  # Create an empty placeholder for dynamic updates
    # listening_text.text("Listening...")  # Display "Listening..." initially
    st.markdown(
        "###### Tap the Start Recording button to start the recording")
    st.markdown(
        "###### When you are done Recording tap the stop recording button to stop recording")
    
    # Real-time Speech-to-text with mic_recorder
    
    unrefined_text = speech_to_text(
        language=input_lang,
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=False,
        use_container_width=False,
        callback=None,
        args=(),
        kwargs={},
        key=None
    )

    text = unrefined_text
    

    # if audio:
    #     audio_bytes = audio["bytes"]
    #     st.info("Processing audio...")

    #     # Transcription
    #     text = speech_to_text(audio_bytes)
    if text:
        
        st.success("Original Transcript:")
        st.write(text)

        # Translation
        
        translated_text = translate_text(text, output_lang)
        
        print("translate_text",translated_text)
        if translated_text:
            st.success("Translated Transcript:")
            st.write(translated_text)

            # Text-to-speech
            audio_file = text_to_speech(translated_text, output_lang)
            if audio_file:
                st.audio(audio_file, format="audio/mpeg")
                os.remove(audio_file)  # Clean up
        else:
            st.error("Translation failed. Please try again.")

    st.markdown('<p style="font-size: 12px; text-align: center;">Powered by Streamlit, Google Speech Recognition, gTTS and Google Gemini</p>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
