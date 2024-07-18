import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from google.generativeai.types import ContentType

# Documentation
# https://ai.google.dev/gemini-api/docs/text-generation?lang=python
# https://ai.google.dev/gemini-api/docs/prompting_with_media?lang=python

load_dotenv(find_dotenv())
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

# Add the model name you want to use


model = genai.GenerativeModel('gemini-1.5-flash-latest')

# response = model.generate_content("Can you give me a list of the most popular places in Colombia?")
response = model.generate_content(
  "Can you give me a list of the most popular places in Colombia?, please include only the list as bullet points no extra text."
)
print(response.text)

chain_node_1_response = model.generate_content(
  f"""
  Can you add a description to each of the places in this list?
  {response.text}
  """
)
print(chain_node_1_response.text)
