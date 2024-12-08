from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# Set up the WebDriver with Chrome options
def setup(driver_path):
    chrome_service = Service(executable_path=driver_path)
    chrome_options = Options()
    # Disable popup blocking to ensure smooth navigation
    chrome_options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

# Initialize the WebDriver
driver = setup('chromedriver-linux64/chromedriver')

# Extract the recipe title
def get_title():
    try:
        # Locate the title container and extract the text
        container = driver.find_element(By.CLASS_NAME, 'recipe-decision-block__title')
        return container.text
    except:
        # Return a placeholder if the element is not found
        return "-"

# Extract the recipe description
def get_description():
    try:
        # Locate the description container and extract the text
        container = driver.find_element(By.CLASS_NAME, 'heading__subtitle')
        return container.text
    except:
        # Return a placeholder if the element is not found
        return "-"

# Extract metadata such as prep, cook, total time, and serving size
def get_meta():
    try:
        # Locate the metadata container
        container = driver.find_element(By.ID, "recipe-decision-block__container_1-0")
        # Extract labels (e.g., Prep, Cook) and corresponding data
        label = container.find_elements(By.CLASS_NAME, 'meta-text__label')
        data = container.find_elements(By.CLASS_NAME, 'meta-text__data')
        labels = [i.text for i in label]
        data = [i.text for i in data]

        # Initialize placeholders for the metadata
        prep, cook, total, serves = "-", "-", "-", "-"

        # Map extracted data to appropriate labels
        for i in range(len(labels)):
            if labels[i] == "Prep":
                prep = data[i]
            if labels[i] == "Cook":
                cook = data[i]
            if labels[i] == "Total":
                total = data[i]
            if labels[i] == "Serves":
                serves = data[i]
        return prep, cook, total, serves
    except:
        # Return placeholders if metadata cannot be extracted
        return "-", "-", "-", "-"

# Extract the recipe image URL
def get_image():
    try:
        # Locate the image element and extract the source URL
        container = driver.find_element(By.CLASS_NAME, "primary-image__image")
        return container.get_attribute("src")
    except:
        # Return a placeholder if the image is not found
        return "-"

# Extract the recipe rating
def get_rating():
    try:
        # Locate the rating container
        container = driver.find_element(By.ID, "aggregate-star-rating__stars_1-0")
        # Count the number of active (filled) stars
        active_stars = container.find_elements(By.CSS_SELECTOR, 'a.active')
        return len(active_stars)
    except:
        # Return a placeholder if the rating is not available
        return "-"

# Extract the list of ingredients
def get_ingredients():
    try:
        # Locate all ingredient list items and extract their text
        ingredients = driver.find_elements(By.CLASS_NAME, 'structured-ingredients__list-item')
        return [i.text for i in ingredients]
    except:
        # Return a placeholder if no ingredients are found
        return "-"

# Extract the recipe instructions
def get_instructions():
    try:
        # Locate all instruction steps and extract their text
        instructions_elements = driver.find_elements(By.CSS_SELECTOR, 'ol.comp.mntl-sc-block > li.comp.mntl-sc-block')
        instructions = [instruction.find_element(By.CSS_SELECTOR, 'p.comp.mntl-sc-block-html').text for instruction in instructions_elements]
        return instructions
    except:
        # Return a placeholder if instructions are not available
        return "-"

# Initialize the CSV file for storing data
filename = "seriouseats2.csv"
def initialize():
    with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["title", "description", "cuisine", "rating", "ingredient_list", "serving", "prep_time", "cook_time", "total_time", "source", "steps", "recipe_url", "image_url"])

# Store extracted data in the CSV file
def store_output(title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, totaltime, steps, recipeurl, imageurl):
    data = [title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, totaltime, "SeriousEats", steps, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Initialize the CSV file
initialize()

# Counter for tracking errors
count = 0

# Open the file containing recipe links and iterate through them
with open("seriouseats/links.txt") as file:
    cuisine = "-"
    for link in file:
        # Check if the line is a comment indicating cuisine type
        if (link[0] == '#'):
            cuisine = link
            cuisine = ' '.join(cuisine.split()[:-2])
            cuisine = cuisine[1:]  # Remove the leading '#' character
            continue
        try:
            # Navigate to the recipe URL
            driver.get(link)
            time.sleep(2)
            
            # Extract metadata and other details
            prep, cook, total, serves = get_meta()
            title, desc, rating, ingrd, servings, preptime, cooktime, totaltime, steps, recipeurl, imageurl = (
                get_title(),
                get_description(),
                get_rating(),
                get_ingredients(),
                serves,
                prep,
                cook,
                total,
                get_instructions(),
                link.strip(),
                get_image()
            )
            
            # Save the extracted data to the CSV
            store_output(title, desc, cuisine, rating, ingrd, servings, preptime, cooktime, totaltime, steps, recipeurl, imageurl)
        
        except Exception as e:
            # Handle errors and increment the error counter
            count += 1
            print(f"Error {count}: Unable to process {link.strip()}")
