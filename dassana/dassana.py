# Import necssary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re

# Creating a 'dassab=na.csv' file to store recipe data

filename = "dassana.csv"

with open(filename, mode="w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file)

    # Parameters for each recipe: title, description, cuisine, rating, ingredient_list, servings, prep_time, 
    #                             cook_time, total_time, source, steps, nutrients, recipe_url, image_url

    writer.writerow(["title","description","cuisine","rating","ingredient_list","serving","prep_time",
                     "cook_time","total_time","source","steps","nutrients","recipe_url","image_url"])


# Define paths and initialize the Chrome WebDriver
driver_path = 'chromedriver-win32\\chromedriver.exe'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)


# Function to get recipe title
def get_title():
    try:
        title_element = driver.find_element(By.XPATH, "//h2[@class='wprm-recipe-name wprm-block-text-normal']").text
    except:
        title_element = '-'
    return title_element


# Function to get recipe description
def get_description():
    try:
        desc = driver.find_element(By.XPATH, "//div[@class='wprm-recipe-summary wprm-block-text-normal']").text
        desc = re.sub(r'<br\s*\/?>', ' ', desc) # Replace <br> tags with spaces
        desc = re.sub(r'<.*?>', '', desc) # Remove other HTML tags
        desc = " ".join(desc.split())  # Clean up extra whitespace
    except: 
        desc = "-"
    return desc


# Function to get list of ingredients
def get_ingredients():
    all_ingredients = []
    try:
        ul_elements = driver.find_elements(By.XPATH, "//ul[@class='wprm-recipe-ingredients']")
        for ul in ul_elements:
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            ingredients = [li.text[2:] for li in li_elements]
            all_ingredients.extend(ingredients) 
    except:
        pass
    return all_ingredients


# Function to get list of steps
def get_steps():
    all_steps = []
    try:
        ul = driver.find_elements(By.XPATH, "//ul[@class='wprm-recipe-instructions']")
        for u in ul:
            li_elements = u.find_elements(By.TAG_NAME, 'li')
            for li in li_elements:
                step = li.text
                step = re.sub(r'<br\s*\/?>', ' ', step)  # Replace <br> tags with spaces
                step = re.sub(r'<.*?>', '', step) # Remove other HTML tags
                step = " ".join(step.split()) # Clean up extra whitespace
                all_steps.append(step)
    except:
        pass
    return all_steps


# Function to get metadata - prep_time, cook_time, total_time, serves
def get_metadata():
    try:
        prep_time = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-prep_time wprm-recipe-prep_time-minutes']").text.replace("\n"," ")
    except:
        prep_time = "-"
    try:
        cook_time = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-cook_time wprm-recipe-cook_time-minutes']").text.replace("\n"," ")
    except:
        cook_time = "-"
    try:
        total_time = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-details wprm-recipe-details-minutes wprm-recipe-total_time wprm-recipe-total_time-minutes']").text.replace("\n"," ")
    except:
        total_time = "-"
    try:        
        serves = driver.find_element(By.XPATH, "//div[@class='wprm-recipe-ingredients-servings']").find_element(By.TAG_NAME, 'input').get_attribute("value")
    except: 
        serves = "-"
    
    return prep_time, cook_time, total_time, serves


# Function to get image url
def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//div[@class='wp-block-image']")

        # Scrolling to get the image into view
        driver.execute_script("arguments[0].scrollIntoView();", image_element)

        # Waiting for image to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'img')))

        img_element = image_element.find_element(By.TAG_NAME, 'img')

        img_src = img_element.get_attribute("src")
        
        # In case there's a placeholder instead of actual image
        if "data:image/svg+xml" in img_src or "placeholder" in img_src:
            img_src = img_element.get_attribute("data-src") or img_element.get_attribute("data-lazy-src") or img_element.get_attribute("data-srcset")
    except:
        img_src = "-"
    return img_src
    

# Function to get recipe rating
def get_rating():
    try:
        rating = driver.find_element(By.XPATH, "//div[@class='wprm-recipe-rating-details wprm-block-text-normal']//span[@class='wprm-recipe-rating-average']").text
    except:
        rating = '-'
    return rating


# Function to get cuisine of recipe
def get_cuisine():
    try:
        cuisine = driver.find_element(By.XPATH, "//span[@class='wprm-recipe-cuisine wprm-block-text-bold']").text
    except:
        cuisine = "-"
    return cuisine


# Function to get nutrients data
def get_nutrients():
    Nutrients = []

    # Main Nutrients
    main = driver.find_elements(By.XPATH, "//span[@class='nutrition-main']")
    for el in main:
        Nutrients.append([el.text])

    # Sub Nutrients
    sub = driver.find_elements(By.XPATH, "//span[@class='nutrition-sub']")
    for el in sub:
        Nutrients.append([el.text])
    return Nutrients


# Function to scrape recipe data from 'dassanalinks.txt' and store data to 'dassana.csv'
def get_recipe_data():
    with open('dassanalinks.txt', 'r') as file:
        for line in file:
            driver.get(line)
            title = get_title()
            desc = get_description()
            preptime, cooktime, totaltime, serves = get_metadata()
            ingrd = get_ingredients()
            steps = get_steps()
            imageurl = get_image_url()
            recipeurl = driver.current_url
            rating = get_rating()
            cuisine = get_cuisine()
            nutrients = get_nutrients()
            store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl)


# Function to store recipe data to 'dassana.csv'
def store_output(title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl):
    filename = "dassana.csv"
    data=[title, desc, cuisine, rating, ingrd, serves, preptime, cooktime, totaltime,"Dassana's Veg Recipes", steps, nutrients, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


# there is a dassanalinks.txt file where all the links of recipes are saved
# Calls function to scrape data from each recipe link
get_recipe_data()  


# Closes browser
driver.quit()