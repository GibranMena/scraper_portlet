
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
driver.get("https://www.gestion.nicaraguacompra.gob.ni/siscae/portal/adquisiciones-gestion/busqueda/#")

# Click on the first link

element = driver.find_element(By.CSS_SELECTOR, "#app-nav .menubar a")
element.click()

# Find the element to hover over
hover_element = driver.find_element(By.CSS_SELECTOR, '#app-nav .menubar:nth-child(1) a')

# Create an ActionChains object
action = ActionChains(driver)

# Hover over the element
action.move_to_element(hover_element).perform()

element2 = driver.find_element(By.CSS_SELECTOR, ".#app-nav .menubar:nth-child(1) > a , .menubar .menubar li+ li a")
element2.click()




# Wait for the second element to appear after the first hover
second_hover_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.menubar .menubar li+ li a')))


# Create another ActionChains object for the second action
action2 = ActionChains(driver)

# Find the second element to hover over and click
#second_element = driver.find_element(By.CSS_SELECTOR, '.menubar .menubar li+ li a')

# Hover over the second element
#action2.move_to_element(second_element).click().perform()

second_hover_element = driver.find_element(By.CSS_SELECTOR, '.menubar .menubar li+ li a')


# Hover over the second element displayed by the first hover
action.move_to_element(second_hover_element).perform()

# Wait for the third element to appear after the second hover
third_element_to_select = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.menubar .menubar li+ li a')))

# Click on the third element shown by the series of hoverings
third_element_to_select.click()

action2 = ActionChains(driver)

#Find second element to hover over

hover_element2 = driver.find_element(By.CSS_SELECTOR, '.menubar .menubar li+ li a')

# Hover over the second element
action2.move_to_element(hover_element2).perform()

# Wait for the submenu to be visible
submenu_locator = (By.CSS_SELECTOR, '.menubar .menubar li+ li a')
#WebDriverWait(driver, 10).until(EC.visibility_of_element_located(submenu_locator))

# Find and click the submenu
submenu_element = driver.find_element(*submenu_locator)
submenu_element.click()



#app-nav .menubar:nth-child(1) a

# Wait for the page to load
time.sleep(5)

# Click on the second link
second_link = driver.find_element_by_css_selector("a.second-link")
second_link.click()

# Wait for the page to load
time.sleep(5)

# Click on the third link
third_link = driver.find_element_by_css_selector("a.third-link")
third_link.click()

# Wait for the page to load
time.sleep(5)

# Scrape the final webpage
final_page_content = driver.page_source

# Print the final webpage content
print(final_page_content)

# Close the browser
driver.quit()