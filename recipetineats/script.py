from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

#note 1: a lot of try-except is necessary so that scraping does not stop because of errors midway
#note 2: it is necessary to scrape recipe links before hand:
#by opening all categories and then storing link for each recipe.
#mistakenly lost the script for this - but very easy to write.

#parameters to store:
#title,description,cuisine,rating,ingredient_list,serving,prep_time,cook_time,source,steps,recipe_url,image_url

#basic setup for selenium

def setup(driver_path):
    # setup chrome driver service and options
    chrome_service = Service(executable_path=driver_path)
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    return webdriver.Chrome(service=chrome_service, options=chrome_options)

driver = setup('chromedriver-linux64/chromedriver')
filename = "RecipeTinEats.csv"

"""
parameters to store:
title,description,cuisine,rating,ingredient_list,serving,prep_time,cook_time,source,steps,recipe_url,image_url
"""

def gettime(classname):
    # get formatted time values from elements with specific class name
    timeel = driver.find_elements(By.CLASS_NAME, classname)
    time_ = ""
    for i in range(len(timeel)):
        time_ += timeel[i].text.replace('\n', ' ')
        time_ += " "
    return time_
        
def getdata(link):
    # initialize data fields with default values
    title = "-"
    description = "-"
    cuisine = "-"
    rating = "-"
    ingredients = "-"
    serving = "-"
    prep_time = "-"
    cook_time = "-"
    total_time = "-"
    source = "RecipeTinEats"
    instructions = "-"
    nutrients_f = "-"
    image_url = "-"
    
    # navigate to the recipe link
    try:
        driver.get(link)
        time.sleep(0.5)
    except:
        pass
    
    # scrape ingredients
    try:
        ingr_el = driver.find_elements(By.CLASS_NAME, 'wprm-recipe-ingredient')
        ingredients = [''.join(i for i in item.text if i != '▢' and i != '\n') for item in ingr_el]
    except:
        ingredients = "-"
    
    # scrape instructions
    try:
        instr_el = driver.find_elements(By.CLASS_NAME, 'wprm-recipe-instructions')
        for item in instr_el:
            try:
                instr_els = item.find_elements(By.TAG_NAME, 'li')
                try:
                    instructions = [i.text for i in instr_els]
                except:
                    instructions = "-"
            except:
                instructions = "-"
    except:
        instructions = "-"
    
    # scrape title
    try:
        title = driver.find_element(By.CLASS_NAME, 'wprm-recipe-name').text
    except:
        title = "-"
    
    # scrape cooking times
    try:
        cook_time = gettime('wprm-recipe-cook_time')
    except:
        cook_time = "-"
    try:
        prep_time = gettime('wprm-recipe-prep_time')
    except:
        prep_time = "-"
    try:
        total_time = gettime('wprm-recipe-total_time')
    except:
        total_time = "-"
        
    # scrape rating
    try:
        rating = driver.find_element(By.CLASS_NAME, 'wprm-recipe-rating-details').text
    except:
        rating = "-"
    
    # scrape cuisine type
    try:
        cuisine = driver.find_element(By.CLASS_NAME, 'wprm-recipe-cuisine').text
    except:
        cuisine = "-"
        
    # scrape description
    try:
        description = driver.find_element(By.CLASS_NAME, 'wprm-recipe-summary').text
        description = description.replace('\n', ' ')
    except:
        description = "-"
    
    # scrape serving size
    try:
        serving = driver.find_element(By.CLASS_NAME, 'wprm-recipe-servings-with-unit').text
    except:
        serving = "-"
    
    # scrape image url
    try:
        image_el = driver.find_element(By.TAG_NAME, 'img')
        image_url = image_el.get_attribute("src")   
    except:
        image_url = "-"
    
    # scrape nutrition information
    try:
        nutrients = driver.find_element(By.CLASS_NAME, 'wprm-entry-nutrition').text
        nutrients = nutrients.split(')')
        nutrients = [i + ')' if i.endswith('%') else i for i in nutrients]
        nutrients_f = []
        for line in nutrients:
            arr = line.split(': ')
            if (len(arr) != 2):
                continue
            nutrient, value = arr[0], arr[1]
            nutrient = nutrient.split('\n')[-1]
            nutrients_f.append([nutrient, value])
    except:
        nutrients_f = "-"
        
    # create a list of all the scraped data
    data = [title, description, cuisine, rating, ingredients, serving, prep_time, cook_time, total_time, source, instructions, nutrients_f, link, image_url]
    
    # write the data to a csv file
    with open(filename, mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    

# create csv file and write the header row
with open(filename, mode="w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title","description","cuisine","rating","ingredient_list","serving","prep_time","cook_time","total_time", "source","steps", "nutrients", "recipe_url","image_url"])

# read links from file and scrape data for each link
links = open('recipetineats/links.txt', 'r')
for link in links:
    getdata(link)
