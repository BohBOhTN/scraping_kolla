import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the webdriver
driver = webdriver.Chrome()

# Open the webpage
driver.get("https://www.elkolla.scanini.tn/client/categories/121/730")

# Wait for the page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]'))
)

# Get the h2_tag text to use as the CSV file name
quote_cards = driver.find_element(By.XPATH, '//div[@class="quote-card"]')
h2_tag = quote_cards.find_element(By.TAG_NAME, 'h1').text

# Sanitize the h2_tag to make it a valid file name
file_name = f"{h2_tag.replace(' ', '_').replace('/', '_').replace('\\', '_')}.csv"

# Prepare the CSV file for writing
with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row for CSV
    writer.writerow(["Image Link", "Title", "Price"])

    # Find the items and extract their details
    items_container = driver.find_element(By.XPATH, '//div[@class="wrapper"]')
    items = items_container.find_elements(By.XPATH, '//div[@class="card"]')

    for index, item in enumerate(items):
        try:
            # Extract item details
            img_element = item.find_element(By.XPATH, './/img[@class="preview-image"]')
            img_link = img_element.get_attribute("src")
            title_element = item.find_element(By.XPATH, './/h1[@class="card-title"]')
            title_text = title_element.text
            price_element = item.find_element(By.XPATH,'//div[@class="card-body"]')
            price_text = price_element.find_element(By.TAG_NAME,'h2').text

            # Write item data to CSV
            writer.writerow([img_link, title_text, price_text])

            print(f"  Image Link: {img_link}")
            print(f"  Title: {title_text}")
            print(f"  Price: {price_text}")

        except Exception as e:
            print(f"Error processing product: {e}")

# Close the webdriver
driver.quit()

print(f"Data exported to {file_name}")
