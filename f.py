
# from googletrans import Translator
# translator = Translator()
# translated = translator.translate('สวัสดีจีน', dest='en')
# translated.text


# print(translated.text)

from google.cloud import aiplatform
import os
import google.generativeai as genai

# Set your API key (obtained from AI Studio)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'AIzaSyCuYHXXG2ajr4retaQzj3_BRZAXz7OacUM'

# Configure the API key
genai.configure(api_key="AIzaSyCuYHXXG2ajr4retaQzj3_BRZAXz7OacUM")

# Create a model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the text to be translated and the target language
text_to_translate = "Hello, world!"
target_language = "fr"  # French

# Prompt the model to translate the text
prompt = f"Translate '{text_to_translate}' to {target_language}."

# Generate the translation
response = model.generate_content(prompt)


print(response.text)