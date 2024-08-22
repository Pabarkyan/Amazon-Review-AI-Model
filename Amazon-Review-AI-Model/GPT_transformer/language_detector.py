from langdetect import detect, lang_detect_exception

def detect_language(text: str): # Esto es una forma de filtrar para poder evitar malgastar tokens de la API de chat gpt al traducir
    if text == '' or text.isspace(): # Evitamos que tenga problemas de adivinar
        return
    try:
        idioma = detect(text)
        return idioma
    except lang_detect_exception.LangDetectException:
        return

