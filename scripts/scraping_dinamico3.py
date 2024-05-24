from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv
import re
import json

# List of terms to search for
terms = [
    "Alcaldía Managua", "Alcaldía Ciudad Sandino", "Alcaldía El Crucero", "Alcaldía Tipitapa",
    "Alcaldía Mateare", "Alcaldía Ticuantepe", "Alcaldía San Rafael del Sur", "Alcaldía Masaya",
    "Alcaldía Granada", "Alcaldía Rivas", "Alcaldía Jinotepe", "Alcaldía Diriamba",
    "Alcaldía San Marcos", "Alcaldía Matagalpa", "Alcaldía El Tuma La Dalia",
    "Alcaldía Jinotega", "Alcaldía San Rafael del Norte", "Alcaldía San José de Bocay",
    "Alcaldía de León", "Alcaldía Chinandega", "Alcaldía Posoltega", "Alcaldía Santo Tomás",
    "Alcaldía Palacagüina", "Alcaldía Estelí", "Alcaldía Ocotal", "Alcaldía San Carlos",
    "Alcaldía El Rama", "Alcaldía Bluefields", "Alcaldía de Bluefields", "Alcaldía Puerto Cabezas",
    "Instituto de la Vivienda Urbana y Rural"
]

# Indices range (from 19 to 14)
index_range = range(18, 12, -1)

# List of input search words
input_words = [
    "Bismarck Martínez", "apartamentos", "casas", "viviendas", "urbanización",
    "lotes", "reparto", "villa", "lotificación", "barrio", "terreno",
    "proyecto", "programa"
]

# Keep session data by setting the driver's options
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# options.add_argument("--headless")

# Setup Chrome Service
service = Service(ChromeDriverManager().install())

# Create WebDriver object with the above options
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the initial webpage
driver.get("https://www.gestion.nicaraguacompra.gob.ni/siscae/portal/adquisiciones-gestion/busqueda?accion=todos&usr_ua_id=todos")
time.sleep(2)  # Wait to simulate human action

# Click on the first link
element = driver.find_element(By.CSS_SELECTOR, "#busqSimpleForm\:Pluto__adquisiciones_gestion_portlet_busquedaProcedimientoPortlet__id22")
element.click()
time.sleep(2)  # Wait to simulate human action

# Iterate over each index and term
for idx in index_range:
    # Select the option by index for the first dropdown
    dropdown_element = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[3]/td[3]/span/select")
    dropdown = Select(dropdown_element)
    dropdown.select_by_index(idx)
    time.sleep(1)  # Wait to simulate human action

    for term in terms:
        # Find the dropdown menu for the term using the full XPATH
        dropdown_element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[8]/td[2]/select")

        # Wrap the element in a Select object
        dropdown2 = Select(dropdown_element2)

        # Select the option by visible text for the term
        dropdown2.select_by_visible_text(term)
        time.sleep(1)  # Wait to simulate human action

        for word in input_words:
            # Find the input element
            input_element = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[1]/td[2]/input")
            
            # Clear the input field
            input_element.clear()
            time.sleep(1)  # Wait to simulate human action

            # Write the word inside the input field
            input_element.send_keys(word)
            time.sleep(1)  # Wait to simulate human action

            # Hit the Search button using full XPath
            element4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input")
            element4.click()
            time.sleep(2)  # Wait to simulate human action

            # Wait until the contents are loaded
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))

            # Scrape the visible content using full XPath
            scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

            # Parse data
            def parse_text(scraped_text):
                pattern = re.compile(
                    r'(LICITACION PUBLICA|CONTRATACION SIMPLIFICADA)\n'
                    r'(\d{1,2}/20\d{2})\n'
                    r'Estado:\n(.*?)\n'
                    r'Código SIGAF:\n#.*?\n'
                    r'Publicación:\n(.*?)\n'
                    r'Cierre:\n(.*?)\n'
                    r'Última Actualización:\n(.*?)\n'
                    r'(.*?) - (.*?)\n'
                    r'(.*?)\n'
                    r'(.*?)\nMás Datos', re.DOTALL
                )

                entries = pattern.findall(scraped_text)
                data_list = []
                for entry in entries:
                    data = {
                        "procedimiento": entry[0],
                        "fecha_procedimiento": entry[1],
                        "estado": entry[2],
                        "codigo_sigaf_fecha_pub": entry[3],
                        "fecha_cierre": entry[4],
                        "última_actualización": entry[5],
                        "alcaldía": entry[6],
                        "unidad": entry[7],
                        "concepto": entry[8],
                        "descripción": entry[9]
                    }
                    data_list.append(data)
                return data_list

            # Function to save data to a JSON file
            def save_to_json(data, filepath='scraped_data.json'):
                try:
                    with open(filepath, 'r+') as file:
                        existing_data = json.load(file)
                        existing_data.extend(data)
                        file.seek(0)
                        json.dump(existing_data, file, indent=4)
                except FileNotFoundError:
                    with open(filepath, 'w') as file:
                        json.dump(data, file, indent=4)

            # Example usage of the functions
            # Make sure to define 'scraped_content' or pass a string directly
            parsed_data = parse_text(scraped_content)
            save_to_json(parsed_data)
            time.sleep(2)  # Wait to simulate human action

# Quit the driver
driver.quit()
