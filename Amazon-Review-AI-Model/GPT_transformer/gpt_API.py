from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener el contenido de una variable
sk = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=sk
)

def gpt_translator(text_to_translate: str, language: str):
  try:
    if language == 'es':
      return text_to_translate
    else:
      completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
      {"role": "system", "content": "Eres un traductor que recibe un texto en cualquier idioma y lo traduce al español."},
      {"role": "user", "content": text_to_translate}
      ]
      )
      return completion.choices[0].message.content # Obtenemos la traducción, solo si el texto no estan en 'es'
  except:
    return text_to_translate


def gpt_reviewer(review: str, longitud: int):
  try:
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": f"""
      Recibes una reseña de un producto y tienes que devolver una reseña con aproximadamente la misma longitud ({longitud} carácteres),
      que mejore la recibida, haciendola mas persuasiva y mejorandola gramaticalmente.
    """},
    {"role": "user", "content": review}
    ]
    )
    return completion.choices[0].message.content
  except:
    return None