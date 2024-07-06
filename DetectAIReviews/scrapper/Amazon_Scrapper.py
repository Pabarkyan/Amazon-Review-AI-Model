from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener el contenido de una variable
path = os.getenv('CHROME_PATH') # Para evitar compartir nuestro path

# Establecemos el driver
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")

# Ruta al chromedriver
chromedriver_path = fr'{path}'

# Inicializa el navegador
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Entramos dentro de la pagina a scrapear, maximizamos la pantalla y aceptamos las cookies

driver.get('https://www.amazon.es/gp/bestsellers/?ref_=nav_cs_bestsellers') # Las reseñas las vamos a obtener de los bestsellers
driver.maximize_window()

accept_cokies = driver.find_element(By.ID ,'sp-cc-accept')
accept_cokies.click()
driver.implicitly_wait(10) # Una espera para evitar errores

# Dentro de la pagina buscamos todas las urls "ver mas" para poder scrapear la mayor cantidad de productos en la menor cantidad de enlaces posibles
 
urls_econtradas = driver.find_elements(By.CLASS_NAME, 'a-link-normal')
urls_ver_mas = []
for url in urls_econtradas:
    if url.text == 'Ver más':
        urls_ver_mas.append(url)

lista_combined_df = []
for url_ver_mas in urls_ver_mas:
    
    url_ver_mas.click()
    driver.implicitly_wait(10)
    clase_link_producto = 'a-link-normal'
    clase_link_hijo = 'aok-block'

    try:   
        urls_todos_productos = driver.find_elements(By.CLASS_NAME, clase_link_hijo)
        driver.implicitly_wait(10)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        categoria_en_div = soup.find('div', class_='_cDEzb_card-title_2sYgw')
        categoria = categoria_en_div.find('h1').text

        lista_df = []
        urls = [elemento.get_attribute('href') for elemento in urls_todos_productos]
        driver.implicitly_wait(10)

        for url_producto in urls:
            # ir = url_producto.get_attribute('href')
            # driver.implicitly_wait(10)

            driver.get(url_producto)
            driver.implicitly_wait(10)

            try:
                clase_producto = 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                reseñas_en_div = soup.find_all('div', class_=clase_producto)
                nombre_producto = soup.find('span', id='productTitle').text

                reseñas = []
                for reseña in reseñas_en_div:
                    if (reseña.find('span').text != 'Video Player is loading.') and (type(reseña.find('span').text) == str): # Algunas reseñas con video daban este mensaje en lugar de la reseña que de nada nos sirve
                        # y otras nos daban nones, por lo que podemos filtrar un poco
                        reseñas.append(reseña.find('span').text)
                        driver.implicitly_wait(10)


                producto = pd.DataFrame()
                producto['reseñas_humanas'] = reseñas
                producto['nombre_producto'] = nombre_producto
                producto['categoria_producto'] = categoria # Esto de momento no cambia
                lista_df.append(producto)
                driver.implicitly_wait(10)

            except Exception as e:
                print(f"Error al extraer información de {url_producto}: {e}") # obsevamos en que url no ha podido entrar

            
            driver.back()
            driver.implicitly_wait(10)

        combined_df = pd.concat(lista_df, ignore_index=True)
    except Exception as e:
        print(f"Error al extraer información de {url_producto}: {e}") 

    lista_combined_df.append(combined_df)

    driver.back()
    driver.implicitly_wait(10)

driver.quit()

df_definitivo = pd.concat(lista_combined_df, ignore_index=True)

df_definitivo.to_csv('reseñas_amazon.csv', index=False)