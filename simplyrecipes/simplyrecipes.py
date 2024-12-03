# Import necessary libraries 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import re

# Creating a 'simplyrecipes.csv' file to store recipe information

filename = "simplyrecipes.csv"

with open(filename, mode="w", newline="", encoding='utf-8') as file:

    writer = csv.writer(file)

    # Parameters for each recipe: title, description, cuisine, ingredient_list, servings, prep_time, 
    #                             cook_time, total_time, source, steps, nutrients, recipe_url, image_url

    writer.writerow(["title","description","cuisine","ingredient_list","serving","prep_time",
                     "cook_time","total_time","source","steps","nutrients","recipe_url","image_url"])


# Define paths and initialize the Chrome WebDriver

driver_path = 'chromedriver-win32\\chromedriver.exe'
chrome_service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service)

# Function to extract recipe title
def get_title():
    try:
        title_element = driver.find_element(By.XPATH, "//h2[@id='recipe-block__header_1-0']").text
    except:
        title_element = '-'
    return title_element


# Function to extract recipe description
def get_description():
    try:
        desc = driver.find_element(By.XPATH, "//p[@class='heading__subtitle']").text
        desc = re.sub(r'<br\s*\/?>', ' ', desc) # Replace <br> tags with spaces
        desc = re.sub(r'<.*?>', '', desc) # Remove other HTML tags
        desc = " ".join(desc.split()) # Clean up extra whitespace
    except: 
        desc = "-"
    return desc


# Function to extract the list of ingredients
def get_ingredients():
    all_ingredients = []
    try:
        ul_elements = driver.find_elements(By.XPATH, "//ul[@class='structured-ingredients__list text-passage']")
        for ul in ul_elements:
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            ingredients = [li.text for li in li_elements]
            all_ingredients.extend(ingredients) 
    except:
        pass
    return all_ingredients


# Function to extract list of steps
def get_steps():
    all_steps = []
    try:
        uls = driver.find_elements(By.XPATH, "//ol//*[self::div[contains(@class, 'comp mntl-sc-block lifestyle-sc-block-subheading mntl-sc-block-subheading')] or self::p[contains(@class,'comp mntl-sc-block mntl-sc-block-html')]]")
        for ul in uls:
            all_steps.append(ul.text)
            
    except:
        pass
    return all_steps


# Function to extract metadata like prep time, cook time, total_time, and servings
def get_metadata():
    try:
        prep_time = driver.find_element(By.XPATH, "//div[@class='prep-time project-meta__prep-time']//span[@class='meta-text__data']").text
    except:
        prep_time = "-"
    try:
        cook_time = driver.find_element(By.XPATH, "//div[@class='cook-time project-meta__cook-time']//span[@class='meta-text__data']").text
    except:
        cook_time = "-"
    try:
        total_time = driver.find_element(By.XPATH, "//div[@class='total-time project-meta__total-time']//span[@class='meta-text__data']").text
    except:
        total_time = "-"
    try:        
        serves = driver.find_element(By.XPATH, "//div[@class='recipe-serving project-meta__recipe-serving']//span[@class='meta-text__data']").text
    except: 
        serves = "-"
    return prep_time, cook_time, total_time, serves


# Function to extract image_url
def get_image_url():
    try:
        image_element = driver.find_element(By.XPATH, "//img[@class='primary-image__image mntl-primary-image--blurry loaded']")
        img_src = image_element.get_attribute("src")
    except:
        img_src = "-"
    return img_src
    

# Function to extract nutrients
def get_nutrients():
    nutrients = []
    try:
        nutrient = driver.find_elements(By.XPATH, "//tr[@class='nutrition-info__table--row']")
        for nu in nutrient:
            element = nu.find_elements(By.TAG_NAME,'td')
            nutrient_info = [el.text for el in element]
            nutrient_info.reverse()
            nutrients.append(nutrient_info)
    except:
        nutrients = []
    return nutrients


# Function to scrape recipe data for each link
def get_recipe_data():

    # There are two .txt file with links.
    # simplyrecipeslinks_cuisine.txt : Contains recipe links that has Cuisine data
    # simplyrecipeslinks_no_cuisine.txt : Contains just recipe links without Cuisine data

    links_with_cuisine = 'simplyrecipes\simplyrecipeslinks_cuisine.txt'
    links_no_cuisine = 'simplyrecipes\simplyrecipeslinks_no_cuisine.txt'

    with open(links_with_cuisine, 'r') as file:
        for line in file:

            # content = line.strip()              # If links_no_cuisine was used
            content = line.strip().split(',')  

            # driver.get(content)                 # If links_no_cuisine was used
            driver.get(content[1])

            title = get_title()
            desc = get_description()
            preptime, cooktime, totaltime, serves = get_metadata()
            ingrd = get_ingredients()
            steps = get_steps()
            imageurl = get_image_url()
            recipeurl = driver.current_url
            nutrients = get_nutrients()

            # cuisine = "-"                  # If links_no_cuisine was used
            cuisine = content[0]
            
            store_output(title, desc, cuisine, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl)


# Function to store recipe data into the CSV         
def store_output(title, desc, cuisine, ingrd, serves, preptime, cooktime, totaltime, steps, nutrients, recipeurl, imageurl):
    filename = "simplyrecipes.csv"
    data=[title, desc, cuisine, ingrd, serves, preptime, cooktime, totaltime,"Simply Recipes", steps, nutrients, recipeurl, imageurl]
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)


get_recipe_data()  # To scrape recipe data from each link stored in .txt files and store in simplyrecipes.csv file

driver.quit()  # Close browser


