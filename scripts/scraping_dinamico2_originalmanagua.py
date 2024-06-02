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
element3 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[3]/td[3]/span/select/option[19]")
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
dropdown.select_by_visible_text("Alcaldía Ciudad Sandino")

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

#Parse data

import re
import json
text = scraped_content

import json
import re

def extract_patterns_and_append_to_json(text, json_file_path):
    # Define the regex pattern to extract details
    pattern = re.compile(r"""
        LICITACION\sPUBLICA\s(\d+/\d+)\n
        Estado:\n(\w+)\n
        Código\sSIGAF:\n(\#)\n
        Publicación:\n(\d{2}/\d{2}/\d{4})\n
        Cierre:\n(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s(?:AM|PM))\n
        Última\sActualización:\n(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}\s(?:AM|PM))\n
        Alcaldía\sManagua\s\(
        Alcaldía\sManagua
        \)\s-\sUnidad\sde\sAdquisición\sMANAGUA\n
        ([^\n]+)\n
        (.+?)\nMás\sDatos
    """, re.VERBOSE | re.DOTALL)

    matches = pattern.findall(text)
    
    # Structure the extracted data
    extracted_data = []
    for match in matches:
        extracted_data.append({
            "licitacion": match[0],
            "estado": match[1],
            "codigo_sigaf": match[2],
            "publicacion": match[3],
            "cierre": match[4],
            "ultima_actualizacion": match[5],
            "unidad_adquisicion": "Alcaldía Managua - Unidad de Adquisición MANAGUA",
            "servicios": match[6],
            "programa": match[7]
        })

    # Load the existing JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        existing_data = json.load(file)

    # Append the new data to the existing JSON data
    existing_data.extend(extracted_data)

    # Save the updated JSON file
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

text = scraped_content

json_file_path = 'scraped_data.json'
extract_patterns_and_append_to_json(text, json_file_path)










