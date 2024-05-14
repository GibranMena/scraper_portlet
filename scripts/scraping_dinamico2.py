
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


# Click on the first link

element = driver.find_element(By.CSS_SELECTOR, "#busqSimpleForm\:Pluto__adquisiciones_gestion_portlet_busquedaProcedimientoPortlet__id22")
element.click()

# Find the element for number of results using XPath and click it
element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]")
element2.click()

# Find the element for year of results using XPath and click it
element3 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]")
element3.click()

# Wait for the input field to appear after clicking the element
input_element = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[1]/td[2]/input")
    
# Write a name inside the input field
input_element.send_keys("Bismarck Martinez")

# Check the first checkbox using full XPath
checkbox1 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[1]/td[4]/label/input")
checkbox1.click()

# Check the second checkbox using full XPath
checkbox2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[11]/td[2]/table/tbody/tr[1]/td[2]/label/input")
checkbox2.click()

# Check the third checkbox using full XPath
checkbox3 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[3]/td[2]/label/input")
checkbox3.click()

# Check the fourth checkbox using full XPath
checkbox4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[29]/td[2]/input")
checkbox4.click()

# Hit the Search button using full XPath
element4 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input")
element4.click()

#time.sleep(4)  # Mimic human delay

# Wait until the contents are loaded
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))

# Initialize CSV file and writer
#csv_file = open('scraped_data.csv', 'a', newline='', encoding='utf-8')
#csv_writer = csv.writer(csv_file)

# Scrape the visible content using full XPath
scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

# Write the scraped content to the CSV file
#csv_writer.writerow([scraped_content])

# Close the CSV file
#csv_file.close()

# Quit the driver
driver.quit()

#Parse data

import re
import json

# Function to parse the text
def parse_text(scraped_text):
    pattern = re.compile(
        r'(LICITACION PUBLICA|CONTRATACION SIMPLIFICADA)\n'
        r'(\d{1,2}/20\d{2})\n'  # Matches a sequence starting with 1-2 digits followed by "/20" and two more digits
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
    return data_list  # Moved return statement outside the loop

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
#scraped_data = scraped_content
parsed_data = parse_text(scraped_content)
save_to_json(parsed_data)









