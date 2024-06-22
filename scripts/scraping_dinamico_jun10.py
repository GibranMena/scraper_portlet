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

#Parse data

import re
import json
import os

input_string = scraped_content


def parse_string(input_string):
    pattern = re.compile(r'Procedimiento\sDetalles\sAcciones\n(.*?)\n'
                          r'Estado:\n(.*?)\n'
                          r'Código\sSIGAF:\n#(.*?)\n'
                          r'Publicación:\n(.*?)\n'
                          r'Cierre:\n(.*?)\n'
                          r'Última\sActualización:\n(.*?)\n'
                          r'(Alcaldía.*?)\n'  # Capture the entire "Alcaldía" line
                          r'(.*?)\n'  # Capture the line after "Alcaldía"
                          r'(.*?)\nMás\sDatos', re.DOTALL)

    results = []
    for match in pattern.finditer(input_string):
        result = {
            'tipo_de_procedimiento': match.group(1).strip(),
            'estado': match.group(2).strip(),
            'codigo_sigaf': match.group(3).strip(),
            'publicacion': match.group(4).strip(),
            'cierre': match.group(5).strip(),
            'última_actualización': match.group(6).strip(),
            'alcaldia': match.group(7).strip(),  
            'detalles_procedimiento': match.group(9).strip()
        }
        results.append(result)

    return results

# Example usage
input_string = 'Procedimiento Detalles Acciones\nLICITACION PUBLICA\n267/2023\nEstado:\nEjecución\nCódigo SIGAF:\n#\nPublicación:\n30/10/2023\nCierre:\n29/11/2023 02:00:00 PM\nÚltima Actualización:\n06/12/2023 03:33:37 PM\nAlcaldía Managua (Alcaldía Managua) - Unidad de Adquisiciones\n\nEjecución\nEstructuras y edificios permanentes (95120000)\nPROGRAMA BISMARCK MARTINEZ VIVIENDA SOCIAL, CONSTRUCCIÓN DE OBRAS DE URBANIZACIÓN VILLA JERUSALÉN IV ETAPA (579 LOTES)\nMás Datos\n... (rest of the input string)'

parsed_data = parse_string(input_string)
print(json.dumps(parsed_data, indent=2, ensure_ascii=False))

# Example usage
input_string = 'Procedimiento Detalles Acciones\nLICITACION PUBLICA\n267/2023\nEstado:\nEjecución\nCódigo SIGAF:\n#\nPublicación:\n30/10/2023\nCierre:\n29/11/2023 02:00:00 PM\nÚltima Actualización:\n06/12/2023 03:33:37 PM\nAlcaldía Managua (Alcaldía Managua) - Unidad de Adquisición MANAGUA\nEstructuras y edificios permanentes (95120000)\nPROGRAMA BISMARCK MARTINEZ VIVIENDA SOCIAL, CONSTRUCCIÓN DE OBRAS DE URBANIZACIÓN VILLA JERUSALÉN IV ETAPA (579 LOTES)\nMás Datos\n... (rest of the input string)'

parsed_data = parse_string(input_string)
print(json.dumps(parsed_data, indent=2, ensure_ascii=False))


parsed_data = parse_string(text)
print(json.dumps(parsed_data, indent=2, ensure_ascii=False))


json_file_path = 'data_prueba.json'
extract_patterns_and_append_to_json(text, json_file_path)











