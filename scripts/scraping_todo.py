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

# Function to extract patterns and append to JSON
def extract_patterns_and_append_to_json(text, json_file_path):
    pattern = re.compile(
        r"""
        Procedimiento\sDetalles\sAcciones\n([^\n]+)\n
        ([^\n]+)\n
        Estado:\n(\w+)\n
        Código\sSIGAF:\n(\#)\n
        Publicación:\n(\d{2}/\d{2}/\d{4})\n
        Cierre:\n(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s(?:AM|PM))\n
        Última\sActualización:\n(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s(?:AM|PM))\n
        Alcaldía\s([^\n]+)\s\([^\n]+\)\s-\sUnidad\sde\sAdquisiciones?\s[^\n]+\n
        ([^\n]+)\n
        (.+?)\nMás\sDatos
        """,
        re.VERBOSE | re.DOTALL
    )

    matches = pattern.findall(text)
    
    extracted_data = []
    for match in matches:
        extracted_data.append({
            "tipo_procedimiento": match[0],
            "licitacion": match[1],
            "estado": match[2],
            "codigo_sigaf": match[3],
            "publicacion": match[4],
            "cierre": match[5],
            "ultima_actualizacion": match[6],
            "alcaldia": match[7],
            "servicios": match[8],
            "programa": match[9]
        })

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    existing_data.extend(extracted_data)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

# Loop through each year and term
for year in years:
    for term in terms:
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

            # Enter "Bismarck Martinez" into the search input
            search_input = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[1]/td[2]/input")
            search_input.clear()
            search_input.send_keys("Bismarck")

            time.sleep(2)  # Mimic human delay

            # Select the checkboxes
            checkbox1 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[1]/td[4]/label/input")
            checkbox1.click()

            checkbox2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[3]/td[2]/label/input")
            checkbox2.click()

            checkbox4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[29]/td[2]/input")
            checkbox4.click()

            # Click the search button
            element4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input")
            element4.click()

            time.sleep(4)  # Mimic human delay

            # Wait for the content to load and scrape it
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))
            scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

            # Append the scraped content to the JSON file
            json_file_path = 'scraped_data.json'
            extract_patterns_and_append_to_json(scraped_content, json_file_path)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

# Quit the driver after completing the loop
driver.quit()
