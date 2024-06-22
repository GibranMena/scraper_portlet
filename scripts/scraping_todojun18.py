import re
import json
import os
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

# Function to append the parsed data to a JSON file
def append_to_json_file(file_path, data):
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
    
    with open(file_path, 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data.extend(data)
        file.seek(0)
        json.dump(file_data, file, indent=4, ensure_ascii=False)

# Setup Chrome Options
options = Options()
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
try:
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"Failed to initialize WebDriver: {e}")
    exit(1)

# List of years and terms
years = ["14", "15", "16", "17", "18", "19", "20"]
search_terms = ["Vivienda", "Urbanización", "Lotes", "Reparto", "Villa", "Barrio", "Lotificación", "Terreno", "Social", "Proyecto", "Programa"]
terms = [
    "Alcaldía Managua", "Alcaldía Ciudad Sandino", "Alcaldía El Crucero", "Alcaldía Tipitapa", 
    "Alcaldía Mateare", "Alcaldía Ticuantepe", "Alcaldía San Rafael del Sur", "Alcaldía Masaya", 
    "Alcaldía Granada", "Alcaldía Rivas", "Alcaldía Jinotepe", "Alcaldía Diriamba", 
    "Alcaldía San Marcos", "Alcaldía Matagalpa", "Alcaldía El Tuma La Dalia", "Alcaldía Jinotega", 
    "Alcaldía San Rafael del Norte", "Alcaldía San José de Bocay", "Alcaldía de León", 
    "Alcaldía Chinandega", "Alcaldía Posoltega", "Alcaldía Santo Tomás", "Alcaldía Palacagüina", 
    "Alcaldía Estelí", "Alcaldía Ocotal", "Alcaldía San Carlos", "Alcaldía El Rama", 
    "Alcaldía Bluefields", "Alcaldía Puerto Cabezas", "Instituto de la Vivienda Urbana y Rural"
]

initial_url = "https://www.gestion.nicaraguacompra.gob.ni/siscae/portal/adquisiciones-gestion/busqueda?accion=todos&usr_ua_id=todos"

# Navigate to the initial webpage
driver.get(initial_url)

# Click on the first link for Advanced Search
element = driver.find_element(By.CSS_SELECTOR, "#busqSimpleForm\:Pluto__adquisiciones_gestion_portlet_busquedaProcedimientoPortlet__id22")
element.click()

# Loop through each year, term, and search term
for year in years:
    for term in terms:
        for search_term in search_terms:
            try:
                # Navigate to the initial webpage
                driver.get(initial_url)
                
                # Click on the first link for Advanced Search
                element = driver.find_element(By.CSS_SELECTOR, "#busqSimpleForm\:Pluto__adquisiciones_gestion_portlet_busquedaProcedimientoPortlet__id22")
                element.click()

                # Select the year using XPath
                year_xpath = f"/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[3]/td[3]/span/select/option[{year}]"
                element3 = driver.find_element(By.XPATH, year_xpath)
                element3.click()

                time.sleep(2)  # Mimic human delay

                # Select the term from dropdown
                dropdown_element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[8]/td[2]/select")
                dropdown = Select(dropdown_element2)
                dropdown.select_by_visible_text(term)

                time.sleep(2)  # Mimic human delay

                # Enter the search term into the search input
                search_input = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[1]/td[2]/input")
                search_input.clear()
                search_input.send_keys(search_term)

                time.sleep(2)  # Mimic human delay

                # Select the checkboxes
                checkbox1 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[1]/td[4]/label/input")
                checkbox1.click()

                checkbox2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[3]/td[2]/label/input")
                checkbox2.click()

                checkbox4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[29]/td[2]/input")
                checkbox4.click()

                # Find the element for number of results using XPath and click it
                element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]")
                element2.click()

                # Click the search button
                element4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input")
                element4.click()

                time.sleep(4)  # Mimic human delay

                # Wait for the content to load and scrape it
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))
                scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

                # Parse the scraped content and append to the JSON file
                json_file_path = 'scraped_data.json'
                parsed_data = parse_text(scraped_content)
                append_to_json_file(json_file_path, parsed_data)
            
            except Exception as e:
                print(f"An error occurred: {e}")
                continue

# Quit the driver after completing the loop
driver.quit()
import json
import csv

# Open the JSON file and load its contents
with open('scraped_data.json', 'r') as file:
    data = json.load(file)

# Create a list to store all the dictionaries
all_data = []
for item in data:
    all_data.append(item)

# Get all the keys from the first dictionary to use as the header row
fieldnames = list(all_data[0].keys())

# Open a new CSV file for writing
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write each dictionary as a row in the CSV file
    for item in all_data:
        writer.writerow(item)
