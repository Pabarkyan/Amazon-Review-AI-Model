# Amazon-Review-AI-Model

_El siguiente repo consiste en clasificar reseñas de amazon escritas por una IA vs Humano, mediante un modelo supervisado, en un dataset creado con webScrapping + API de OpenAI_

## Descripción 🚀
 
Este repo lo podemos dividir en 2 partes, la primera es la creación del dataset mediante webScrapping en la página de amazon (carpeta de scrapper). Posteriormente mediante la API de chatGPT de OpenAI le pedimos que nos escriba las mismas reseñas pero con sus "palabras". Evidentemente entre etapa y etapa hacemos limpieza de datos. Para finalizar sacamos gran cantidad de cualidades numericas mediante procesamiento del lenguaje natural de cada reseña para posteriormente utilizar un Random Forest para clasificar si lo ha escrito una IA o no.

# Instalación 📋

_Que cosas necesitas para instalar el software y como instalarlas_

## 1. Clona este repositorio

''
`git clone https://github.com/Pabarkyan/Amazon-Review-AI-Model.git`

`cd [nombre del repo]`
''

## 2. Crear y activar el entorno virtual

`python -m venv venv`

`source venv/bin/activate`  # O `venv\Scripts\activate` en Windows`

`pip install -r requirements.txt`

## 3. claves

#### Necesitaras las siguientes claves:

- En GPT_transformer/.env -> OPENAI_API_KEY=[tu clave de tu api de openAI] (debes tener dinero para que funcione)
- En scrapper/.env -> CHROME_PATH=[La ruta donde este instalado tu webDriver]