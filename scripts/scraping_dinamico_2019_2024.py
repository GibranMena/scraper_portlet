import sys
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

def main(input_text, start_index, search_text):
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

    try:
        # Navigate to the initial webpage
        driver.get("https://www.gestion.nicaraguacompra.gob.ni/siscae/portal/adquisiciones-gestion/busqueda?accion=todos&usr_ua_id=todos")

        # Click on the first link
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#busqSimpleForm\\:Pluto__adquisiciones_gestion_portlet_busquedaProcedimientoPortlet__id22"))).click()

        # Find the element for number of results using XPath and click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]"))).click()

        # Find the element for year of results using XPath and click it
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]"))).click()

        # Wait for the input field to appear after clicking the element
        input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[1]/td[2]/input")))
        
        # Write a name inside the input field
        input_element.send_keys(input_text)

        # Check the checkboxes
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[1]/td[4]/label/input"))).click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[11]/td[2]/table/tbody/tr[1]/td[2]/label/input"))).click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[27]/td[2]/table/tbody/tr[3]/td[2]/label/input"))).click()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[29]/td[2]/input"))).click()

        # Select the year from start_index to 13
        dropdown_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[1]/tbody/tr[3]/td[3]/span/select")))
        dropdown = Select(dropdown_element)

        for index in range(start_index, 12, -1):
            dropdown.select_by_index(index)
            time.sleep(1)  # Wait for 1 second to ensure the page updates

        # Select the option by visible text
        dropdown_element2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[8]/td[2]/select")))
        dropdown2 = Select(dropdown_element2)
        dropdown2.select_by_visible_text(search_text)

        # Hit the Search button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input"))).click()

        # Wait until the contents are loaded
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))

        # Scrape the visible content
        scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

        # Parse and save data
        parsed_data = parse_text(scraped_content)
        save_to_json(parsed_data)

    finally:
        # Quit the driver
        driver.quit()

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
    return data_list

def save_to_json(data, filepath='scraped_data_prueba.json'):
    try:
        with open(filepath, 'r+') as file:
            existing_data = json.load(file)
            existing_data.extend(data)
            file.seek(0)
            json.dump(existing_data, file, indent=4)
    except FileNotFoundError:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: script.py <input_text> <start_index> <search_text>")
        sys.exit
