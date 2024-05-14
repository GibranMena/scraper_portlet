
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

# Find the element using XPath and click it
element2 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/div/table/tbody/tr/td[4]/select/option[4]")
element2.click()

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
element3 = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[3]/tbody/tr/td[1]/input")
element3.click()

# Wait until the contents are loaded
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td/table")))

# Initialize CSV file and writer
csv_file = open('scraped_data.csv', 'a', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)

# Scrape the visible content using full XPath
scraped_content = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/form[2]/table[1]/tbody/tr[3]/td").text

# Write the scraped content to the CSV file
csv_writer.writerow([scraped_content])

# Close the CSV file
csv_file.close()

# Quit the driver
driver.quit()








