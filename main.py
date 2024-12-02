import base64
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

directory_name = "images"
try:
    os.mkdir(directory_name)
except Exception:
    print("La carpeta ya existe")

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Ensure GUI is not displayed
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Define the path to chromedriver (this works in Colab)
chrome_driver_path = "/usr/bin/chromedriver"

# Setup the Chrome service
service = Service(chrome_driver_path)

# Create a WebDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to a webpage
search_key_word = "HOMER SIMPSON PROGRAMMING"
query = f"https://www.google.com/search?q={search_key_word}&tbm=isch"

driver.get(query)

images = driver.find_elements(By.CLASS_NAME, 'YQ4gaf')

# Define minimum resolution
min_width = 150  # Minimum width in pixels
min_height =150  # Minimum height in pixels

for index, image in enumerate(images):
    try:
        # Extract the base64 data from the image src
        image_data = image.get_attribute('src')
        
        # Extract width and height attributes
        width = image.get_attribute('width')
        height = image.get_attribute('height')
        
        # If width or height is None, skip this image
        if width is None or height is None:
            print(f"Image {index} skipped: Missing width or height.")
            continue
        
        width = int(width)
        height = int(height)
        
        # Check if the image meets the minimum resolution
        if width >= min_width and height >= min_height:
            # Check if the image is base64 encoded
            if image_data.startswith('data:image/jpeg;base64,'):
                # Remove the prefix 'data:image/jpeg;base64,' to get the base64 string
                base64_image = image_data.split('base64,')[1]
                
                # Decode the base64 string
                img_data = base64.b64decode(base64_image)
                
                # Save the image to a file
                with open(f'./images/img_{index}.jpg', 'wb') as f:
                    f.write(img_data)
                print(f"High-quality image {index} saved successfully.")
            else:
                print(f"Image {index} is not base64 encoded.")
        else:
            print(f"Image {index} skipped: Resolution too low ({width}x{height}).")
    except Exception as e:
        print(f"Error processing image {index}: {e}")

# Example action: find and print the page title
print(driver.title)

# Close the driver
driver.quit()
