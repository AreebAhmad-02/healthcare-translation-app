# import streamlit as st
# from googletrans import LANGUAGES
# import os
# import streamlit as st
# # import speech_recognition as sr
# from gtts import gTTS
# from googletrans import Translator,LANGUAGES
# import os
# import assemblyai as aai
# from streamlit_mic_recorder import mic_recorder

# # Replace with your API key
# aai.settings.api_key = "ac38c03ab1fd4cc4b970a2dc5d6f8a31"

# # Initialize Translator
# translator = Translator()

# # # Function for speech-to-text
# # def speech_to_text():
# #     recognizer = sr.Recognizer()
# #     with sr.Microphone() as source:
# #         st.info("Listening... Speak now!")
# #         try:
# #             audio_data = recognizer.listen(source, timeout=5)
# #             text = recognizer.recognize_google(audio_data)
# #             return text
# #         except sr.UnknownValueError:
# #             st.error("Could not understand audio")
# #         except sr.RequestError as e:
# #             st.error(f"Speech recognition error: {e}")
# #         return None

# def speech_to_text(audio_bytes):
#     # recognizer = sr.Recognizer()


#     # audio_data = recognizer.listen(source, timeout=5)
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(audio_bytes)
#     if transcript.status == aai.TranscriptStatus.error:
#         print(transcript.error)
#     else:
#         print(transcript.text)
#     return transcript.text


# # Function to translate text
# def translate_text(text, target_language):
#     try:
#         translated = translator.translate(text, dest=target_language)
#         return translated.text
#     except Exception as e:
#         st.error(f"Translation error: {e}")
#         return None

# # Function to generate audio
# def text_to_speech(text, lang):
#     try:
#         tts = gTTS(text=text, lang=lang)
#         audio_file = "temp_audio.mp3"
#         tts.save(audio_file)
#         return audio_file
#     except Exception as e:
#         st.error(f"Text-to-Speech error: {e}")
#         return None

# # Streamlit app
# def main():
#     st.title("Healthcare Translation Web App")
#     st.markdown("#### Real-time multilingual communication for patients and healthcare providers")
#     # Get all supported languages as a dictionary
#     languages = LANGUAGES

#     # Convert LANGUAGES dictionary into a list of tuples [(code, name)]
#     language_options = [(code, name.title()) for code, name in LANGUAGES.items()]

#     # Sidebar for language selection
#     st.header("Language Settings")

#     # Input Language Selection
#     input_lang = st.selectbox(
#         "Input Language",
#         options=[code for code, name in language_options],
#         format_func=lambda code: dict(language_options)[code]
#     )


#     # Output Language Selection
#     output_lang = st.selectbox(
#         "Output Language",
#         options=[code for code, name in language_options],
#         format_func=lambda code: dict(language_options)[code]
#     )
#     # Speech-to-text
#     audio=mic_recorder(
#     start_prompt="Start recording",
#     stop_prompt="Stop recording",
#     just_once=False,
#     use_container_width=False,
#     callback=None,
#     args=(),
#     kwargs={},
#     key=None
#     )

#     if audio:
#         audio_bytes = audio["bytes"]
#         text = speech_to_text(audio_bytes)
#         if text:
#             st.success("Original Transcript:")
#             st.write(text)

#             # Translation
#             translated_text = translate_text(text, output_lang)
#             if translated_text:
#                 st.success("Translated Transcript:")
#                 st.write(translated_text)

#                 # Text-to-speech
#                 audio_file = text_to_speech(translated_text, output_lang)
#                 if audio_file:
#                     st.audio(audio_file, format="audio/mp3")
#                     os.remove(audio_file)  # Clean up

#     st.markdown('<p style="font-size: 12px; text-align: center;">Powered by Streamlit, Google Speech Recognition, and gTTS</p>',
#         unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()


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

# Replace with your API key
# aai.settings.api_key = "ac38c03ab1fd4cc4b970a2dc5d6f8a31"

# Initialize Translator
# translator = google_translator()
translator = Translator()

# Real-time transcription function


# def speech_to_text(audio_bytes):
#     transcriber = aai.Transcriber()
#     transcript = transcriber.transcribe(audio_bytes)
#     if transcript.status == aai.TranscriptStatus.error:
#         print(transcript.error)
#         return None
#     else:
#         return transcript.text

# Function to translate text


def translate_text(text, target_language):
    try:
          
        genai.configure(api_key=st.secrets['GEMINI_API_KEY'])

        # Create a model instance
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Define the text to be translated and the target language
        text_to_translate = text
        target_language = target_language  

        # Prompt the model to translate the text
        prompt = f"You are a language translator who is experienced in medical domain. Translate '{text_to_translate}' to {target_language}. Please be specific and do not provide any additional detail"

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
    listening_text.text("Listening...")  # Display "Listening..." initially
    
    # Real-time Speech-to-text with mic_recorder
    
    text = speech_to_text(
        language='en',
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=False,
        use_container_width=False,
        callback=None,
        args=(),
        kwargs={},
        key=None
    )

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
                st.audio(audio_file, format="audio/mp3")
                os.remove(audio_file)  # Clean up
        else:
            st.error("Translation failed. Please try again.")

    st.markdown('<p style="font-size: 12px; text-align: center;">Powered by Streamlit, Google Speech Recognition, and gTTS</p>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
