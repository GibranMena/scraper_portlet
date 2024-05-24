import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Initialize the WebDriver
def initialize_webdriver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver

# Function to interact with the page, select option from dropdown by text, and input text
def interact_with_page(driver, dropdown_text, input_text):
    # Open the webpage
    driver.get("http://example.com")  # Replace with your target URL

    # Find the dropdown menu using the XPATH
    dropdown_element = driver.find_element(By.XPATH, "/html/body/div[4]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/div/div/div/table[2]/tbody/tr/td/form/table[2]/tbody/tr[8]/td[2]/select")
    
    # Wrap the element in a Select object
    dropdown = Select(dropdown_element)
    
    # Select the option by visible text
    dropdown.select_by_visible_text(dropdown_text)

    # Find the input field and input the text
    input_element = driver.find_element(By.XPATH, 'XPATH_OF_INPUT_FIELD')  # Replace with the actual XPATH of the input field
    input_element.send_keys(input_text)

    # Assume some scraping logic here to get the data
    data = {"dropdown_text": dropdown_text, "input_text": input_text, "scraped_data": "example_data"}  # Replace with actual scraped data

    return data

# Function to save or append data to a JSON file
def save_to_json(data, filename="data.json"):
    try:
        with open(filename, 'r+') as file:
            # Load existing data
            existing_data = json.load(file)
            # Append new data
            existing_data.append(data)
            # Move the cursor to the beginning of the file
            file.seek(0)
            # Save updated data
            json.dump(existing_data, file, indent=4)
    except FileNotFoundError:
        # File does not exist, create it and save data
        with open(filename, 'w') as file:
            json.dump([data], file, indent=4)

# Function to convert JSON to CSV
def json_to_csv(json_filename="data.json", csv_filename="data.csv"):
    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
    
    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Main function to run the entire process
def main(dropdown_texts, input_text):
    driver = initialize_webdriver()

    for text in dropdown_texts:
        data = interact_with_page(driver, text, input_text)
        save_to_json(data)

    driver.quit()

    # Convert final JSON to CSV
    json_to_csv()

# Example usage
dropdown_texts = ["Option1", "Option2", "Option3"]  # List of option texts to search and select
input_text = "Bismarck Martinez"  # User input

main(dropdown_texts, input_text)