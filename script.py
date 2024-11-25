import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the webdriver
driver = webdriver.Chrome()

# Function to process each page
def process_page(url):
    try:
        print(f"Processing {url}...")

        # Open the webpage
        driver.get(url)

        # Wait for the page to load by checking for the main wrapper element
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]'))
            )

            # Optional: Additional time to ensure page is fully rendered
            time.sleep(2)

            # Try to extract the h2 tag (or handle missing element)
            try:
                quote_cards = driver.find_element(By.XPATH, '//div[@class="quote-card"]')
                h2_tag = quote_cards.find_element(By.TAG_NAME, 'h1').text

                # Sanitize the h2_tag to create a valid file name
                file_name = f"{h2_tag.replace(' ', '_').replace('/', '_').replace('\\', '_')}.csv"

                # Prepare the CSV file for writing
                with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Image Link", "Title", "Price"])

                    # Find the items and extract their details
                    items_container = driver.find_element(By.XPATH, '//div[@class="wrapper"]')
                    items = items_container.find_elements(By.XPATH, '//div[@class="card"]')

                    if not items:
                        print(f"No products found on {url}. Moving to the next link...")
                        return

                    for index, item in enumerate(items):
                        try:
                            img_element = item.find_element(By.XPATH, './/img[@class="preview-image"]')
                            img_link = img_element.get_attribute("src")
                            title_element = item.find_element(By.XPATH, './/h1[@class="card-title"]')
                            title_text = title_element.text
                            price_element = item.find_element(By.XPATH, './/div[@class="card-body"]')
                            price_text = price_element.find_element(By.TAG_NAME, 'h2').text

                            # Write item data to CSV
                            writer.writerow([img_link, title_text, price_text])

                            print(f"Produit {index + 1}:")
                            print(f"  Image Link: {img_link}")
                            print(f"  Title: {title_text}")
                            print(f"  Price: {price_text}")

                        except Exception as e:
                            print(f"Error processing item {index + 1}: {e}")

                print(f"Data exported to {file_name}")

            except Exception as e:
                print(f"No content found or error extracting details on {url}. Error: {e}. Moving to the next link...")

        except Exception as e:
            print(f"Error loading page {url}: {e}. Moving to the next link...")

    except Exception as e:
        print(f"Error processing {url}: {e}. Moving to the next link...")

# Loop through categories 121 to 127, excluding 123
for category in range(121, 128):
    if category == 123:  # Skip category 123
        continue
    for i in range(700, 738):
        url = f"https://www.elkolla.scanini.tn/client/categories/{category}/{i}"
        process_page(url)

# Close the webdriver after all processing is done
driver.quit()
