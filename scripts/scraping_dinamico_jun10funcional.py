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

# Keep session data by setting the driver's options
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
#options.add_argument("--headless")

# Setup Chrome Service
service = Service(ChromeDriverManager().install())

# Create WebDriver object with the above options
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the initial webpage
driver.get("https://www.gestion.nicaraguacompra.gob.ni/siscae/portal/adquisiciones-gestion/busqueda?accion=todos&usr_ua_id=todos")


# Click on the first link for Advanced Search

element = driver.find_element(By.CSS_SELECTOR, "#busqSimpleForm\:Pluto__adquisiciones_gestion_portlet_busquedaProcedimientoPortlet__id22")
element.click()

# Find the element for number of results using XPath and click it
element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]")
element2.click()

# Find the element for year of results using XPath and click it (year)
element3 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[3]/td[3]/span/select/option[18]")
element3.click()

time.sleep(4)  # Mimic human delay

# Wait for the input field to appear after clicking the element
input_element = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[1]/td[2]/input")
    
# Write a name inside the input field
input_element.send_keys("Bismarck Martinez")

# Check the first checkbox using full XPath
checkbox1 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[1]/td[4]/label/input")
checkbox1.click()

# Check the second checkbox using full XPath (Adjudicado)
checkbox2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[3]/td[2]/label/input")
checkbox2.click()

# Check the third checkbox using full XPath (Adjudicado)
#checkbox3 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[3]/td[2]/label/input")
#checkbox3.click()

# Check the fourth checkbox using full XPath
checkbox4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[29]/td[2]/input")
checkbox4.click()

# Select the  year from 19 to 14
# Find the dropdown menu using the full XPATH
#dropdown_element = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[3]/td[3]/span/select")

# Wrap the element in a Select object
#dropdown = Select(dropdown_element)

# Select the option by index (indexing starts from 0, so 19th option is index 18)
#dropdown.select_by_index(16)

## Find the dropdown menu using the full XPATH (alcaldía)
dropdown_element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[8]/td[2]/select")

# Wrap the element in a Select object
dropdown = Select(dropdown_element2)

# Select the option by visible text (select by text entered) Alcaldía
dropdown.select_by_visible_text("Alcaldía Managua")

time.sleep(4)  # Mimic human delay

# Hit the Search button using full XPath
element4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input")
element4.click()

time.sleep(4)  # Mimic human delay

# Wait until the contents are loaded
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))

# Scrape the visible content using full XPath
scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

# Quit the driver
driver.quit()

text = scraped_content

#Parse data

import re
import json
import os

# Define the regular expressions for each element
regex_patterns = {
    "tipo_de_procedimiento": re.compile(r'^(.*?)(?=\n|$)', re.DOTALL),
    "estado": re.compile(r'Estado:\n(.*?)\n', re.DOTALL),
    "codigo_sigaf": re.compile(r'Código\sSIGAF:\n#(.*?)\n', re.DOTALL),
    "publicacion": re.compile(r'Publicación:\n(\d{2}/\d{2}/\d{4})\n', re.DOTALL),
    "cierre": re.compile(r'Cierre:\n(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [APM]{2})\n', re.DOTALL),
    "ultima_actualizacion": re.compile(r'Última\sActualización:\n(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2} [APM]{2})\n', re.DOTALL),
    "alcaldia": re.compile(r'Alcaldía\s(.*?)\n', re.DOTALL),
    "detalles_procedimiento": re.compile(r'(?:Alcaldía\s.*?\n)(.*?)(?=Más\sDatos|$)', re.DOTALL)
}

# Function to parse the text and extract the required elements
def parse_text(text):
    parsed_data = []
    # Split the text into segments
    segments = re.split(r'Procedimiento\sDetalles\sAcciones\n|\nMás\sDatos\n', text)
    for segment in segments:
        if segment.strip():  # Skip empty segments
            tipo_de_procedimiento_match = regex_patterns["tipo_de_procedimiento"].search(segment)
            tipo_de_procedimiento = tipo_de_procedimiento_match.group(1).strip() if tipo_de_procedimiento_match else None
            estado_match = regex_patterns["estado"].search(segment)
            estado = estado_match.group(1).strip() if estado_match else None
            codigo_sigaf_match = regex_patterns["codigo_sigaf"].search(segment)
            codigo_sigaf = codigo_sigaf_match.group(1).strip() if codigo_sigaf_match else None
            publicacion_match = regex_patterns["publicacion"].search(segment)
            publicacion = publicacion_match.group(1).strip() if publicacion_match else None
            cierre_match = regex_patterns["cierre"].search(segment)
            cierre = cierre_match.group(1).strip() if cierre_match else None
            ultima_actualizacion_match = regex_patterns["ultima_actualizacion"].search(segment)
            ultima_actualizacion = ultima_actualizacion_match.group(1).strip() if ultima_actualizacion_match else None
            alcaldia_match = regex_patterns["alcaldia"].search(segment)
            alcaldia = alcaldia_match.group(1).strip() if alcaldia_match else None
            detalles_procedimiento_match = regex_patterns["detalles_procedimiento"].search(segment)
            detalles_procedimiento = detalles_procedimiento_match.group(1).strip() if detalles_procedimiento_match else None

            parsed_data.append({
                "tipo_de_procedimiento": tipo_de_procedimiento,
                "estado": estado,
                "codigo_sigaf": codigo_sigaf,
                "publicacion": publicacion,
                "cierre": cierre,
                "ultima_actualizacion": ultima_actualizacion,
                "alcaldia": alcaldia,
                "detalles_procedimiento": detalles_procedimiento
            })
    return parsed_data

# Function to check if a JSON file exists, create it if it doesn't, and append the parsed data
def append_to_json_file(file_path, data):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
    
    with open(file_path, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data.extend(data)
        file.seek(0)
        json.dump(file_data, file, indent=4, ensure_ascii=False)

# Parse the text
parsed_data = parse_text(text)

# Print the parsed data
print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

# Append the parsed data to the JSON file
json_file_path = 'parsed_data.json'
append_to_json_file(json_file_path, parsed_data)





